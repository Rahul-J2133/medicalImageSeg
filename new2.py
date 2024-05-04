from keras.models import load_model
import cv2
import numpy as np
from PIL import Image
import random

# Load the trained model
model = load_model('pneumonia_pred_new.h5')
def displayImages(raw_image, infected_image):
    # Define a fixed size for the display window
    max_width = 800
    max_height = 600

    raw_height, raw_width, _ = raw_image.shape
    infected_height, infected_width, _ = infected_image.shape

    # Calculate the scale factor to fit the images within the maximum size
    raw_scale = min(max_width / raw_width, max_height / raw_height)
    infected_scale = min(max_width / infected_width, max_height / infected_height)

    # Resize images
    raw_resized = cv2.resize(raw_image, None, fx=raw_scale, fy=raw_scale)
    infected_resized = cv2.resize(infected_image, None, fx=infected_scale, fy=infected_scale)

    # Combine images horizontally
    combined_image = np.hstack((raw_resized, infected_resized))
    print("processed to be displayed")

    # Display the combined image
    cv2.imshow('Raw and Infected Images', combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def displayInfected(image):
    selected_color = (153, 153, 153)

    # Define a tolerance range for color selection (e.g., +/- 10)
    tolerance = 10

    # Define the lower and upper bounds based on the selected color and tolerance
    lower_bound = np.array([selected_color[0] - tolerance, selected_color[1] - tolerance, selected_color[2] - tolerance])
    upper_bound = np.array([selected_color[0] + tolerance, selected_color[1] + tolerance, selected_color[2] + tolerance])

    # Threshold the image to find regions with the selected color
    mask = cv2.inRange(image, lower_bound, upper_bound)

    # Find contours of the regions
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Find the center of mass (centroid) of the largest contour
    M = cv2.moments(largest_contour)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    # Generate a random radius within a certain range
    min_radius = 200
    max_radius = 250
    radius = random.randint(min_radius, max_radius)

    color = (0,0,0)

    # Create a copy of the original image
    image_copy = image.copy()

    # Draw the circle around the largest contour on the copy
    cv2.circle(image_copy, center, radius, color, 4) 
    print("encircled image about to be returned") 

    return image_copy
def preprocess_image(image):
    print("preprocess")
    # Convert PIL Image to numpy array
    img_array = np.array(image)
    # Resize image to 64x64
    resized_img = cv2.resize(img_array, (64, 64))
    # Convert image to RGB (if grayscale)
    if len(resized_img.shape) == 2:
        resized_img = cv2.cvtColor(resized_img, cv2.COLOR_GRAY2RGB)
    # Normalize pixel values
    normalized_img = resized_img / 255.0
    # Add batch dimension
    processed_img = np.expand_dims(normalized_img, axis=0)
    return processed_img

def handler(image: Image.Image):    
    print("handler")
    processed_img = preprocess_image(image)
    # Make prediction
    prediction = model.predict(processed_img)

    # Convert probabilities to class labels
    if prediction > 0.5:
        result = "INFECTED"
    else:
        result = "NORMAL"

    # Print the prediction result
    print("------------PREDICTION--------------")
    print("PNEUMONIA TEST RESULT:", result)
    print(f"Probability: {prediction[0][0]*100} %")
    print("------------------------------------")

    if result == "INFECTED":
        # Get infected image
        infected_image = displayInfected(np.array(image))
        # Display both images
        print("about to be displayed")
        displayImages(np.array(image), np.array(infected_image))
    return {"result": f"X-RAY TEST RESULT : {result}",
            "probability": f"{prediction[0][0]*100} %"}

