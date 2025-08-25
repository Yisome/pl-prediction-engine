import sqlite3
import pandas as pd

csv_name = '2021-2022.csv'
database_name = 'pl_historical_data.db'


try:
    df = pd.read_csv(csv_name)
    print(f"Successfully loaded {len(df)} rows of data from {csv_name}")
    print("Original DataFrame columns:", df.columns.tolist())


    column_mapping = {
        'HomeTeam': 'home_team',
        'AwayTeam': 'away_team',
        'FTHG': 'home_goals',
        'FTAG': 'away_goals',
        'HS': 'home_shots',
        'AS': 'away_shots',
        'HC': 'home_corners',
        'AC': 'away_corners',
        'HR': 'home_red_cards',
        'AR': 'away_red_cards'
    }

    df.rename(columns=column_mapping, inplace=True) #renaming the columns since its kind of hard to read with the original col names

    #safe guard: js making sure all the columns are in place
    required_columns = ['home_goals', 'away_goals', 'home_shots', 'away_shots', 'home_red_cards', 'away_red_cards']
    for col in required_columns:
        if col not in df.columns:
            df[col] = 0
            print("{col} not find. Value is set to 0")

    #null the rows that dont have data
    df.dropna(subset=required_columns, inplace=True)


    #convert red cards to a integer format.
    for col in ['home_red_cards', 'away_red_cards']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    

    con = sqlite3.connect(database_name)

    df.to_sql('fixtures', con, if_exists='replace', index=False)

    con.close()
    
    print("\nData successfully processed and saved to a local database.")
    print("Database columns saved:", df.columns.tolist())
    print("DataFrame Preview:")
    print(df[['home_team', 'away_team', 'home_goals', 'away_goals', 'home_shots', 'away_shots', 'home_red_cards', 'away_red_cards']].tail())
    
except FileNotFoundError:
    print(f"Error: The file '{csv_name}' was not found. Please download the dataset and place it in your project folder.")

