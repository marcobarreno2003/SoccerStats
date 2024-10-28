import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import pandas as pd
import requests
import joblib

def preprocess_data(X):
    # Set handle_unknown='ignore' to avoid errors with unseen team names
    column_transformer = ColumnTransformer(
        transformers=[
            ('team', OneHotEncoder(handle_unknown='ignore'), ['home_team', 'away_team']),
        ], remainder='passthrough'
    )

    X_transformed = column_transformer.fit_transform(X)
    return X_transformed, column_transformer

def preprocess_for_prediction(X, column_transformer, scaler):
    """Apply the same preprocessing steps used during training for new input data."""
    X_transformed = column_transformer.transform(X)
    X_transformed[:, -2:] = scaler.transform(X_transformed[:, -2:])
    print("Shape of preprocessed input:", X_transformed.shape)  # Debugging line
    return X_transformed

def get_matches(api_key, league_id, season, date_from, date_to):
    """Fetches match data from the API."""
    url = 'https://v3.football.api-sports.io/fixtures'
    
    headers = {
        'x-rapidapi-host': 'v3.football.api-sports.io',
        'x-rapidapi-key': api_key
    }

    params = {
        'league': league_id,
        'season': season,
        'from': date_from,
        'to': date_to
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if 'response' in data and len(data['response']) > 0:
        return data['response']
    else:
        return []

def process_matches(match_data):
    """Processes raw match data into features (X) and labels (y)."""
    matches = []
    for match in match_data:
        result = 0  # Default to draw
        if match['teams']['home']['winner']:
            result = 1  # Home team win
        elif match['teams']['away']['winner']:
            result = 2  # Away team win
        
        match_info = {
            'home_team': match['teams']['home']['name'],
            'away_team': match['teams']['away']['name'],
            'home_goals': match['goals']['home'],
            'away_goals': match['goals']['away'],
            'result': result
        }
        matches.append(match_info)

    df = pd.DataFrame(matches)
    
    if df.empty:
        print("No valid match data found.")
        return None, None

    X = df[['home_team', 'away_team', 'home_goals', 'away_goals']]
    y = df['result']

    return X, y

def train_model(X, y):
    """Creates, trains, and evaluates a neural network model."""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale numerical columns (goals)
    scaler = StandardScaler(with_mean=False)
    X_train[:, -2:] = scaler.fit_transform(X_train[:, -2:])
    X_test[:, -2:] = scaler.transform(X_test[:, -2:])
    
    # Build the model
    model = Sequential([
        Input(shape=(X_train.shape[1],)),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(3, activation='softmax')
    ])
    
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))
    
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f'Model accuracy: {accuracy * 100:.2f}%')
    
    return model, scaler

# Main flow for training and saving model and scaler
if __name__ == "__main__":
    api_key = '11ad5f439755ea3775a46bd3736c4255'
    league_id = '39'
    season = '2022'
    date_from = '2021-01-01'
    date_to = '2022-12-31'

    # Get the match data
    match_data = get_matches(api_key, league_id, season, date_from, date_to)

    if match_data:
        print(f"Found {len(match_data)} matches.")
        X, y = process_matches(match_data)

        if X is not None and y is not None:
            # Preprocess the data
            X_processed, column_transformer = preprocess_data(X)
            
            # Train the model
            model, scaler = train_model(X_processed, y)
            
            # Save the model, scaler, and column transformer
            model.save('backend/api/soccer_model.keras')
            joblib.dump(scaler, 'backend/api/scaler.save')
            joblib.dump(column_transformer, 'backend/api/column_transformer.save')
    else:
        print("No match data was returned by the API.")
