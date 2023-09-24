import cv2
from roadmap.epipolar_geo.rectification_stereo import estimate_essential_matrix, decompose_essential_matrix, \
                validate_cheirality_condition_all_pts, get_3d_triangulated_points
import numpy as np
from roadmap.basic_vo.ops import orb_keypoints, feature_matching_with_ransac, \
                            get_euler_angles, get_mse

######################

# Load the HEVC video
base_path = "roadmap/basic_vo/assets/calib_challenge-main/labeled/"
video_path = 'roadmap/basic_vo/assets/calib_challenge-main/labeled/0.hevc'
cap = cv2.VideoCapture(video_path)

gt = np.loadtxt(base_path + str(0) + '.txt')

if not cap.isOpened():
    print("Error: Couldn't open the video file.")
    exit()


INTRINSIC_MATRIX = np.array([
                                [910,      0, 874/2.0],
                                [0,      910, 1164/2.0],
                                [0,        0,     1]
                            ])

prev_frame = None

predicted_pitch_yaw = []
op = 0

pitch, yaw = 0, 0



while True:
    # Read a frame from the video
    ret, frame = cap.read()
    if prev_frame is None :
        prev_frame = frame
        continue

    # If the frame is not read correctly, break the loop
    if not ret:
        break
    # print(op)

    img_arr = [prev_frame, frame]
    kp_des_list = orb_keypoints(img_arr)
    fundamental_mat, kp1, kp2, ransac_matches, src_pts, dst_pts = feature_matching_with_ransac(img_arr, kp_des_list)
    essential_mat = estimate_essential_matrix(fundamental_mat, INTRINSIC_MATRIX, INTRINSIC_MATRIX)
    # print("Essential Matrix " , essential_mat)
    # get possible rotation and translation matrices
    possible_rotations, possible_translations = decompose_essential_matrix(essential_matrix=essential_mat)

    # cheirality verification
    R,t = validate_cheirality_condition_all_pts(INTRINSIC_MATRIX, possible_rotations, possible_translations, src_pts, dst_pts)
    # print("Valid rotation and translation matrices \n", R, "\n\n", t)
    if R is not None:
        pitch, yaw = get_euler_angles(R)
        
    print("Pitch and yaw ", pitch, yaw)
    predicted_pitch_yaw.append([pitch, yaw])
    op+=1

    zero_mses = []
    mses = []


    zero_mses.append(get_mse(gt[:op], np.zeros_like(gt[:op])))

    mses.append(get_mse(gt[:op], predicted_pitch_yaw[:op]))


    percent_err_vs_all_zeros = 100*np.mean(mses)/np.mean(zero_mses)
    print(f'YOUR ERROR SCORE IS {percent_err_vs_all_zeros:.2f}% (lower is better)')

    cv2.putText(
        frame,                                  # Image
        f"Error - {percent_err_vs_all_zeros}%",                   # Text
        (int(frame.shape[0] - frame.shape[0]*0.25), int(frame.shape[1]*0.25)),                             # Starting point coordinates
        cv2.FONT_HERSHEY_COMPLEX_SMALL,         # Font type
        1,                                      # Font scale
        (0, 255, 0),                            # Font color (Green in this case)
        1                                       # Line type
    )


    # Display the frame
    cv2.imshow('HEVC Video', frame)

    # Wait for 25ms and check if the user pressed the 'q' key
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

    prev_frame = frame



# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
