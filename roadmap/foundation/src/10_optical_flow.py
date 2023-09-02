import numpy as np
import cv2

# Initialize video capture
cap = cv2.VideoCapture('/home/hedwig/Downloads/production_id 4793828 (1080p).mp4')

# Parameters for ShiTomasi corner detection
feature_params = dict(maxCorners=100, qualityLevel=0.6, minDistance=7, blockSize=7)

# Parameters for Lucas-Kanade optical flow
lk_params = dict(winSize=(30, 30), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.1))

# Initial frame and points
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)

# Initialize video writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_optical_flow.mp4', fourcc, 20.0, (1920, 1080))


while True:
    ret, frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate optical flow using Lucas-Kanade method
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # Select good points
    good_new = p1[st == 1]
    good_old = p0[st == 1]

    # Draw the tracks
    magnitudes = np.linalg.norm(good_new - good_old, axis=1)
    threshold = 2.0  # Set your own threshold
    good_new = good_new[magnitudes > threshold]
    good_old = good_old[magnitudes > threshold]

    if len(good_old) == 0 or len(good_new) == 0:
        continue

    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)
        frame = cv2.circle(frame, (int(a), int(b)), 5, (0, 0, 255), -1)

        # # adjust box height so that reduces as person goes far away
        # box_height = 200  # Replace with the desired height of the box
        # box_width = int(box_height / 2)  # Width is half the height (2:1 ratio)
        # center_point = (int(a), int(b))
        # # Calculate the top-left and bottom-right points of the box
        # top_left = (int(center_point[0] - box_width / 2), int(center_point[1] - box_height / 2))
        # bottom_right = (int(center_point[0] + box_width / 2), int(center_point[1] + box_height / 2))
        # cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

        # print(a, b)

    img = cv2.add(frame, mask)


    # Resize the frame to 1920, 1080 before writing
    img_resized = cv2.resize(img, (1920, 1080))

    # Write the frame
    out.write(img_resized)

    # Show the image
    cv2.imshow('Optical Flow - Lucas-Kanade', img)

    # Update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

out.release()
cv2.destroyAllWindows()
cap.release()
