import requests

# URL de GitHub
BASE_URL = 'https://raw.githubusercontent.com/statsbomb/open-data/master/data/'

def fetch_matches_data():
    url = f'{BASE_URL}matches/43/3.json'
    response = requests.get(url)
    return response.json()

def fetch_events_data(match_id):
    url = f'{BASE_URL}events/{match_id}.json'
    response = requests.get(url)
    return response.json()
