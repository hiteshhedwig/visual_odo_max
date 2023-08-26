# - **Objective**: Implement a tool that can calibrate a camera using a checkerboard pattern or other known markers. Dive into intrinsic and extrinsic parameters and lens distortion correction.
# - **Skills Gained**: Familiarity with camera calibration techniques and understanding of intrinsic and extrinsic parameters.

import cv2
import numpy as np
import glob

# Termination criteria for the iterative algorithm
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# checkerboard size:
checkerboard_size = (7,11)

# Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
# Assuming the checkerboard is 12x8
objp = np.zeros((checkerboard_size[0]*checkerboard_size[1],3), np.float32)
objp[:,:2] = np.mgrid[0:checkerboard_size[0],0:checkerboard_size[1]].T.reshape(-1,2)


# Arrays to store object points and image points from all the images
objpoints = [] # 3d points in real world space
imgpoints = [] # 2d points in image plane

def files_list(directory):
    files = []
    for file in glob.glob(directory+"/*"):
        img = cv2.imread(file)
        files.append(img)
    return files


def findCheckerboard(img):
    # The `global imgpoints, objpoints` statement is used to indicate that the `imgpoints` and
    # `objpoints` variables are global variables, meaning they can be accessed and modified from
    # anywhere in the code.
    global imgpoints, objpoints

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, checkerboard_size, None)
    if ret:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, checkerboard_size, corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(100)


def main():
    checkerboard_images = files_list("roadmap/foundation/assets/checkerboard/data/imgs/leftcamera")

    for checkerboard in checkerboard_images:
        findCheckerboard(checkerboard)
    cv2.destroyAllWindows()

    # Calibrate the camera
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, checkerboard_images[0].shape[1:], None, None)

    print("(Intrinsic) Camera Matrix: \n", mtx)
    print("Distortion Coefficients: \n", dist)


if __name__ == '__main__':
    main()