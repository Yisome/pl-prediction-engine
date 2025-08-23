import pandas as pd
import sqlite3

connect = sqlite3.connect('pl_historical_data.db')

df = pd.read_sql_query("SELECT * FROM fixtures", connect) #I only know what this does because a year ago I was confused on how to do stuff ina sql database.
#basically just reading the entire fixtures table to a DF

connect.close()
#troubleshoot
print(f"Loaded {len(df)} fixture")
print(df.head())

#data cleaning

df.dropna(subset=['home_goals','away_goals'], inplace=True) #drops all the null goals rows


