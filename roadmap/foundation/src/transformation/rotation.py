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
import curses


def to_radians(deg):
    """
    Convert degrees to radians.
    
    Parameters:
    - deg (float): Angle in degrees.
    
    Returns:
    - float: Angle in radians.
    """
    return deg * math.pi / 180

def generate_2d_rotation_matrix(angle_rad):
    """
    Generate a 2x2 rotation matrix for a given angle in radians.
    
    Parameters:
    - angle_rad (float): Angle of rotation in radians.
    
    Returns:
    - ndarray: 2x2 rotation matrix.
    """
    return np.array([
            [np.cos(angle_rad), -np.sin(angle_rad)],
            [np.sin(angle_rad), np.cos(angle_rad)]
        ])

def generate_rotation_matrix_x(angle_rad, is_4d=False):
    """
    Generate a rotation matrix for rotation about the X-axis.
    
    Parameters:
    - angle_rad (float): Angle of rotation in radians.
    - is_4d (bool): If True, returns a 4x4 matrix, otherwise 3x3.
    
    Returns:
    - ndarray: Rotation matrix for rotation about X-axis.
    """
    if is_4d:
        return np.array([
            [1, 0, 0, 0],
            [0, np.cos(angle_rad), -np.sin(angle_rad), 0],
            [0, np.sin(angle_rad), np.cos(angle_rad), 0],
            [0, 0, 0, 1]
        ])
    else:
        return np.array([
            [1, 0, 0],
            [0, np.cos(angle_rad), -np.sin(angle_rad)],
            [0, np.sin(angle_rad), np.cos(angle_rad)],
        ])

def generate_rotation_matrix_y(angle_rad, is_4d=False):
    """
    Generate a rotation matrix for rotation about the Y-axis.
    
    Parameters:
    - angle_rad (float): Angle of rotation in radians.
    - is_4d (bool): If True, returns a 4x4 matrix, otherwise 3x3.
    
    Returns:
    - ndarray: Rotation matrix for rotation about Y-axis.
    """
    if is_4d:
        return np.array([
            [np.cos(angle_rad), 0, np.sin(angle_rad), 0],
            [0, 1, 0, 0],
            [-np.sin(angle_rad), 0, np.cos(angle_rad), 0],
            [0, 0, 0, 1]
        ])
    else:
        return np.array([
            [np.cos(angle_rad), 0, np.sin(angle_rad)],
            [0, 1, 0],
            [-np.sin(angle_rad), 0, np.cos(angle_rad)],
        ])

def generate_rotation_matrix_z(angle_rad, is_4d=False):
    """
    Generate a rotation matrix for rotation about the Z-axis.
    
    Parameters:
    - angle_rad (float): Angle of rotation in radians.
    - is_4d (bool): If True, returns a 4x4 matrix, otherwise 3x3.
    
    Returns:
    - ndarray: Rotation matrix for rotation about Z-axis.
    """
    if is_4d:
        return np.array([
            [np.cos(angle_rad), -np.sin(angle_rad), 0, 0],
            [np.sin(angle_rad), np.cos(angle_rad), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
    else:
        return np.array([
            [np.cos(angle_rad), -np.sin(angle_rad), 0],
            [np.sin(angle_rad), np.cos(angle_rad), 0],
            [0, 0, 1],
        ])


def apply_3d_rotation(x_rotation_matrix, y_rotation_matrix, z_rotation_matrix, point):
    """
    Apply rotation matrices to a 3D point.
    
    Parameters:
    - x_rotation_matrix (ndarray): X-axis rotation matrix.
    - y_rotation_matrix (ndarray): Y-axis rotation matrix.
    - z_rotation_matrix (ndarray): Z-axis rotation matrix.
    - point (ndarray): 3D point.
    
    Returns:
    - ndarray: Rotated 3D point.
    """
    return z_rotation_matrix @ y_rotation_matrix @ x_rotation_matrix @ point

def apply_2d_rotation(rotation_matrix_2d, point_2d):
    """
    Apply a 2D rotation matrix to a 2D point.
    
    Parameters:
    - rotation_matrix_2d (ndarray): 2D rotation matrix.
    - point_2d (ndarray): 2D point.
    
    Returns:
    - ndarray: Rotated 2D point.
    """
    return rotation_matrix_2d @ point_2d

def rotate_points_based_on_key(angle_deg, axis_key, points):
    """
    Rotate a list of points based on a given axis key.
    
    Parameters:
    - angle_deg (float): Angle of rotation in degrees.
    - axis_key (int): Key representing the axis of rotation.
    - points (list): List of 3D points.
    
    Returns:
    - list: List of rotated 3D points.
    """
    rotated_points = []
    angle_rad = np.radians(angle_deg)
    
    x_rotation_matrix = generate_rotation_matrix_x(0)
    y_rotation_matrix = generate_rotation_matrix_y(0)
    z_rotation_matrix = generate_rotation_matrix_z(0)
    
    if axis_key == curses.KEY_DOWN:
        x_rotation_matrix = generate_rotation_matrix_x(angle_rad)
    elif axis_key == curses.KEY_RIGHT:
        y_rotation_matrix = generate_rotation_matrix_y(angle_rad)
    elif axis_key == curses.KEY_UP:
        x_rotation_matrix = generate_rotation_matrix_x(-angle_rad)
    elif axis_key == curses.KEY_LEFT:
        y_rotation_matrix = generate_rotation_matrix_y(-angle_rad)

    for point in points:
        rotated_point = apply_3d_rotation(x_rotation_matrix, y_rotation_matrix, z_rotation_matrix, point)
        rotated_points.append(rotated_point)
    
    return rotated_points

    

def main():
    """
    Demonstrate the rotation of a 3D point using the above functions.
    """
    angle = to_radians(45)
    object_xyz = np.array([2, 3, 6, 1])

    x_rot = generate_rotation_matrix_x(angle)
    y_rot = generate_rotation_matrix_y(angle)
    z_rot = generate_rotation_matrix_z(angle)

    rotated_xyz = apply_3d_rotation(x_rot, y_rot, z_rot, object_xyz)
    print("Rotated point:", rotated_xyz)

if __name__ == "__main__":
    # Run the demonstration
    main()



