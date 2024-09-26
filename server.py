from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse  # To send JSON responses
import base64
import io
from PIL import Image  # For handling image files
import cv2  # For image processing with OpenCV
import new2  # Importing the logic from the `new2.py` file
import google.generativeai as genai


# Create an instance of the FastAPI class
app = FastAPI()


def setCameraUrl(camera_ip, camera_port):

    # URL of the camera feed
    return f"http://{camera_ip}:{camera_port}/video"


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


def generateResponse(result):
    # If CombinedImg is included, encode it to base64
    response_data = {"result": result["result"], "probability": result["probability"]}

    if result["CombinedImg"] is not None:
        combined_img_base64 = new2.encode_image_to_base64(result["CombinedImg"])
        response_data["combined_img_base64"] = combined_img_base64
        print("not none")
    return response_data


# Define a route handler for the root endpoint
@app.get("/")
async def read_root():
    return {"message": "Hello, World"}


@app.get("/invokePython")
async def Cam(camera_ip: str, camera_port: str):
    print("reached")
    cap = cv2.VideoCapture(setCameraUrl(camera_ip, camera_port))

    if not cap.isOpened():
        raise HTTPException(status_code=500, detail="Error: Could not open camera.")

    while True:
        ret, frame = cap.read()
        if not ret:
            raise HTTPException(
                status_code=500, detail="Error: Could not read frame from camera."
            )
            break

        cv2.imshow("Camera Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord("s"):
            frame_saved = frame
            break

    cap.release()
    cv2.destroyAllWindows()

    result = new2.handler(frame_saved)

    response_data = generateResponse(result)

    return JSONResponse(content=response_data)


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))
        result = new2.handler(img)

        response_data = generateResponse(result)
        return JSONResponse(content=response_data)

    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post("/insights")
async def insights(insight_data: dict):
    text = insight_data.get("insight_text", "")

    prompt=f'''
You are a medical AI under professional medical use, tasked with assisting a medical professional by analyzing the following X-ray description and providing the possible medical conditions.

Desciption: "{text}. Specify the possible conditions"

Generate **no more than four** concise insights:
1. Summarize key findings from the X-ray.
2. Specify the potential medical conditions based on the findings.
3. Recommend further diagnostic steps or medical evaluations where necessary.

'''

    # insight_response = f"Insight based on the text: {text}"
    genai.configure(api_key="AIzaSyCs3jLFvt_cGWwQg1n1P9zxcpHKUK8xmik")
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    insight_response = model.generate_content(text)
    generatedResponse = insight_response.text

    lines = generatedResponse.splitlines()
    insight_output = "\n".join(lines[1:])

    return {"insight": insight_output}

# Run the server with uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
