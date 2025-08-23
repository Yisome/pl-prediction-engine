import os #hide my api key grrrrr...
import requests
import pandas as pd
from dotenv import load_dotenv #you not getting it lol

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = "v3.football.api-sports.io"
BASE_URL = f"https://{API_HOST}"

endpoint = f'{BASE_URL}/fixtures'


headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': API_HOST
}

params = {
    'league': '39', # Prem ID
    'season': '2023'  #year
}

def get_data(url,headers, params):
    try:
        response = requests.get(url, headers=headers, params=params) #gets HTTP request
        response.raise_for_status() #exceptions for no good codes (200 300 valid)
        data = response.json()
        return data.get('response')

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

match_data = get_data(endpoint, headers, params)


#troubleshooting
if match_data:
    print(f" fetched {len(match_data)} matches.")
else:
    print("Failed fetch data. Probably api or url issue lol")


#process+store data

import sqlite3 #IDK what this does...   
#Apparently it is a lightweight disk based database -> not a seperate server process (reg sql has a seperate server for it) bc sqlite is file based while other standard sql are server based

if match_data:

    processed = []

    for fixture in match_data:
        #dic for seperat ficture data
        fixture_details = {
            'fixture_id': fixture['fixture']['id'],
            'date': fixture['fixture']['date'],
            'status': fixture['fixture']['status']['short'],
            'home_team': fixture['teams']['home']['name'],
            'away_team': fixture['teams']['away']['name'],
            'home_goals': fixture['goals']['home'],
            'away_goals': fixture['goals']['away'],
        }
        processed.append(fixture_details) #append the details of each fixture to processed
    
    #What this for loop is doing: scouring through all the fixtures in match data one by one and making a dictionary stored with the details of that fixture
    #once stored in a dic, we appeend it to processed

    #dataframe creation -> done this many in datamine Purdue projects
    df = pd.DataFrame(processed)

    connect = sqlite3.connect('pl_historical_data.db') #dont rly know what this does: essentialy making or connecting to a sqlite3 database under this name
    df.to_sql('fixtures', connect, if_exists='replace', index=False) #self explanatory

    connect.close()

    print("\nData successfully processed and saved to pl_historical_data.db")
    print("DataFrame Preview:")
    print(df.head())



