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
    for path in glob.glob(PATH+"mount*.jpg"):
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

def get_good_matches(kp_desc_1, kp_desc_2):

    descriptors1 = kp_desc_1[1]
    descriptors2 = kp_desc_2[1]
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
    return good_matches

def homography_estimation(kp_desc_1, kp_desc_2, good_matches):
    keypoints1, descriptors1 = kp_desc_1
    keypoints2, descriptors2 = kp_desc_2

    # Extract the coordinates of matched keypoints
    src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches])
    dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches])

    # use ransac : 
    H, inliers = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    if inliers is None:
        raise ValueError("Homography not found !")

    # Filter matches using the inliers
    ransac_matches = [good_matches[i] for i, val in enumerate(inliers.ravel()) if val == 1]
    return H,ransac_matches

def laplacian_pyramid(img, levels):
    pyramid = []
    for i in range(levels):
        next_img = cv2.pyrDown(img)
        up_img = cv2.pyrUp(next_img, dstsize=(img.shape[1], img.shape[0]))
        laplacian = cv2.subtract(img, up_img)
        pyramid.append(laplacian)
        img = next_img
    pyramid.append(img)
    return pyramid

def blend_pyramids(lap_pyr1, lap_pyr2):
    blended_pyr = []
    for lap1, lap2 in zip(lap_pyr1, lap_pyr2):
        rows, cols, _ = lap1.shape
        laplacian = np.hstack((lap1[:, :cols//2], lap2[:, cols//2:]))
        blended_pyr.append(laplacian)
    return blended_pyr

def reconstruct_image(lap_pyr):
    img = lap_pyr[-1]
    for i in range(len(lap_pyr) - 2, -1, -1):
        img = cv2.pyrUp(img, dstsize=(lap_pyr[i].shape[1], lap_pyr[i].shape[0]))
        img = cv2.add(img, lap_pyr[i])
    return img


def main():
    PATH = "roadmap/foundation/assets/paranoma/"
    images =  load_paranoma_images(PATH)

    img0, img1 = images[:2]
    img0_grey = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
    img1_grey = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    keypoints1, descriptors1 = get_sift_feature(img0_grey)
    keypoints2, descriptors2 = get_sift_feature(img1_grey)

    good_matches = get_good_matches((keypoints1, descriptors1), (keypoints2, descriptors2))

    computed_homography, ransac_matches = homography_estimation((keypoints1, descriptors1), (keypoints2, descriptors2), good_matches)
    print(computed_homography.shape)

    # Draw matches
    img_matches = cv2.drawMatches(img0, keypoints1, img1, keypoints2, ransac_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # Warp image
    height, width, channels = img1.shape
    img0_warped = cv2.warpPerspective(img0, computed_homography, (width, height))

    # Simple blending
    # result = img1.copy()
    # result[np.where(img0_warped != 0)] = img0_warped[np.where(img0_warped != 0)]

    levels = 1  # Number of pyramid levels
    lap_pyr1 = laplacian_pyramid(img0_warped, levels)
    lap_pyr2 = laplacian_pyramid(img1, levels)

    blended_pyr = blend_pyramids(lap_pyr1, lap_pyr2)

    result = reconstruct_image(blended_pyr)

    # Show the results
    cv2.imshow('SIFT Feature Matching', img_matches)
    cv2.imshow("Multi-Band Blending ", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__' :
    main()