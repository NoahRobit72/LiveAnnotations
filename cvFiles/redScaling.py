import cv2
import numpy as np

# Define the range of red color in HSV
lower_red1 = np.array([0, 50, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 50, 50])
upper_red2 = np.array([180, 255, 255])

# Initialize the video capture object
cap = cv2.VideoCapture(0)  # Use 0 for webcam, or replace with video file path

if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

# Initial minimum contour area threshold
initial_min_contour_area = 1000
min_contour_area = initial_min_contour_area

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create masks for the red color
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize tracker presence flag
    tracker_present = False

    # If any contours are found
    if contours:
        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Calculate the area of the largest contour
        area = cv2.contourArea(largest_contour)
        
        # Update minimum contour area threshold based on the detected area
        min_contour_area = initial_min_contour_area * (1000 / area)

        if area > min_contour_area:
            # Calculate the moments of the largest contour
            M = cv2.moments(largest_contour)
            
            if M['m00'] != 0:
                # Calculate the centroid of the largest contour
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])

                # Print the centroid coordinates and area
                print(f"Centroid of the red object: ({cx}, {cy}), Area: {area} pixels")

                # Draw the largest contour and the centroid on the frame
                cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

                # Set tracker presence flag
                tracker_present = True

    # If no tracker detected, print "No tracker"
    if not tracker_present:
        print("No tracker")

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()