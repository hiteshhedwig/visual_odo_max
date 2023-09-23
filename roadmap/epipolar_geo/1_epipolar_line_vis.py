import cv2
import numpy as np  
from matplotlib import pyplot as plt
from roadmap.epipolar_geo.rectification_stereo import estimate_essential_matrix, decompose_essential_matrix, \
                validate_cheirality_condition, get_3d_triangulated_points

imgs_name = [
    "im0.png",
    "im1.png",
]

INTRINSIC_MATRIX = np.array([
                                [1733.74,  0,     792.27],
                                [0,      1733.74, 541.89],
                                [0,        0,     1]
                            ])

PATH = "roadmap/foundation/assets/stereo_data/artroom1/"

def load_image_from_asset(filename):
    return cv2.imread(PATH+filename)

def orb_keypoints(images):
    kp_des_list = []
    for image in images:
        orb = cv2.ORB_create()
        # find the keypoints with ORB
        kp = orb.detect(image,None)
        # compute the descriptors with ORB
        kp, des = orb.compute(image, kp)
        kp_des_list.append([kp, des])

    return kp_des_list

def feature_matching_with_ransac(images, kp_des_list):
    im0 = images[0]
    im1 = images[1]

    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    kp1 = kp_des_list[0][0]
    kp2 = kp_des_list[1][0]

    des1 = kp_des_list[0][1]
    des2 = kp_des_list[1][1]

    matches = bf.knnMatch(des1, des2, k=2)

    # For each pair of matches (m, n) obtained:
    # m is the best match and n is the second-best match.
    good_matches = []
    for m, n in matches:
        # The ratio test checks the quality of the matches.
        # If the distance of the best match (m.distance) is significantly smaller than that of the second-best match (n.distance),
        # then the match is considered to be "good".
        # In this case, if m's distance is less than 75% of n's distance, it's added to the good_matches list.
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # Extract the coordinates of matched keypoints
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches])
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches])

    # Use RANSAC to identify inliers
    # The fundamental matrix encapsulates the epipolar geometry between two views and is a fundamental concept in stereo vision and structure from motion.
    _, inliers = cv2.findFundamentalMat(src_pts, dst_pts, cv2.FM_RANSAC)

    # Filter matches using the inliers
    ransac_matches = [good_matches[i] for i, val in enumerate(inliers) if val == 1]

    # img_matches = cv2.drawMatches(im0, kp1, im1, kp2, ransac_matches, None)
    # plt.imshow(img_matches)
    # plt.show()

    # Use RANSAC to identify inliers
    # The fundamental matrix encapsulates the epipolar geometry between two views and is a fundamental concept in stereo vision and structure from motion.
    fundamental_mat, inliers = cv2.findFundamentalMat(src_pts, dst_pts, cv2.FM_RANSAC)
    if inliers is None:
        exit(0)

    # Filter matches using the inliers
    ransac_matches = [good_matches[i] for i, val in enumerate(inliers) if val == 1]

    # Extract the coordinates of matched keypoints using RANSAC matches
    src_pts_ransac = np.float32([kp1[m.queryIdx].pt for m in ransac_matches])
    dst_pts_ransac = np.float32([kp2[m.trainIdx].pt for m in ransac_matches])


    return fundamental_mat, kp1, kp2, ransac_matches, src_pts_ransac, dst_pts_ransac

def to_homogeneous_points(pts):
    return np.array([pts[0], pts[1], 1]).reshape(3,1)

def compute_epipolar_line(fundamental_mat, pts):
    homogeneous_pts = to_homogeneous_points(pts)
    homogeneous_epipolar_line = fundamental_mat@homogeneous_pts
    return homogeneous_epipolar_line.T[0]

def draw_epipolar_line(img, epipolar_line):
    # Determine two points on the epipolar line
    a,b,c = epipolar_line
    y1 = (-c - a*0) / b
    y2 = (-c - a*img.shape[1]) / b
    pt1 = (0, int(y1))
    pt2 = (img.shape[1], int(y2))

    # Draw the epipolar line on the image
    return cv2.line(img, pt1, pt2, (0, 255, 0), 2)  # Drawing the line in green color with thickness 2



def select_point(event, x, y, flags, param):
    global selected_point, img0, img1

    if event == cv2.EVENT_LBUTTONDOWN:
        selected_point = (x, y)
        print(f"Selected Point: {selected_point}")
        cv2.circle(img0, selected_point, 15, (0, 0, 255), -1)  # Draw a red circle at the selected point
        cv2.imshow("Stereo Image", img0)

def display_window(title , img):
    # global img0, img1

    # Create a window and set the mouse callback to our function
    cv2.namedWindow(title)
    cv2.setMouseCallback(title, select_point)

    cv2.imshow(title, img)
    cv2.waitKey(0)

def close_window():
    cv2.destroyAllWindows()

img0 = None
img1 = None
selected_point = None

def main():
    global img0, img1, selected_point

    img0 = load_image_from_asset(imgs_name[0])
    img1 = load_image_from_asset(imgs_name[1])

    img_arr = [img0, img1]
    # extract features from the image and match them 
    kp_des_list = orb_keypoints(img_arr)

    # match and compute fundamental matrix
    fundamental_mat, kp1, kp2, ransac_matches, src_pts, dst_pts = feature_matching_with_ransac(img_arr, kp_des_list)
    print(fundamental_mat)

    display_window("Stereo Image", img0)
    close_window()

    epipolar_line = compute_epipolar_line(fundamental_mat, selected_point)
    print(epipolar_line)

    annotated_img = draw_epipolar_line(img1, epipolar_line)
    display_window("EPIPOLAR LINES",annotated_img)
    close_window()

    # estimate essential matrices
    essential_mat = estimate_essential_matrix(fundamental_mat, INTRINSIC_MATRIX, INTRINSIC_MATRIX)
    print("Essential Matrix " , essential_mat)

    # get possible rotation and translation matrices
    possible_rotations, possible_translations = decompose_essential_matrix(essential_matrix=essential_mat)
    print(possible_rotations[0].shape)

    # cheirality verification
    R,t = validate_cheirality_condition(INTRINSIC_MATRIX, possible_rotations, possible_translations, src_pts[0], dst_pts[0])
    print("Valid rotation and translation matrices \n", R, "\n\n", t)

    ## stereo rectification
    R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(
        cameraMatrix1=INTRINSIC_MATRIX,
        cameraMatrix2=INTRINSIC_MATRIX,
        distCoeffs1=None,
        distCoeffs2=None,
        imageSize=img0.shape[0:2],
        R=R,
        T=t
    )

    ## warping soon !

if __name__ == '__main__':
    main()