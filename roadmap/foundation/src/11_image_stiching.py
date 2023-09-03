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
    for path in glob.glob(PATH+"img*.jpg"):
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

def blend_pyramids(lap_pyr_list):
    # Initialize the blended pyramid with zeros, using the shape of the first pyramid
    blended_pyr = [np.zeros(lap.shape) for lap in lap_pyr_list[0]]

    # Calculate the number of pyramids
    num_pyr = len(lap_pyr_list)

    # Iterate through each level of the pyramid
    for level in range(len(blended_pyr)):
        # Iterate through each pyramid
        for lap_pyr in lap_pyr_list:
            # Add the contribution of each pyramid to the blended pyramid at this level
            blended_pyr[level] += lap_pyr[level] / num_pyr

    return blended_pyr

def reconstruct_and_combine(lap_pyr_results):
    # Initialize an empty image for accumulating the results
    final_img = None
    
    for lap_pyr in lap_pyr_results:
        # Reconstruct the image from its Laplacian pyramid
        img = lap_pyr[-1]
        for i in range(len(lap_pyr) - 2, -1, -1):
            img = cv2.pyrUp(img, dstsize=(lap_pyr[i].shape[1], lap_pyr[i].shape[0]))
            img = cv2.add(img, lap_pyr[i])
        
        # Accumulate the reconstructed image
        if final_img is None:
            final_img = img
        else:
            # Assuming the images are aligned and of the same size
            img = img.astype(final_img.dtype)
            final_img = cv2.addWeighted(final_img, 0.5, img, 0.5, 0)
    
    return final_img


def combine_images(images):
    result = images[0]
    for image in images[1:]:
        result = cv2.hconcat([result, image])
    return result

def normalize(img):
    min_val = np.min(img)
    max_val = np.max(img)
    return ((img - min_val) / (max_val - min_val) * 255).astype(np.uint8)

def reconstruct_image(lap_pyr):
    img = lap_pyr[-1]  # Start with the smallest image
    for i in range(len(lap_pyr) - 2, -1, -1):  # Traverse the pyramid from bottom to top
        img = cv2.pyrUp(img, dstsize=(lap_pyr[i].shape[1], lap_pyr[i].shape[0]))  # Upsample the image
        img = cv2.add(img, lap_pyr[i])  # Add the Laplacian image
    return img

def reconstruct_and_combine(lap_pyr_results):
    final_img = None
    for lap_pyr in lap_pyr_results:
        img = reconstruct_image(lap_pyr)
        if final_img is None:
            final_img = img
        else:
            final_img = cv2.hconcat([final_img, img])
    return final_img

def main():
    PATH = "roadmap/foundation/assets/paranoma/"
    images = load_paranoma_images(PATH)
    lap_pyr_results = []
    accumulated_pyr = None
    result = images[0]

    for img0, img1 in zip(images, images[1:]):
        img0_grey = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
        img1_grey = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        keypoints1, descriptors1 = get_sift_feature(img0_grey)
        keypoints2, descriptors2 = get_sift_feature(img1_grey)
        good_matches = get_good_matches((keypoints1, descriptors1), (keypoints2, descriptors2))
        computed_homography,_ = homography_estimation((keypoints1, descriptors1), (keypoints2, descriptors2), good_matches)
        height, width, channels = img1.shape
        img0_warped = cv2.warpPerspective(img0, computed_homography, (width, height))

        blended_img = img1.copy()
        blended_img[np.where(img0_warped != 0)] = img0_warped[np.where(img0_warped != 0)]
        
        # Update the result (assuming the images are aligned)
        result[np.where(blended_img != 0)] = blended_img[np.where(blended_img != 0)]

    # Show the results
    cv2.imshow("Multi-Band Blending ", normalize(result))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
