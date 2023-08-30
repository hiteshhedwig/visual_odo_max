## A step to be more better in VO : 

### Disclaimer :

I am starting this repo to revisit all the basics and fill in the gaps in my knowledge. I have several years of experience in Computer Vision and Deep Learning, but I haven't documented any notes for review. This repo is designed to address that exact issue. In the process, I aim to help people who are interested in building a strong foundation in the basics.

1. Foundational Knowledge : 

- [**Done**] Linear Algebra: Understand matrices, vectors, eigenvalues, and eigenvectors.
- [**Done**] Probability and Statistics: Basics of probability, Bayes' theorem, and statistical estimation techniques.
- [**Ongoing**] Computer Vision Basics: Familiarize yourself with image processing, feature extraction, and camera models.

2. Understand Camera Models and Calibration:

- Learn about different camera models, especially the pinhole camera model.
- Understand camera calibration techniques to determine intrinsic and extrinsic parameters.

3. Study Epipolar Geometry:

- Get a grasp of concepts like epipolar lines, epipoles, and the essential and fundamental matrices.
- These concepts are crucial for understanding the geometric relationship between multiple camera views.

4. Hands-on with Basic VO:

- Start with 2-view VO, where you estimate the motion between two consecutive frames.
- Use feature matching techniques (like SIFT, SURF, ORB) to find correspondences between frames.
- Estimate the relative pose (rotation and translation) between frames.

5. Explore Robust Estimation Techniques:

- Learn about RANSAC and its variants to handle outliers in feature matching.
- Understand how to refine pose estimates using bundle adjustment.

6. Dive into Advanced VO Techniques:

- Explore direct methods (which use pixel intensity values) in addition to feature-based methods.
- Study multi-view optimization where more than two views are used to estimate motion.
- Look into loop closure detection to correct drift over long sequences.

7. Hands-on Projects:

- Implement a basic VO pipeline using a library like OpenCV.
- Use datasets like KITTI or TUM to test and benchmark your VO implementation.
- Explore open-source VO and SLAM systems like ORB-SLAM to understand advanced implementations.

8. Deepen Your Understanding:

- Delve into probabilistic approaches to VO, understanding how uncertainty is modeled and propagated.
- Explore the integration of VO with inertial measurement units (IMUs) for more robust motion estimation.

9. Stay Updated and Engage with the Community:

- VO is an active research area. Regularly read new research papers and articles.
- Engage with online forums, attend workshops or conferences, and participate in open-source projects.

10. Expand to Visual SLAM:

- Once you're comfortable with VO, you can expand to Visual Simultaneous Localization and Mapping (SLAM), which combines VO with mapping capabilities.

Recommended Resources**:

    Books: "Multiple View Geometry in Computer Vision" by Richard Hartley and Andrew Zisserman.
    Online Courses: "Visual Perception for Self-Driving Cars" on Coursera by the University of Toronto.
    Tutorials: OpenCV tutorials, ROS visual odometry tutorials.
    Datasets: KITTI Vision Benchmark Suite, TUM MonoVO dataset.

