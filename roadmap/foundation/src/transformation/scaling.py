"""
Scaling Matrix Implementation
A scaling matrix is a fundamental concept in both linear algebra and computer graphics. 
It's primarily used to modify the size of an object, either enlarging or shrinking it, 
based on specified scaling factors along its axes.

This implementation focuses on scaling a 3D point in homogeneous coordinates.
"""

import numpy as np

def get_scaling_matrix(Sx, Sy, Sz, extra_dim=None):
    """
    Generate a 4x4 scaling matrix for 3D transformations.
    
    Parameters:
    - Sx (float): Scaling factor along the X-axis.
    - Sy (float): Scaling factor along the Y-axis.
    - Sz (float): Scaling factor along the Z-axis.
    
    Returns:
    - ndarray: 4x4 scaling matrix.
    """
    if extra_dim is not None:
        return np.array([
                        [Sx, 0, 0, 0],
                        [0, Sy, 0, 0],
                        [0, 0, Sz, 0],
                        [0, 0, 0, 1]
                    ])
    else :
        return np.array([
                        [Sx, 0, 0],
                        [0, Sy, 0],
                        [0, 0, Sz],
                    ])

def apply_scaling(scaling_matrix, point_xyz_h):
    """
    Apply the scaling transformation to a 3D point in homogeneous coordinates.
    
    Parameters:
    - scaling_matrix (ndarray): 4x4 scaling matrix.
    - point_xyz_h (ndarray): 3D point in homogeneous coordinates.
    
    Returns:
    - ndarray: Scaled 3D point in homogeneous coordinates.
    """
    return scaling_matrix @ point_xyz_h

def apply_scaling_to_pointarray(Sx, Sy, Sz, points_arr):
    points_arr_new = []
    scaling_mat = get_scaling_matrix(Sx, Sy, Sz)
    for point_xyz in points_arr:
        translated_xyz = apply_scaling(scaling_mat, point_xyz)
        points_arr_new.append(translated_xyz)
    return points_arr_new


def main():
    # A 3D point in homogeneous coordinates [X,Y,Z,1]
    point_xyz_h = np.array([2, 3, 6, 1])

    # Define scaling factors for X, Y, and Z axes
    Sx, Sy, Sz = 3, 5, 2
    print(f"Scaling factors: X={Sx}, Y={Sy}, Z={Sz}")

    # Get the scaling matrix
    scaling_matrix = get_scaling_matrix(Sx, Sy, Sz)

    # Apply the scaling transformation
    scaled_point_xyz = apply_scaling(scaling_matrix, point_xyz_h)

    print("Scaled point:", scaled_point_xyz)

if __name__ == '__main__':
    main()
