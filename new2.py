from keras.models import load_model
import base64
import cv2
import numpy as np
from PIL import Image
import random

# Load the trained model
model = load_model(r'C:\Users\RAHUL JETHWANI\OneDrive\Desktop\Matlab\medicalImageSeg\pneumonia_pred_self.h5')
def displayImages(raw_image, infected_image):

    # Define a fixed size for the display window
    max_width = 800
    max_height = 600

    raw_height, raw_width, _ = raw_image.shape
    infected_height, infected_width, _ = infected_image.shape

    # Calculate the scale factor to fit the images within the maximum size
    raw_scale = min(max_width / raw_width, max_height / raw_height)
    infected_scale = min(max_width / infected_width, max_height / infected_height)

    print("being processed to be displayed")
    # Resize images
    raw_resized = cv2.resize(raw_image, None, fx=raw_scale, fy=raw_scale)
    infected_resized = cv2.resize(infected_image, None, fx=infected_scale, fy=infected_scale)

    # Combine images horizontally
    combined_image = np.hstack((raw_resized, infected_resized))
    print("processed to be displayed")

    return combined_image

def displayInfected(image):
    selected_color = (153, 153, 153)
    tolerance = 10

    # Define the lower and upper bounds based on the selected color and tolerance
    lower_bound = np.array([selected_color[0] - tolerance, selected_color[1] - tolerance, selected_color[2] - tolerance])
    upper_bound = np.array([selected_color[0] + tolerance, selected_color[1] + tolerance, selected_color[2] + tolerance])

    print("Lower Bound:", lower_bound)
    print("Upper Bound:", upper_bound)

    # Check the input image
    print("Image shape:", image.shape)
    print("Image dtype:", image.dtype)

    # Threshold the image to find regions with the selected color
    mask = cv2.inRange(image, lower_bound, upper_bound)
    
    print("Mask created.")
    print("Mask shape:", mask.shape)
    print("Unique values in mask:", np.unique(mask))

    # Check if any areas matched
    if cv2.countNonZero(mask) == 0:
        print("No areas matched the selected color.")
        return image  # Handle accordingly

    print("Finding contours")

    # Find contours of the regions
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contours were found
    if len(contours) == 0:
        print("No contours found.")
        return image  # Handle accordingly

    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Find the center of mass (centroid) of the largest contour
    M = cv2.moments(largest_contour)
    if M["m00"] == 0:  # Prevent division by zero
        print("Moment calculation failed.")
        return image

    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    # Generate a random radius within a certain range
    min_radius = 200
    max_radius = 250
    radius = random.randint(min_radius, max_radius)

    color = (0, 0, 0)

    # Create a copy of the original image
    image_copy = image.copy()

    # Draw the circle around the largest contour on the copy
    cv2.circle(image_copy, center, radius, color, 4)
    print("Encircled image about to be returned")

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

# Utility function to encode image to base64
def encode_image_to_base64(image):
    # Encode the image as a JPEG in memory
    success, buffer = cv2.imencode('.jpg', image)  
    if success:
        img_str = base64.b64encode(buffer).decode('utf-8')  # Convert to base64 string
        return img_str
    else:
        raise ValueError("Could not encode the image to base64.")

def handler(image: Image.Image):    
    print("handler")
    processed_img = preprocess_image(image)
    prediction = model.predict(processed_img)

    if prediction > 0.5:
        result = "INFECTED"
        print(result)

        # Convert PIL image to NumPy array in BGR format for OpenCV
        img_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Get infected image
        infected_image = displayInfected(img_bgr)  # Pass the converted image
        print("encircled")

        img_filename = 'IMG.jpg'  # Define the filename
        cv2.imwrite(img_filename, np.array(infected_image))  # Save the image as IMG.jpg

        # Generate the combined image
        CombinedImg = displayImages(np.array(img_bgr), np.array(infected_image))
        
    else:
        result = "NORMAL"
        CombinedImg = None  # No combined image for NORMAL cases

    print("------------PREDICTION--------------")
    print("PNEUMONIA TEST RESULT:", result)
    print(f"Probability: {prediction[0][0]*100} %")
    print("------------------------------------")

    return {
        "result": f"{result}",
        "probability": f"{prediction[0][0]*100} %",
        "CombinedImg": CombinedImg  # This will be None if result is NORMAL
    }
