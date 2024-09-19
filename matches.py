def get_match_rivals(match_data):
    home_team = match_data['home_team']['home_team_name']
    away_team = match_data['away_team']['away_team_name']
    return home_team, away_team

def get_match_result(match_data):
    home_score = match_data['home_score']
    away_score = match_data['away_score']
    return home_score, away_score
