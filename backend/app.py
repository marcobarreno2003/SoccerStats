import os
import sys
import numpy as np
import pandas as pd
import http.client
import requests
import joblib
from flask import Flask, json, render_template
from tensorflow.keras.models import load_model

# Configuración de Flask
app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/assets')

# Configura el path para importar módulos desde la carpeta 'api'
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

# Importa la función de preprocesamiento desde data.py
from api.data import preprocess_for_prediction

# Cargar el modelo entrenado, el scaler y el column transformer
model_path = os.path.join(os.path.dirname(__file__), 'api', 'soccer_model.keras')
scaler_path = os.path.join(os.path.dirname(__file__), 'api', 'scaler.save')
column_transformer_path = os.path.join(os.path.dirname(__file__), 'api', 'column_transformer.save')

# Cargar modelo y transformadores pre-entrenados
model = load_model(model_path)
scaler = joblib.load(scaler_path)
column_transformer = joblib.load(column_transformer_path)

def preprocess_for_prediction(X):
    X_transformed = column_transformer.transform(X)
    X_transformed = X_transformed.toarray() if hasattr(X_transformed, "toarray") else X_transformed
    X_transformed[:, -2:] = scaler.transform(X_transformed[:, -2:])
    return X_transformed

# Ruta para la página principal
@app.route('/')
def index():
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        "x-rapidapi-host": "v3.football.api-sports.io",
        "x-rapidapi-key": "11ad5f439755ea3775a46bd3736c4255"
    }
    conn.request("GET", "/fixtures?live=all", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    parsed_data = json.loads(data)
    live_matches = parsed_data.get('response', [])

    for match in live_matches:
        home_team = match['teams']['home']['name']
        away_team = match['teams']['away']['name']
        home_goals = match['goals']['home']
        away_goals = match['goals']['away']

        X = pd.DataFrame([[home_team, away_team, home_goals, away_goals]], 
                         columns=['home_team', 'away_team', 'home_goals', 'away_goals'])
        X_processed = preprocess_for_prediction(X)
        prediction = model.predict(X_processed)
        predicted_label = np.argmax(prediction)
        labels = ["Draw", "Home Win", "Away Win"]
        match['prediction'] = labels[predicted_label]

    return render_template('index.html', live_matches=live_matches)

# Ruta para ver partidos en vivo de una liga específica
@app.route('/league/<int:league_id>')
def league(league_id):
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        "x-rapidapi-host": "v3.football.api-sports.io",
        "x-rapidapi-key": "11ad5f439755ea3775a46bd3736c4255"
    }
    conn.request("GET", f"/fixtures?league={league_id}&live=all", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    parsed_data = json.loads(data)
    live_matches = parsed_data.get('response', [])

    for match in live_matches:
        home_team = match['teams']['home']['name']
        away_team = match['teams']['away']['name']
        home_goals = match['goals']['home']
        away_goals = match['goals']['away']

        X = pd.DataFrame([[home_team, away_team, home_goals, away_goals]], 
                         columns=['home_team', 'away_team', 'home_goals', 'away_goals'])
        X_processed = preprocess_for_prediction(X)
        prediction = model.predict(X_processed)
        predicted_label = np.argmax(prediction)
        labels = ["Draw", "Home Win", "Away Win"]
        match['prediction'] = labels[predicted_label]

    return render_template('index.html', live_matches=live_matches)

# Ruta del Blog
@app.route('/blog')
def blog():
    return render_template('blog.html')

# Ruta de About Me
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
