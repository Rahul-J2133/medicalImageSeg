import React, { useState } from 'react';

function FileUpload({ onResponse }) {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append('file', selectedFile);
  
      fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        body: formData
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        // console.log('File uploaded successfully:', data);
        // Pass response data to parent component
        onResponse(data);
      })
      .catch(error => {
        console.error('There was a problem uploading the file:', error);
      });
    } else {
      console.error('No file selected');
    }
  };
  

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <br/>
      <button onClick={handleUpload}>Upload</button>
      <br/><br/><br/>
    </div>
  );
}

export default FileUpload;
