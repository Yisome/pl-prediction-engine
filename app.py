import joblib
import pandas as pd
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS # <--- ADD THIS LINE
import os
import sys

# Create the Flask application instance
app = Flask(__name__)
CORS(app) # <--- ADD THIS LINE

# Load the trained model and scaler
try:
    model = joblib.load('pl_model.pkl')
    scaler = joblib.load('pl_scaler.pkl')
except FileNotFoundError:
    print("Error: Model or scaler file not found. Please run model.py first.", file=sys.stderr)
    sys.exit(1)

# Define the features that our model was trained on
features = ['goal_diff', 'shot_diff', 'red_card_diff']

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# This is the prediction endpoint. It accepts a POST request.
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        print(f"Received data from request: {data}", file=sys.stderr)
        print(f"Type of data: {type(data)}", file=sys.stderr)

        if not all(key in data for key in features):
            print("Error: Missing keys in data.", file=sys.stderr)
            return jsonify({'error': 'Missing data in request'}), 400

        live_stats_raw = pd.DataFrame([data])
        live_stats_raw = live_stats_raw[features]
        live_stats_scaled = scaler.transform(live_stats_raw)
        win_probability = model.predict_proba(live_stats_scaled)[0][1]

        print(f"Prediction successful, probability: {win_probability}", file=sys.stderr)
        return jsonify({'win_probability': float(win_probability)})

    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    app.run(debug=True)