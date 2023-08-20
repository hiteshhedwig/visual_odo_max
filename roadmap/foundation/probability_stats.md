# Probability and Statistics Projects for Visual Odometry (VO)

This repository contains a collection of projects focused on applying probability and statistics concepts, especially tailored for understanding visual odometry.

## Table of Contents

- [Probability and Statistics Projects for Visual Odometry (VO)](#probability-and-statistics-projects-for-visual-odometry-vo)
  - [Table of Contents](#table-of-contents)
  - [Gaussian Distribution Simulator](#gaussian-distribution-simulator)
  - [Bayesian Filter Implementation](#bayesian-filter-implementation)
  - [Multivariate Gaussian Distribution Visualization](#multivariate-gaussian-distribution-visualization)
  - [Monte Carlo Simulation for VO](#monte-carlo-simulation-for-vo)
  - [Particle Filter for VO](#particle-filter-for-vo)
  - [Statistical Hypothesis Testing in Feature Matching](#statistical-hypothesis-testing-in-feature-matching)
  - [Error Analysis in VO](#error-analysis-in-vo)
  - [Camera Motion Estimation with RANSAC](#camera-motion-estimation-with-ransac)
  - [Probabilistic Data Association in VO](#probabilistic-data-association-in-vo)
  - [Gaussian Mixture Models for VO](#gaussian-mixture-models-for-vo)

## Gaussian Distribution Simulator

- **Objective**: Implement a simulator that generates data based on Gaussian distributions and visualizes it.
- **Skills Gained**: Deep understanding of Gaussian distributions and their properties.
- **Addition**: Introduce the concept of covariance in 2D Gaussian distributions. Visualize how changing the covariance affects the shape and orientation of the distribution.

## Bayesian Filter Implementation

- **Objective**: Implement a basic Bayesian filter to estimate the state of a system given noisy measurements.
- **Skills Gained**: Application of conditional probability and Bayes' theorem in state estimation.
- **Modification**: Extend the Bayesian filter to handle multi-modal distributions and implement a specific type like the Kalman Filter.

## Multivariate Gaussian Distribution Visualization

- **Objective**: Extend the Gaussian Distribution Simulator to handle multivariate Gaussian distributions. Visualize the 2D and 3D distributions.
- **Skills Gained**: Understand multivariate Gaussian distributions and their significance in VO.

## Monte Carlo Simulation for VO

- **Objective**: Use Monte Carlo methods to simulate the motion of a camera through a scene and estimate its trajectory based on noisy measurements.
- **Skills Gained**: Practical understanding of sampling methods and their application in state estimation.

## Particle Filter for VO

- **Objective**: Implement a particle filter to estimate the camera's trajectory in a 2D space using synthetic data.
- **Skills Gained**: Grasp non-parametric filtering and its applications in non-linear systems or non-Gaussian noise scenarios.

## Statistical Hypothesis Testing in Feature Matching

- **Objective**: Given two sets of image features, use statistical tests to determine if they come from the same distribution.
- **Skills Gained**: Application of hypothesis testing in image processing and VO.

## Error Analysis in VO

- **Objective**: Implement a basic VO pipeline and introduce various types of noise (e.g., Gaussian, motion blur). Analyze the impact of different noise levels on VO accuracy.
- **Skills Gained**: Understand the robustness of VO algorithms to different types of noise and uncertainties.

## Camera Motion Estimation with RANSAC

- **Objective**: Implement the RANSAC algorithm to robustly estimate camera motion from matched feature points, discarding outliers.
- **Skills Gained**: Understand the application of probabilistic models in robust estimation techniques.

## Probabilistic Data Association in VO

- **Objective**: Implement a system that probabilistically associates features between frames, considering the uncertainty in feature detection and matching.
- **Skills Gained**: Application of probability in data association problems, crucial for feature-based VO.

## Gaussian Mixture Models for VO

- **Objective**: Implement a Gaussian Mixture Model to represent multi-modal distributions in VO scenarios, like when there are multiple possible camera poses.
- **Skills Gained**: Understand how to represent and handle uncertainties when there are multiple hypotheses in VO.

