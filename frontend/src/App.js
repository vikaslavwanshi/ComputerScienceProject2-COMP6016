import React, { useState, useEffect } from 'react';
import MyNavbar from './component/navbar';
import ProfileCover from './component/cover';
import LogDisplay from './component/LogDisplay';
import 'bootstrap/dist/css/bootstrap.min.css';
import { FaBug, FaNetworkWired, FaShieldAlt } from 'react-icons/fa';

const App = () => {
  const [logs, setLogs] = useState('');
  const [error, setError] = useState(null);
  const [attackStatus, setAttackStatus] = useState({}); 

  const handleStartService = async (serviceType) => {
    let endpoint;
    switch (serviceType) {
      case "POX":
        endpoint = 'http://localhost:8001/start_pox';
        break;
      case "ML Server":
        endpoint = 'http://localhost:8001/start_ml_server';
        break;
      case "Backend":
        endpoint = 'http://localhost:8001/start_backend';
        break;
      default:
        return;
    }

    try {
      const response = await fetch(endpoint, { method: 'POST' });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Unknown error occurred');
      }
      alert(data.message);
    } catch (error) {
      console.error(`Error starting ${serviceType}:`, error);
      alert(`Failed to start ${serviceType}: ${error.message}`);
    }
  };

  const handleAttack = async (attackType) => {
    const formData = new FormData();
    const datasetFile = new Blob(["Your dataset contents here"], { type: 'text/csv' });

    if (attackType === "SQL Injection") {
      formData.append('dataset_file', datasetFile, 'modified_SWaT_Dataset.csv');
    }
    formData.append('attack_type', attackType);
    formData.append('target_host', 'FIT101');

    try {
      const response = await fetch('http://localhost:8001/simulate_attack', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setLogs((prevLogs) => prevLogs + '\n' + data.message);
        setAttackStatus({ ...attackStatus, [attackType]: 'success' });
      } else {
        setError('Failed to trigger the attack simulation.');
        setAttackStatus({ ...attackStatus, [attackType]: 'failed' });
      }
    } catch (error) {
      setError('Error occurred while connecting to backend.');
      setAttackStatus({ ...attackStatus, [attackType]: 'failed' });
      console.error(error);
    }
  };

  useEffect(() => {
    const intervalId = setInterval(async () => {
      try {
        const response = await fetch('http://localhost:8001/logs');
        const data = await response.json();
        setLogs(data.logs.join('\n'));
      } catch (error) {
        setError('Error fetching logs.');
        console.error(error);
      }
    }, 10000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div>
      <MyNavbar />
      <ProfileCover />
      <div className="container">
        <h1>Mininet Traffic Simulation</h1>
        <p className="text-muted">Choose an attack type below to simulate traffic anomalies or start services.</p>

        {/* Service and Attack Buttons in Two Columns */}
        <div className="row">
          {/* Service Buttons Column */}
          <div className="col-md-6">
            <h4>Service Controls</h4>
            <div className="d-flex flex-column mb-3">
              <button
                onClick={() => handleStartService("POX")}
                className="btn btn-outline-primary mb-2"
              >
                Start POX Controller
              </button>
              <button
                onClick={() => handleStartService("ML Server")}
                className="btn btn-outline-secondary mb-2"
              >
                Start ML Server
              </button>
              <button
                onClick={() => handleStartService("Backend")}
                className="btn btn-outline-success mb-2"
              >
                Start Backend Server
              </button>
            </div>
          </div>

          {/* Attack Buttons Column */}
          <div className="col-md-6">
            <h4>Attack Simulations</h4>
            <div className="d-flex flex-column mb-3">
              <button
                onClick={() => handleAttack("SQL Injection")}
                className={`btn ${attackStatus["SQL Injection"] === 'failed' ? 'btn-danger' : 'btn-outline-danger'} mb-2`}
              >
                <FaBug className="me-2" /> Trigger SQL Injection
              </button>
              <button
                onClick={() => handleAttack("DoS")}
                className={`btn ${attackStatus["DoS"] === 'failed' ? 'btn-warning' : 'btn-outline-warning'} mb-2`}
              >
                <FaNetworkWired className="me-2" /> Trigger DoS Attack
              </button>
              <button
                onClick={() => handleAttack("MITM")}
                className={`btn ${attackStatus["MITM"] === 'failed' ? 'btn-info' : 'btn-outline-info'} mb-2`}
              >
                <FaShieldAlt className="me-2" /> Trigger MITM Attack
              </button>
            </div>
          </div>
        </div>

        {error && <div className="alert alert-danger mt-3">{error}</div>}

        <h3 className="mt-4">Traffic Alerts</h3>
        <div className="logs-container p-3 border rounded" style={{ height: '500px', overflowY: 'scroll' }}>
          <LogDisplay logs={logs} />
        </div>
      </div>
    </div>
  );
};

export default App;