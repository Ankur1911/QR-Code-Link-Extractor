import React from 'react';
import { useLocation } from 'react-router-dom';

const ProcessedData = () => {
  const location = useLocation();
  const { data } = location.state || { data: {} };

  return (
    <div className="processed-data-container">
      <h2>Processed Data</h2>
      <pre className="processed-data-content">{typeof data === 'string' ? data : JSON.stringify(data, null, 2)}</pre>
      {/* <Link to="/links">Back to Links</Link> */}
    </div>
  );
};

export default ProcessedData;