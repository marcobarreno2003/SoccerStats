import requests

# Function to get match data from the API
def get_matches(api_key, league_id, season, date_from, date_to):
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

    # Print the entire response to see what is being returned
    print(f"API Response Status: {response.status_code}")
    
    # Check for errors in the response
    if response.status_code != 200:
        print(f"Error: {data['message'] if 'message' in data else 'Unknown error'}")
        return []

    print(f"Full API Response: {data}")
    
    if 'response' in data and len(data['response']) > 0:
        return data['response']
    else:
        print("No match data available for the given parameters.")
        return []
