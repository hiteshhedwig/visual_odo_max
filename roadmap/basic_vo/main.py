import cv2

# Load the HEVC video
video_path = 'roadmap/basic_vo/assets/calib_challenge-main/labeled/0.hevc'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Couldn't open the video file.")
    exit()

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # If the frame is not read correctly, break the loop
    if not ret:
        break

    # Display the frame
    cv2.imshow('HEVC Video', frame)

    # Wait for 25ms and check if the user pressed the 'q' key
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
