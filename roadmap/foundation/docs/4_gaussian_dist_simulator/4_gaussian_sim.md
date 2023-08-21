# Gaussian Distribution Simulator

## Overview

A Gaussian distribution, also known as a normal distribution, is a type of continuous probability distribution for a real-valued random variable. It's characterized by its mean (µ) and standard deviation (σ). The Gaussian distribution is fundamental in statistics and is used in the natural and social sciences to represent real-valued random variables whose distributions are not known.

## Objective

The main goal of this project is to implement a simulator that can generate data points based on specified Gaussian distributions and then visualize these points. This visualization will help in understanding the properties and behavior of the Gaussian distribution.

## Skills Gained

### 1. Deep understanding of Gaussian distributions and their properties:

- **Mean (µ)**: Represents the center of the distribution.
- **Standard Deviation (σ)**: Indicates the spread or width of the distribution. A smaller σ will make the curve narrower, while a larger σ will make it wider.
- **Probability Density Function (PDF)**: The function used to depict the data distribution. The area under the curve represents the probability of a data point falling within a particular range.

### 2. Data Generation:

Learn how to generate random data points that follow a Gaussian distribution using various methods, such as the Box-Muller transform or using libraries like NumPy.

### 3. Data Visualization:

Understand how to plot and visualize the generated data points and the Gaussian distribution curve, which can be done using libraries like Matplotlib or Seaborn in Python.

## Addition: Covariance in 2D Gaussian Distributions

When dealing with multivariate Gaussian distributions (like 2D), the concept of covariance comes into play. Covariance indicates the directionality or orientation of the data spread.

- **Covariance Matrix**: In a 2D Gaussian distribution, the covariance matrix is a 2x2 matrix that represents the covariance between the two variables. The diagonal elements represent the variances of the variables, and the off-diagonal elements represent the actual covariance.

- **Visualizing Covariance**: By changing the values in the covariance matrix, you can observe changes in the shape and orientation of the 2D Gaussian distribution. For instance:
  - A positive covariance will tilt the distribution counterclockwise.
  - A negative covariance will tilt it clockwise.
  - A covariance of zero means the variables are independent, resulting in a circular (or axis-aligned elliptical) distribution.

By introducing the concept of covariance and allowing the user to modify the covariance matrix in the simulator, you can gain a deeper understanding of how covariance affects the shape and orientation of 2D Gaussian distributions.

