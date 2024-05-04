import cv2
import numpy as np
import random

# Load the X-ray Image
image = cv2.imread(r'C:\Users\RAHUL JETHWANI\OneDrive\Desktop\dataset\covid\1-s2.0-S0929664620300449-gr2_lrg-a.jpg')

# Define the color you want to select (e.g., (153, 153, 153))
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
max_radius = 300
radius = random.randint(min_radius, max_radius)

color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Draw the circle around the largest contour
cv2.circle(image, center, radius, color, 2)  # Green color (BGR: 0, 255, 0)

# Create a blank canvas of constant size
constant_size = (800, 600)
canvas = np.zeros((constant_size[1], constant_size[0], 3), dtype=np.uint8)

# Calculate the scale factor to fit the entire image within the canvas
scale_factor = min(constant_size[0] / image.shape[1], constant_size[1] / image.shape[0])

# Resize the image with the calculated scale factor
resized_image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)

# Calculate the offset for centering the resized image on the canvas
offset_x = (constant_size[0] - resized_image.shape[1]) // 2
offset_y = (constant_size[1] - resized_image.shape[0]) // 2

# Paste the resized image onto the canvas
canvas[offset_y:offset_y+resized_image.shape[0], offset_x:offset_x+resized_image.shape[1]] = resized_image

# Display the result
cv2.imshow('Encircled the Infected segment', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
