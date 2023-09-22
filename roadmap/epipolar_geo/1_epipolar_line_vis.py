import cv2
import numpy as np  
from matplotlib import pyplot as plt

imgs_name = [
    "im0.png",
    "im1.png",
]

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

def main():
    img0 = load_image_from_asset(imgs_name[0])
    img1 = load_image_from_asset(imgs_name[1])

    img_arr = [img0, img1]
    # extract features from the image and match them 
    kp_des_list = orb_keypoints(img_arr)
    fundamental_mat, kp1, kp2, ransac_matches, src_pts_ransac, dst_pts_ransac = feature_matching_with_ransac(img_arr, kp_des_list)
    print(fundamental_mat)


if __name__ == '__main__':
    main()