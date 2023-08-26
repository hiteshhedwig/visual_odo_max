# ### Project 2: Feature Matching Tool
# - **Objective**: Implement a tool that detects features in images using techniques like SIFT or ORB and matches them across multiple images. Introduce RANSAC for robust feature matching.
# - **Skills Gained**: Understanding of feature detection, description, matching, and robust estimation techniques.
import glob as glob
import cv2 
import numpy as np
from matplotlib import pyplot as plt

def files_list(directory):
    files = []
    for file in glob.glob(directory+"/*"):
        img = cv2.imread(file, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (600,600))
        files.append(img)
    return files

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

def generate_bf_matching_keypoints(images,kp_des_list):

    for idx, image in enumerate(images):
        if idx == len(images)-1:
            break
        # Use BFMatcher (Brute Force Matcher) to find matches
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(kp_des_list[idx][1], kp_des_list[idx+1][1])

        # Sort matches based on their distances
        matches = sorted(matches, key=lambda x: x.distance)

        # Draw the matches
        img_matches = cv2.drawMatches(images[idx], kp_des_list[idx][0], images[idx+1], kp_des_list[idx+1][0], matches[:50], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        # Display the matched images
        plt.imshow(img_matches)
        plt.show()

def main():
    directory = "roadmap/foundation/assets/jimmy"
    images = files_list(directory)
    print(f"{len(images)} Numbers of images are loaded")

    kp_des_list = orb_keypoints(images)
    img1 = images[0]
    img2 = images[1]

    # generate_bf_matching_keypoints(images, kp_des_list)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)

    kp1 = kp_des_list[0][0]
    kp2 = kp_des_list[1][0]

    des1 = kp_des_list[0][1]
    des2 = kp_des_list[1][1]

    # use knnMatch(not match()) to apply good ratio filter later
    # The knnMatch method is used to find the k closest descriptors in the second image for each descriptor in the first image.
    # Specifically, for each descriptor in the first image (des1), knnMatch finds the k best matches in the second image (des2).
    # When performing the ratio test, k is typically set to 2. This means for each descriptor in des1, we retrieve the two best matches from des2.
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


    img_matches = cv2.drawMatches(img1, kp1, img2, kp2, ransac_matches, None)
    plt.imshow(img_matches)
    plt.show()


if __name__ == '__main__':
    main()