import React, { useState, useEffect } from 'react';
import './App.css';
import FileUpload from './FileUpload';
import PythonComponent from "./OpenCamera";

function App() {
  const [response, setResponse] = useState(null);

  const handleResponse = (responseData) => {
    setResponse(responseData);
  };

  useEffect(() => {
    if (response) {
      console.log(response);
    }
  }, [response]);

  return (
    <div className="App">
      <h1 style={{ textDecoration: "underline" }}>MEDICAL IMAGE SEGMENTATION</h1>
      <h1>Get your X-RAY testified</h1>
      <FileUpload onResponse={handleResponse} />
      <PythonComponent onResponse={handleResponse} />
      {/* Display response and image if response is not null */}
      {response && (
        <div className="response-container">
          <h3>Response</h3>
          <div>{response.result}</div>
          <div>Probability: {response.probability}</div>
          </div>
      )}
    </div>
  );
}

export default App;
