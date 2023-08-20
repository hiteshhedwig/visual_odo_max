# Rotation:
# Definition: Rotation means turning the 3D object about a specific axis or a point. This transformation can simulate activities like spinning a top, turning a doorknob, or rotating a camera view.
# Key Concepts:
#     Axis of Rotation: An object can be rotated around any of the three primary axes (X, Y, Z) or around an arbitrary axis.
#     Angle of Rotation: It defines the magnitude of the rotation. A positive angle results in a counter-clockwise rotation, while a negative angle results in a clockwise rotation (assuming you're looking in the direction of the axis).
#     Rotation Matrix: Like translation, rotation in 3D space can also be represented using matrices. A different rotation matrix is used for each axis (X, Y, Z).
#     Quaternion Rotation: Quaternions offer an alternative to matrices for representing rotations and can avoid certain issues like gimbal lock.
#     Applications: Any scenario requiring a change in the orientation of an object or camera uses rotation. For instance, turning characters in video games or simulations of planetary rotations
import numpy as np
import math

def to_radians(deg):
    """
    Convert degrees to radians.
    
    Parameters:
    - deg (float): Angle in degrees.
    
    Returns:
    - float: Angle in radians.
    """
    return deg * math.pi / 180

def rotation_matrix_2d(theta):
    return np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ])

def rotation_matrix_x(theta, extra_dim=None):
    """
    Generate a 4x4 rotation matrix for rotation about the X-axis.
    
    Parameters:
    - theta (float): Angle of rotation in radians.
    
    Returns:
    - ndarray: 4x4 matrix for rotation about X-axis.
    """
    if extra_dim is not None:
        return np.array([
            [1, 0, 0, 0],
            [0, np.cos(theta), -np.sin(theta), 0],
            [0, np.sin(theta), np.cos(theta), 0],
            [0, 0, 0, 1]
        ])
    else :
        return np.array([
            [1, 0, 0],
            [0, np.cos(theta), -np.sin(theta)],
            [0, np.sin(theta), np.cos(theta)],
        ])

def rotation_matrix_y(theta, extra_dim=None):
    """
    Generate a 4x4 rotation matrix for rotation about the Y-axis.
    
    Parameters:
    - theta (float): Angle of rotation in radians.
    
    Returns:
    - ndarray: 4x4 matrix for rotation about Y-axis.
    """
    if extra_dim is not None:
        return np.array([
            [np.cos(theta), 0, np.sin(theta), 0],
            [0, 1, 0, 0],
            [-np.sin(theta), 0, np.cos(theta), 0],
            [0, 0, 0, 1]
        ])
    else :
        return np.array([
            [np.cos(theta), 0, np.sin(theta)],
            [0, 1, 0],
            [-np.sin(theta), 0, np.cos(theta)],
        ])

def rotation_matrix_z(theta, extra_dim=None):
    """
    Generate a 4x4 rotation matrix for rotation about the Z-axis.
    
    Parameters:
    - theta (float): Angle of rotation in radians.
    
    Returns:
    - ndarray: 4x4 matrix for rotation about Z-axis.
    """
    if extra_dim is not None:
        return np.array([
            [np.cos(theta), -np.sin(theta), 0, 0],
            [np.sin(theta), np.cos(theta), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
    else :
        return np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1],
        ])


def apply_rotation(rot_x, rot_y, rot_z, point_xyz):
    # print("rotation_mat ", rot_x, " ", rot_y, " ", rot_z)
    # print("point_xyz ", point_xyz)
    rotated = np.array(rot_z @ rot_y @ rot_x @ point_xyz)
    # print("rotated ", rotated)
    return rotated

def apply_rotation_2d(rot2d, point_xy):
    return np.array(rot2d@point_xy).astype(int)

def apply_rotation_to_pointarray(theta,axis, points_arr):
    points_arr_new = []
    x_rot = rotation_matrix_x(0)
    y_rot = rotation_matrix_x(0)
    z_rot = rotation_matrix_x(0)
    angle = to_radians(theta)
    if axis == "x":
        x_rot = rotation_matrix_x(angle)
    if axis == "y":
        y_rot = rotation_matrix_y(angle)
    if axis == "z":
        z_rot = rotation_matrix_z(angle)

    for point_xyz in points_arr:
        rotated_xyz = apply_rotation(x_rot, y_rot, z_rot, point_xyz)
        points_arr_new.append(rotated_xyz)
    return points_arr_new
    

def main():
    """
    Demonstrate the rotation of a 3D point using the above functions.
    """
    angle = to_radians(45)
    object_xyz = np.array([2, 3, 6, 1])

    x_rot = rotation_matrix_x(angle)
    y_rot = rotation_matrix_y(angle)
    z_rot = rotation_matrix_z(angle)

    rotated_xyz = apply_rotation(x_rot, y_rot, z_rot, object_xyz)
    print("Rotated point:", rotated_xyz)

if __name__ == "__main__":
    # Run the demonstration
    main()



