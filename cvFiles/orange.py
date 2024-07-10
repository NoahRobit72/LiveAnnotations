import cv2
import numpy as np
import time
from datetime import date
 
# Returns the current local date
# Define the range of orange color in HSV
lower_green = np.array([35, 50, 50])
upper_green = np.array([85, 255, 255])

f = open("dataFile.txt", "w")
today = date.today()
f.write(str(today))
f.close()

# Initialize the video capture object
cap = cv2.VideoCapture(0)  # Use 0 for webcam, or replace with video file path

if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()
    
fappend = open("dataFile.txt", "a")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the orange color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # If any contours are found
    if contours:
        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        
        area = cv2.contourArea(largest_contour)
        
        # Calculate the moments of the largest contour
        M = cv2.moments(largest_contour)
        
        if M['m00'] != 0:
            # Calculate the centroid of the largest contour
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            # Print the centroid coordinates
            print(f"Centroid of the orange object: ({cx}, {cy})")
            
            fappend.write(str(int(time.time())) + " " + str(cx) + "," + str(cy) +  " " + str(area) +  "\n" )

            # Draw the largest contour and the centroid on the frame
            cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    time.sleep(.01)

    
    

# Release the capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()