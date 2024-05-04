import React, { useState } from 'react';

function PythonComponent({ onResponse }) {
    const [cameraIp, setCameraIp] = useState('');
    const [cameraPort, setCameraPort] = useState();

    const handleCameraIpChange = (event) => {
        setCameraIp(event.target.value);
    };

    const handleCameraPortChange = (event) => {
        setCameraPort(event.target.value);
    };

    const executePythonScript = () => {
        let url = `http://127.0.0.1:8000/invokePython?camera_ip=${encodeURIComponent(cameraIp)}&camera_port=${encodeURIComponent(cameraPort)}`;

        if (!cameraIp || !cameraPort) {
            url = `http://127.0.0.1:8000/invokePython?camera_ip=${encodeURIComponent("192.168.29.117")}&camera_port=${encodeURIComponent(4747)}`;
        };

        fetch(url, {
            method: 'GET',
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Response from server:', data);
            // Pass response data to parent component
            onResponse(data);
        })
        .catch(error => {
            console.error('There was a problem with the request:', error);
        });
    };

    return (
        <div>
            <input type="text" placeholder="Camera IP" value={cameraIp} onChange={handleCameraIpChange} />
            <br/>
            <input type="text" placeholder="Camera Port" value={cameraPort} onChange={handleCameraPortChange} />
            <br/>
            <button onClick={executePythonScript}>Open Camera</button>
            <br/>
        </div>
    );
}

export default PythonComponent;
