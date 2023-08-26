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
        # img = cv2.resize(img, (600,600))
        files.append(img)
    return files

def main():
    directory = "roadmap/foundation/assets/dogs"
    images = files_list(directory)
    print(f"{len(images)} Numbers of images are loaded")

    orb = cv2.ORB_create()
    # find the keypoints with ORB
    kp = orb.detect(images[-1],None)
    # compute the descriptors with ORB
    kp, des = orb.compute(images[-1], kp)

    print(des)

    img2 = cv2.drawKeypoints(images[-1], kp, None, color=(255,0,0), flags=0)
    plt.imshow(img2), plt.show()

if __name__ == '__main__':
    main()