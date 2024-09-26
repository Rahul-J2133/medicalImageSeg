import React, { useState, useEffect } from 'react';
import './App.css';
import FileUpload from './FileUpload';
import PythonComponent from './OpenCamera';
import InsightComponent from './InsightComponent';  // Import the new component

function App() {
  const [response, setResponse] = useState(null);

  const handleResponse = (responseData) => {
    console.log("Response from backend:", responseData);  // Debugging the response
    setResponse(responseData);
  };

  useEffect(() => {
    if (response) {
      console.log("Updated Response State:", response);  // Debugging state update
    }
  }, [response]);

  return (
    <div className="App">
      <h1>MEDICAL IMAGE SEGMENTATION</h1>
      <h1>Get your X-RAY testified</h1>

      {/* File Upload Component */}
      <FileUpload onResponse={handleResponse} />
      
      {/* Python Script for Opening Camera */}
      <PythonComponent onResponse={handleResponse} />

      {/* Response Display */}
      {response && (
        <div className="response-container">
          <h3>Response</h3>
          <div>X-RAY TEST RESULT: {response.result}</div>
          <div>PROBABILITY: {response.probability}</div>

          {/* Conditional display of combined image */}
          {response.result === "INFECTED" && response.combined_img_base64 ? (
            <div className="infected-container">
              <h4>Combined Image (Infected):</h4>
              <img
                src={`data:image/jpeg;base64,${response.combined_img_base64}`}
                alt="Infected Area Highlighted"
                style={{ maxWidth: '100%', height: 'auto' }}  // Ensure image is properly visible
              />
              
              {/* Use the new InsightComponent here */}
              {/* <InsightComponent /> */}
            </div>
          ) : (
            <p>No infected area detected, or image is unavailable.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
