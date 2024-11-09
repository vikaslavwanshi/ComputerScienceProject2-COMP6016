import React from 'react';

const ResultDisplay = ({ result }) => {
  return (
    <div>
      <h2>Observations:</h2>
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  );
};

export default ResultDisplay;
