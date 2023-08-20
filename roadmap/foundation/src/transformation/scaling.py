"""
Scaling Matrix Implementation
A scaling matrix is a fundamental concept in both linear algebra and computer graphics. 
It's primarily used to modify the size of an object, either enlarging or shrinking it, 
based on specified scaling factors along its axes.

This implementation focuses on scaling a 3D point in homogeneous coordinates.
"""

import numpy as np

def generate_scaling_matrix(sx, sy, sz, is_homogeneous=False):
    """
    Generates a scaling matrix based on the given scaling factors along the X, Y, and Z axes.
    
    Args:
    - sx (float): Scaling factor along the X-axis.
    - sy (float): Scaling factor along the Y-axis.
    - sz (float): Scaling factor along the Z-axis.
    - is_homogeneous (bool): If True, returns a 4x4 matrix, otherwise a 3x3 matrix.

    Returns:
    - np.array: A scaling matrix.
    """
    if is_homogeneous:
        return np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])
    else:
        return np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, sz]
        ])

def apply_scaling_to_point(scaling_matrix, point):
    """
    Applies the scaling transformation to a 3D point.

    Args:
    - scaling_matrix (np.array): The scaling matrix.
    - point (np.array): The 3D point.

    Returns:
    - np.array: The scaled 3D point.
    """
    return np.dot(scaling_matrix, point)

def apply_scaling_to_points(sx, sy, sz, points, is_homogeneous=False):
    """
    Applies the scaling transformation to an array of 3D points.

    Args:
    - sx (float): Scaling factor along the X-axis.
    - sy (float): Scaling factor along the Y-axis.
    - sz (float): Scaling factor along the Z-axis.
    - points (list): List of 3D points.
    - is_homogeneous (bool): If True, uses homogeneous coordinates.

    Returns:
    - list: List of scaled 3D points.
    """
    scaling_matrix = generate_scaling_matrix(sx, sy, sz, is_homogeneous)
    return [apply_scaling_to_point(scaling_matrix, point) for point in points]

def main():
    # A 3D point in homogeneous coordinates [X,Y,Z,1]
    point_homogeneous = np.array([2, 3, 6, 1])

    # Define scaling factors for X, Y, and Z axes
    sx, sy, sz = 3, 5, 2
    print(f"Scaling factors: X={sx}, Y={sy}, Z={sz}")

    # Apply the scaling transformation
    scaled_point = apply_scaling_to_point(generate_scaling_matrix(sx, sy, sz, is_homogeneous=True), point_homogeneous)

    print("Scaled point:", scaled_point)

if __name__ == '__main__':
    main()
