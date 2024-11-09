import React from 'react';

const ResultDisplay = ({ result, trafficData }) => {
  return (
    <div className="result-display mt-4">
      {result && (
        <div className="alert alert-info">
          <h4>Prediction Result</h4>
          <p>{result.message}</p>
          <p>Prediction: {result.prediction}</p>
        </div>
      )}
      {trafficData && (
        <div className="alert alert-warning">
          <h4>Traffic Data Received</h4>
          <p>{trafficData.message}</p>
        </div>
      )}
    </div>
  );
};

export default ResultDisplay;
