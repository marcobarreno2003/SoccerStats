def get_lineups(events_data):
    lineups = {}
    
    for event in events_data:
        if event['type']['name'] == 'Starting XI':
            team_name = event['team']['name']
            lineup = []
            
            for player in event['tactics']['lineup']:
                player_name = player['player']['name']
                position = player['position']['name']
                jersey_number = player['jersey_number']
                lineup.append(f"{player_name} ({position}, {jersey_number})")
            
            lineups[team_name] = lineup
    
    return lineups
