import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib

connect = sqlite3.connect('pl_historical_data.db')
df = pd.read_sql_query("SELECT * FROM fixtures", connect)
connect.close()

#data cleaning
df.dropna(subset=['home_goals', 'away_goals', 'home_shots', 'away_shots', 'home_red_cards', 'away_red_cards'], inplace=True)
df['home_win'] = (df['home_goals'] > df['away_goals']).astype(int)

#additional stats: goal diff, shot diff, red card diff
df['goal_diff'] = df['home_goals'] - df['away_goals']
df['shot_diff'] = df['home_shots'] - df['away_shots']
df['red_card_diff'] = df['home_red_cards'] - df['away_red_cards']

#twaining
features = ['goal_diff', 'shot_diff', 'red_card_diff']
X = df[features]
y = df['home_win']

# scaling the features of the 3 I included, figures out the avg distribution between them and scales it between 0 to 1
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


#80% training 20% testing
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
print(f"Training size: {len(X_train)}")
print(f"Testing size: {len(X_test)}")


model = LogisticRegression()
model.fit(X_train, y_train)


#testing this out
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"\nModel Accuracy on Test Data: {accuracy:.2f}")

# The example live stats now include the 'features' list to prevent the UserWarning
live_stats = pd.DataFrame([{'goal_diff': 0, 'shot_diff': 7, 'red_card_diff': 0}], columns=features)


#scaling live data
live_stats_scaled = scaler.transform(live_stats)

# The model's prediction is the probability of a home team win
probability_of_win = model.predict_proba(live_stats_scaled)[0][1]
print(f"\nWin probability for example scenario: {probability_of_win:.2f}")
#sving the model and scaler
joblib.dump(model, 'pl_model.pkl')
joblib.dump(scaler, 'pl_scaler.pkl')