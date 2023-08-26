# ### Project 2: Feature Matching Tool
# - **Objective**: Implement a tool that detects features in images using techniques like SIFT or ORB and matches them across multiple images. Introduce RANSAC for robust feature matching.
# - **Skills Gained**: Understanding of feature detection, description, matching, and robust estimation techniques.
import glob as glob
import cv2 
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

    generate_bf_matching_keypoints(images, kp_des_list)


if __name__ == '__main__':
    main()