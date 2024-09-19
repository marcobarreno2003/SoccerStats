from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Función para obtener los datos de partidos (matches) desde GitHub
def fetch_matches_data():
    # URL de los datos de partidos
    url = 'https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/43/3.json'
    response = requests.get(url)
    return response.json()

# Función para obtener datos de eventos de un partido por match_id desde GitHub
def fetch_events_data(match_id):
    # URL de los datos de eventos
    url = f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json'
    response = requests.get(url)
    return response.json()

# Función para obtener las competiciones por año usando los datos de partidos
def get_competitions_by_year(matches_data):
    competitions_by_year = {}
    
    for match in matches_data:
        competition_name = match['competition']['competition_name']
        season = match['season']['season_name']
        match_id = match['match_id']
        
        if competition_name not in competitions_by_year:
            competitions_by_year[competition_name] = {}
        
        competitions_by_year[competition_name][season] = match_id
    
    return competitions_by_year

# Función para obtener rivales y resultados de los partidos
def get_match_details(matches_data):
    matches_info = []

    for match in matches_data:
        home_team = match['home_team']['home_team_name']
        away_team = match['away_team']['away_team_name']
        home_score = match['home_score']
        away_score = match['away_score']
        match_id = match['match_id']

        match_details = {
            "match_id": match_id,
            "home_team": home_team,
            "away_team": away_team,
            "home_score": home_score,
            "away_score": away_score
        }

        matches_info.append(match_details)

    return matches_info

# Endpoint para obtener las competiciones y años
@app.route('/competitions', methods=['GET'])
def competitions():
    matches_data = fetch_matches_data()  # Llama a la función para obtener los datos de los partidos
    competitions = get_competitions_by_year(matches_data)  # Agrupa las competiciones por año
    return jsonify(competitions)

# Ruta para obtener todos los partidos con detalles
@app.route('/matches', methods=['GET'])
def matches():
    matches_data = fetch_matches_data()  # Llama a la función para obtener los datos de los partidos
    match_details = get_match_details(matches_data)  # Extrae los detalles de cada partido
    return jsonify(match_details)

# Endpoint para acceder a un archivo JSON específico por match_id
@app.route('/events/<int:match_id>')
def get_match_data(match_id):
    events_data = fetch_events_data(match_id)  # Llama a la función para obtener los datos de eventos del partido
    return jsonify(events_data)

if __name__ == '__main__':
    app.run(debug=True)
