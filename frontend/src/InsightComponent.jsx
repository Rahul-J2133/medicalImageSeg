import React, { useState } from 'react';
import './InsightComponent.css'

function InsightComponent({ onSubmit }) {
  const [textInput, setTextInput] = useState(''); // State to hold the user input text
  const [insightResponse, setInsightResponse] = useState(''); // State to hold the response from backend

  // Update text input state when user types in the textarea
  const handleTextInputChange = (e) => {
    setTextInput(e.target.value);
  };

  // Handle form submission
  const handleSubmit = async () => {
    try {
      const res = await fetch('http://localhost:8000/insights', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ insight_text: textInput }),  // Send text input to backend
      });

      const data = await res.json();
      setInsightResponse(data.insight);  // Assuming the response contains an "insight" field

      if (onSubmit) {
        onSubmit(data.insight);  // Call parent onSubmit function if passed
      }
    } catch (error) {
      console.error("Error sending text to insights endpoint:", error);
    }
  };

  return (
    <div className="insight-component">
      {/* Textarea for user input */}
      <textarea
        value={textInput}
        onChange={handleTextInputChange}
        placeholder="Enter your insights here..."
        style={{width: '100%', height: '100px' }}
      />
      
      {/* Submit button */}
      <button onClick={handleSubmit}>Submit Insight</button>

      {/* Display the response from backend */}
      {insightResponse && (
        <div className="insight-response">
          <h4>Insight Response:</h4>
          <pre>{insightResponse}</pre>
        </div>
      )}
    </div>
  );
}

export default InsightComponent;
