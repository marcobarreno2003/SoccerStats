import os
import markdown
from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    blog_directory = 'blog_entries'
    blog_posts = []

    if os.path.exists(blog_directory):
        for filename in os.listdir(blog_directory):
            if filename.endswith(".md"):
                filepath = os.path.join(blog_directory, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    html_content = markdown.markdown(content)

                    # Extraemos la fecha y el título del archivo
                    post_title = filename.split('-')[3].replace('_', ' ').replace('.md', '')
                    post_date = '-'.join(filename.split('-')[:3])

                    blog_posts.append({
                        "title": post_title,
                        "date": post_date,
                        "content": html_content
                    })

    return render_template('blog.html', blog_posts=blog_posts)

@app.route('/stats')
def stats():
    return "This is the Soccer Stats page."

# Función para obtener los datos de partidos (matches) desde GitHub
def fetch_matches_data():
    url = 'https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/43/3.json'
    response = requests.get(url)
    return response.json()

# Función para obtener datos de eventos de un partido por match_id desde GitHub
def fetch_events_data(match_id):
    url = f'https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Función para obtener las competiciones, año, y detalles de cada partido
def get_match_details(matches_data):
    matches_info = []

    for match in matches_data:
        match_id = match['match_id']
        competition_name = match['competition']['competition_name']
        season = match['season']['season_name']
        home_team = match['home_team']['home_team_name']
        away_team = match['away_team']['away_team_name']
        home_score = match['home_score']
        away_score = match['away_score']
        
        # Obtenemos los eventos para este partido en específico
        events_data = fetch_events_data(match_id)
        
        goals = []
        cards = []
        starting_lineups = {}

        for event in events_data:
            # Obtener alineación inicial (Starting XI)
            if event['type']['name'] == 'Starting XI':
                team_name = event['team']['name']
                lineup = [player['player']['name'] for player in event['tactics']['lineup']]
                starting_lineups[team_name] = lineup

            # Obtener goles (Shot con resultado "Goal")
            if event['type']['name'] == 'Shot' and event['shot']['outcome']['name'] == 'Goal':
                goals.append({
                    "scorer": event['player']['name'],
                    "team": event['team']['name'],
                    "minute": event['minute']
                })

            # Obtener tarjetas (Card event)
            if event['type']['name'] == 'Card':
                cards.append({
                    "player": event['player']['name'],
                    "team": event['team']['name'],
                    "card_type": event['card']['name'],
                    "minute": event['minute']
                })

        match_details = {
            "match_id": match_id,
            "competition_name": competition_name,
            "season": season,
            "home_team": home_team,
            "away_team": away_team,
            "home_score": home_score,
            "away_score": away_score,
            "starting_lineups": starting_lineups,
            "goals": goals,
            "cards": cards
        }

        matches_info.append(match_details)

    return matches_info

# Ruta para obtener todos los partidos con competición, año, resultado, alineación, goles y tarjetas
@app.route('/matches', methods=['GET'])
def matches():
    matches_data = fetch_matches_data()
    match_details = get_match_details(matches_data)
    return jsonify(match_details)

if __name__ == '__main__':
    app.run(debug=True)
