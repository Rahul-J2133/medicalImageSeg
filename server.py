from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import base64
import io
from PIL import Image
import new2
import cv2

# Create an instance of the FastAPI class
app = FastAPI()

def setCameraUrl(camera_ip, camera_port):

    # URL of the camera feed
    return f'http://{camera_ip}:{camera_port}/video'

global frame_saved

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:5173",  # Add the origin of your React app
    # Add more origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Define a route handler for the root endpoint
@app.get("/")
async def read_root():
    return {"message": "Hello, World"}

@app.get("/invokePython")
async def Cam(camera_ip: str, camera_port: str):
# Open the camera feed
    print("reached")
    cap = cv2.VideoCapture(setCameraUrl(camera_ip, camera_port))

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    # Read and display frames from the camera feed
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from camera.")
            break
        
        cv2.imshow('Camera Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            frame_saved=frame
            break

    # Release the camera
    cap.release()
    cv2.destroyAllWindows()
    return new2.handler(frame_saved)
    

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))
        return new2.handler(img)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
# Run the server with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)