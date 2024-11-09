import React, { useEffect, useState } from 'react';

const LogDisplay = () => {
  const [logs, setLogs] = useState(''); // State to store logs
  const [error, setError] = useState(null); // State to store any errors

  // Function to fetch logs from the backend
  const fetchLogs = async () => {
    try {
      const response = await fetch('http://localhost:8001/logs');  // Ensure the correct port here
      if (response.ok) {
        const logData = await response.json(); // Expecting JSON response with 'logs' key
        setLogs(logData.logs.join('\n')); // Join logs array with new lines
      } else {
        console.error('Failed to fetch logs:', response.statusText);
        setError('Failed to fetch logs.');
      }
    } catch (error) {
      console.error('Error fetching logs:', error);
      setError('Error fetching logs.');
    }
  };

  useEffect(() => {
    // Fetch logs when the component mounts
    fetchLogs();

    // Fetch logs every 10 seconds
    const intervalId = setInterval(fetchLogs, 10000); // Adjust the interval timing as per your requirement

    return () => clearInterval(intervalId); // Cleanup interval on component unmount
  }, []);

  return (
    <div>
      <h2>Traffic Logs</h2>
      {error && <div className="alert alert-danger">{error}</div>}
      <pre>{logs}</pre> {/* <pre> tag ensures proper formatting */}
    </div>
  );
};

export default LogDisplay;