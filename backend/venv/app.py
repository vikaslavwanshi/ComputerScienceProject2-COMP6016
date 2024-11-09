import subprocess
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import tempfile
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mn_traffic_injection import perform_dos_attack, perform_mitm_attack 

# Configuration for logging
logging.basicConfig(level=logging.INFO, filename='traffic_log.txt',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='a', force=True)


app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

model = joblib.load('random_forest_model.pkl')

def start_service(command):
    """Start a service using subprocess."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr

@app.route('/start_pox', methods=['POST'])
def start_pox():
    try:
        command = [
            "/home/vikas/Downloads/pox/pox/pox.py", 
            "log.level", 
            "--DEBUG", 
            "openflow.of_01", 
            "--port=6637", 
            "pox_controller"
        ]
        return_code, stdout, stderr = start_service(command)
        if return_code == 0:
            return jsonify({"message": "POX controller started"}), 200
        else:
            logging.error(f"Failed to start POX controller: {stderr.decode()}")
            return jsonify({"error": "Failed to start POX controller"}), 500
    except Exception as e:
        logging.error(f"Exception in starting POX controller: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/start_ml_server', methods=['POST'])
def start_ml_server():
    try:
        command = [
            "/home/vikas/Downloads/Project-comp6016/COMP6016_project2/backend/venv/bin/gunicorn", 
            "--bind", "0.0.0.0:5003", "ml_server:app"
        ]
        return_code, stdout, stderr = start_service(command)
        if return_code == 0:
            return jsonify({"message": "ML server started"}), 200
        else:
            logging.error(f"Failed to start ML server: {stderr.decode()}")
            return jsonify({"error": "Failed to start ML server"}), 500
    except Exception as e:
        logging.error(f"Exception in starting ML server: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/start_backend', methods=['POST'])
def start_backend():
    try:
        command = [
            "/home/vikas/Downloads/Project-comp6016/COMP6016_project2/backend/venv/bin/gunicorn", 
            "--bind", "0.0.0.0:8001", "--timeout", "300", "app:app"
        ]
        return_code, stdout, stderr = start_service(command)
        if return_code == 0:
            return jsonify({"message": "Backend server started"}), 200
        else:
            logging.error(f"Failed to start backend server: {stderr.decode()}")
            return jsonify({"error": "Failed to start backend server"}), 500
    except Exception as e:
        logging.error(f"Exception in starting backend server: {str(e)}")
        return jsonify({"error": str(e)}), 500

def inject_traffic_with_sudo(dataset_file_path):
    # Run 'mn -c' to clear previous Mininet configurations
    cleanup_result = subprocess.run(['sudo', 'mn', '-c'], capture_output=True, text=True)
    if cleanup_result.returncode != 0:
        logging.error(f"Mininet cleanup failed: {cleanup_result.stderr}")
        raise Exception("Failed to clean Mininet environment.")
    else:
        logging.info("Mininet environment cleaned successfully.")

    # Run the main Mininet script
    script_path = "/home/vikas/Downloads/Project-comp6016/COMP6016_project2/backend/venv/mn_traffic_injection.py"
    command = ['sudo', 'python3', script_path, dataset_file_path]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        logging.info("Mininet script executed successfully. SQL Injection simulated.")
    else:
        logging.error(f"Mininet script failed: {result.stderr}")
        raise Exception("Failed to simulate attack. Please check logs for details.")

@app.route('/simulate_attack', methods=['POST'])
def simulate_attack():
    try:
        attack_type = request.form.get('attack_type')
        target_host = request.form.get('target_host')

        if attack_type == "SQL Injection":
            dataset_file = request.files['dataset_file']
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                dataset_file.save(temp_file.name)
                inject_traffic_with_sudo(temp_file.name)

            logging.info('SQL Injection Attack simulated in Mininet.')
            return jsonify({'message': 'SQL Injection Attack simulated in Mininet'}), 200
        
        elif attack_type == "DoS":
            # Make sure to pass the target_host to the function
            perform_dos_attack(target_host)  # Pass the target host name here
            logging.info(f"DoS attack simulated on {target_host}.")
            return jsonify({'message': f'DoS attack simulated on {target_host}'}), 200
        
        elif attack_type == "MITM":
            perform_mitm_attack('FIT101', 'LIT101')
            logging.info("MITM attack simulated between FIT101 and LIT101.")
            return jsonify({'message': 'MITM attack simulated between FIT101 and LIT101'}), 200
        else:
            return jsonify({'error': 'Invalid attack type'}), 400

    except Exception as e:
        logging.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 400


@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        with open('traffic_log.txt', 'r') as log_file:
            logs = log_file.read().splitlines()
        return jsonify({'logs': logs}), 200
    except Exception as e:
        logging.error(f'Error reading log file: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "Welcome to the Backend API"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
