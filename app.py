import os
import sys
import numpy as np
import pandas as pd
import http.client
import joblib
from flask import Flask, json, render_template
from tensorflow.keras.models import load_model

# ---------------------------
# Flask configuration
# ---------------------------
app = Flask(__name__, template_folder="templates", static_folder="static")

# Make sure we can import from /api
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
API_DIR = os.path.join(BASE_DIR, "api")
if API_DIR not in sys.path:
    sys.path.append(API_DIR)

# Import your preprocessing function
from api.data import preprocess_for_prediction  # noqa: E402

# ---------------------------
# Load trained ML artifacts
# ---------------------------
MODEL_PATH = os.path.join(API_DIR, "soccer_model.keras")
SCALER_PATH = os.path.join(API_DIR, "scaler.save")
COL_TRANSFORMER_PATH = os.path.join(API_DIR, "column_transformer.save")

model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
column_transformer = joblib.load(COL_TRANSFORMER_PATH)

# ---------------------------
# Main Routes
# ---------------------------

@app.route("/")
def index():
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        "x-rapidapi-host": "v3.football.api-sports.io",
        "x-rapidapi-key": os.getenv("API_FOOTBALL_KEY", "your_api_key_here"),
    }
    conn.request("GET", "/fixtures?live=all", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    parsed_data = json.loads(data)
    live_matches = parsed_data.get("response", [])

    labels = ["Draw", "Home Win", "Away Win"]

    for match in live_matches:
        home_team = match["teams"]["home"]["name"]
        away_team = match["teams"]["away"]["name"]
        home_goals = match["goals"]["home"]
        away_goals = match["goals"]["away"]

        X = pd.DataFrame([[home_team, away_team, home_goals, away_goals]],
                         columns=["home_team", "away_team", "home_goals", "away_goals"])
        X_processed = preprocess_for_prediction(X, column_transformer, scaler)
        prediction = model.predict(X_processed)
        predicted_label = np.argmax(prediction)
        match["prediction"] = labels[predicted_label]

    # 👇 corregido
    return render_template("index.html", live_matches=live_matches)


@app.route("/league/<int:league_id>")
def league(league_id):
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        "x-rapidapi-host": "v3.football.api-sports.io",
        "x-rapidapi-key": os.getenv("API_FOOTBALL_KEY", "your_api_key_here"),
    }
    conn.request("GET", f"/fixtures?league={league_id}&live=all", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    parsed_data = json.loads(data)
    live_matches = parsed_data.get("response", [])

    labels = ["Draw", "Home Win", "Away Win"]

    for match in live_matches:
        home_team = match["teams"]["home"]["name"]
        away_team = match["teams"]["away"]["name"]
        home_goals = match["goals"]["home"]
        away_goals = match["goals"]["away"]

        X = pd.DataFrame([[home_team, away_team, home_goals, away_goals]],
                         columns=["home_team", "away_team", "home_goals", "away_goals"])
        X_processed = preprocess_for_prediction(X, column_transformer, scaler)
        prediction = model.predict(X_processed)
        predicted_label = np.argmax(prediction)
        match["prediction"] = labels[predicted_label]

    # 👇 corregido
    return render_template("index.html", live_matches=live_matches)


@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    # from dotenv import load_dotenv; load_dotenv()  # opcional si usas .env
    app.run(debug=True)
