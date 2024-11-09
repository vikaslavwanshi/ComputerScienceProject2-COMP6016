import os
import pandas as pd
import requests
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
import subprocess

# Clear previous Mininet instances
def clear_mininet():
    subprocess.call(['sudo', 'mn', '-c'])
    print("Cleared previous Mininet configurations.")

def inject_traffic(dataset):
    dataset['FIT101'] = dataset['FIT101'].astype(object)
    attack_host = 'FIT101'
    attack_command = "'; DROP TABLE SensorData; --"
    dataset.loc[dataset['Timestamp'] == attack_host, 'FIT101'] = attack_command

    print(f"SQL injection attack sent to host {attack_host}")

    dataset_file_path = 'modified_SWaT_Dataset.csv'
    dataset.to_csv(dataset_file_path, index=False)

    url = "http://localhost:8001/simulate_attack"
    try:
        with open(dataset_file_path, 'rb') as f:
            files = {'dataset_file': f}
            response = requests.post(url, files=files)
            if response.status_code == 200:
                print(f"SQL Injection attack reported to backend: {response.json()}")
            else:
                print(f"Failed to report SQL Injection attack to backend. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error in sending request to Flask backend: {e}")

def perform_dos_attack(net, target_host):
    target_host = net.get(target_host)
    print(f"Starting DoS attack on {target_host}...")
    target_host.cmd("ping -f -c 20 127.0.0.1")  # Use flood ping within Mininet for simulation
    print(f"Completed DoS attack on {target_host}.")

def perform_mitm_attack(src_host_name, dest_host_name):
    print(f"Starting MITM attack between {src_host_name} and {dest_host_name}...")
    print(f"Intercepting traffic between {src_host_name} and {dest_host_name}...")
    print(f"Completed MITM attack between {src_host_name} and {dest_host_name}.")

def create_topology(dataset):
    net = Mininet(controller=None, switch=OVSSwitch)
    s1 = net.addSwitch('s1')
    sensors = ['FIT101', 'LIT101']
    actuators = ['MV101', 'P101']
    for sensor in sensors:
        net.addHost(sensor)
    for actuator in actuators:
        net.addHost(actuator)
    for sensor in sensors:
        net.addLink(sensor, s1)
    for actuator in actuators:
        net.addLink(actuator, s1)

    net.start()
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6637)
    c0.start()
    s1.start([c0])

    inject_traffic(dataset)
    perform_dos_attack(net, 'FIT101')
    perform_mitm_attack('FIT101', 'LIT101')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    # Clear Mininet
    clear_mininet()

    # Load the dataset and define column names
    dataset = pd.read_csv('modified_SWaT_Dataset.csv', skiprows=1)
    dataset.columns = ['Timestamp', 'FIT101', 'LIT101', 'MV101', 'P101', 'P102', 'AIT201', 'AIT202', 'AIT203',
                       'FIT201', 'MV201', 'P201', 'P202', 'P203', 'P204', 'P205', 'P206', 'DPIT301', 'FIT301',
                       'LIT301', 'MV301', 'MV302', 'MV303', 'MV304', 'P301', 'P302', 'AIT401', 'AIT402', 'FIT401',
                       'LIT401', 'P401', 'P402', 'P403', 'P404', 'UV401', 'AIT501', 'AIT502', 'AIT503', 'AIT504',
                       'FIT501', 'FIT502', 'FIT503', 'FIT504', 'P501', 'P502', 'PIT501', 'PIT502', 'PIT503',
                       'FIT601', 'P601', 'P602', 'P603', 'Normal/Attack']

    # Run topology and attacks
    create_topology(dataset)