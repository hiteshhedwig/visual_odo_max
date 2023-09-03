import cv2
import numpy as np
import glob


# Initialize SIFT detector
sift = cv2.SIFT_create()

def load_image(filename):
    img = cv2.imread(filename)
    img = cv2.resize(img, (640, 480))
    return img

def load_paranoma_images(PATH) :
    paths = []
    for path in glob.glob(PATH+"*.jpg"):
        paths.append(path)
    sorted_paths = sorted(paths)
    print(sorted_paths)
    imgs = []
    for path in sorted_paths:
        imgs.append(load_image(path))
    return imgs

def get_sift_feature(img):
    global sift
    keypoints1, descriptors1 = sift.detectAndCompute(img, None)
    return keypoints1, descriptors1

def main():
    PATH = "roadmap/foundation/assets/paranoma/"
    images =  load_paranoma_images(PATH)

    img0, img1 = images[:2]
    img0_grey = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
    img1_grey = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    keypoints1, descriptors1 = get_sift_feature(img0_grey)
    keypoints2, descriptors2 = get_sift_feature(img1_grey)

    # Initialize FLANN-based matcher
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Match descriptors using FLANN
    matches = flann.knnMatch(descriptors1, descriptors2, k=2)

    # Apply ratio test to find good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    # Draw matches
    img_matches = cv2.drawMatches(img0, keypoints1, img1, keypoints2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # Show the results
    cv2.imshow('SIFT Feature Matching', img_matches)
    cv2.waitKey(0)
    cv2.destroyAllWindows()





    

if __name__ == '__main__' :
    main()