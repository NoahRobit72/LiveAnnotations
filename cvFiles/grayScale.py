import cv2

# Initialize the video capture object
cap = cv2.VideoCapture(0)  # Use 0 for webcam, or replace with video file path

if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

# Loop to continuously get frames
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if frame is captured successfully
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('Grayscale Video', gray)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()