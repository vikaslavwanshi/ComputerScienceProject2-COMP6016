import joblib
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

# Load the trained ML model (random forest in this case)
model = joblib.load('random_forest_model.pkl')

@app.route('/')
def home():
    return "Welcome to the ML Traffic Monitoring API"

# Route to handle incoming traffic data from the POX controller
@app.route('/process_traffic', methods=['POST'])
def process_traffic():
    try:
        # Parse the incoming JSON traffic data
        traffic_data = request.json
        logging.debug(f'Received traffic data: {traffic_data}')
        
        # Convert the traffic data into a format suitable for the ML model
        df = pd.DataFrame([traffic_data])
        
        # Ensure columns are ordered correctly
        df = df[['Timestamp', 'FIT101', 'LIT101', 'MV101', 'P101', 'P102', 'AIT201', 'AIT202', 'AIT203',
                 'FIT201', 'MV201', 'P201', 'P202', 'P203', 'P204', 'P205', 'P206', 'DPIT301', 'FIT301',
                 'LIT301', 'MV301', 'MV302', 'MV303', 'MV304', 'P301', 'P302', 'AIT401', 'AIT402', 'FIT401',
                 'LIT401', 'P401', 'P402', 'P403', 'P404', 'UV401', 'AIT501', 'AIT502', 'AIT503', 'AIT504',
                 'FIT501', 'FIT502', 'FIT503', 'FIT504', 'P501', 'P502', 'PIT501', 'PIT502', 'PIT503',
                 'FIT601', 'P601', 'P602', 'P603', 'Normal/Attack']]  # Ensure all columns are present
        
        # Perform the prediction using the ML model
        prediction = model.predict(df)
        
        # Check if an attack is predicted (based on how the model is trained)
        if prediction[0] == 1:  # Assuming 1 means an attack
            message = "Attack detected! Real-time traffic anomaly."
        else:
            message = "No attack detected. Traffic is normal."
        
        # Return the result as JSON
        return jsonify({'message': message, 'prediction': int(prediction[0])})

    except Exception as e:
        logging.error(f'Error processing traffic data: {str(e)}')
        return jsonify({'error': str(e)}), 400