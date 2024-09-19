from flask import app


@app.route('/competitions', methods=['GET'])
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
