# Depth Estimation from Stereo

Stereo vision is the process of extracting 3D information from multiple 2D views of a scene. Stereo cameras, which are two cameras placed side by side at a known distance apart (known as the baseline), capture two images of the same scene from slightly different viewpoints. By finding the difference in the position of the same point in the two images (known as disparity), we can estimate the depth of that point in the scene.

## DATA SOURCE :

Middlebury Stereo Dataset

**Description**: The Middlebury Stereo dataset is one of the most well-known datasets in the stereo vision community. It provides several pairs of rectified stereo images along with ground truth disparity maps.
**Content**: Contains images of indoor scenes with objects at various depths. The dataset also provides non-occluded regions, which can be useful for evaluating the performance of disparity algorithms.

## Objective

The main goal of this project is to capture images from a stereo camera setup and use algorithms to compute the disparity map, which can then be used to estimate depth.

### Block Matching:

Block matching is a simple and widely used method for disparity computation. For each pixel in the left image, a block of pixels around it is compared with blocks in the same row of the right image. The block in the right image that matches best with the block in the left image gives the disparity. The comparison is often done using a similarity measure like Sum of Absolute Differences (SAD) or Sum of Squared Differences (SSD).

### Semi-Global Block Matching (SGBM):

SGBM is a more advanced method that considers not only the disparity of a single pixel but also the disparities of its neighbors. It introduces a smoothness constraint to ensure that the disparities change smoothly across the image, except at object boundaries. This results in more accurate and cleaner disparity maps compared to simple block matching.

## Skills Gained

- **Camera Models & Calibration**: Before estimating depth, it's crucial to understand the geometry of the stereo setup. Cameras need to be calibrated to find their intrinsic parameters (like focal length) and extrinsic parameters (like rotation and translation relative to each other). This calibration ensures that the disparity is computed accurately.

- **Feature Matching**: While not always necessary for block matching or SGBM, feature matching can be used to find corresponding points in the two images, which can aid in disparity computation, especially in textured regions.

- **Depth Estimation**: Once the disparity map is computed, it can be converted to a depth map. The depth Z of a point can be found using the formula:

`Z = f * B / d`

Where:
  - `f` is the focal length of the camera.
  - `B` is the baseline (distance between the two cameras).
  - `d` is the disparity of the point.

- **Understanding of Algorithms**: Implementing block matching and SGBM from scratch or even using libraries will give a deep understanding of how these algorithms work, their strengths, and their limitations.

- **Post-processing**: Raw disparity maps might have noise, inconsistencies, or holes. Skills in post-processing techniques like median filtering, bilateral filtering, or hole-filling can be gained to refine the disparity maps.

## Implementation Tips:

1. Start with capturing well-aligned stereo images. The better the alignment, the more accurate the disparity computation will be.
2. Use OpenCV, which provides functions for stereo calibration, rectification, and disparity computation.
3. Experiment with different block sizes and parameters for the algorithms to see how they affect the disparity map.
4. Visualize the disparity map using a colormap to get a pseudo-3D view of the scene.
5. For real-world applications, consider optimizing the algorithms for speed, especially if aiming for real-time performance.

In conclusion, this project offers a comprehensive understanding of stereo vision, from capturing images to processing them for depth estimation. It's a foundational project for anyone looking to delve into 3D computer vision or robotics.
