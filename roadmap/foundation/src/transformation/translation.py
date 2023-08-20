# Definition: Translation refers to the process of moving a 3D object linearly from one location in the space to another without altering its orientation or size.
# Key Concepts:
# Vector Movement: The translation of an object is determined by a vector. This vector provides the direction and magnitude (distance) for the translation.
# Transformation Matrix: In linear algebra, the translation of a 3D object can be achieved using a 4x4 matrix. When this matrix multiplies the homogeneous coordinates of the object, it results in a translated object.
# Applications: Translation is often used in animations where an object needs to move from one location to another or in scenarios like camera movement in 3D visualization tools.


# The translation matrix in a 3D space is a 4x4 matrix that 
# is used to move an object to a new position in the 3D space. 
# Given a translation vector [Tx,Ty,Tz], the translation 
# matrix TT in homogeneous coordinates
import numpy as np

def generate_translation_matrix(tx, ty, tz, is_homogeneous=False):
    """
    Generates a translation matrix based on the given translations along the X, Y, and Z axes.
    
    Args:
    - tx (float): Translation along the X-axis.
    - ty (float): Translation along the Y-axis.
    - tz (float): Translation along the Z-axis.
    - is_homogeneous (bool): If True, returns a 4x4 matrix, otherwise a 3x1 vector.

    Returns:
    - np.array: A translation matrix or vector.
    """
    if is_homogeneous:
        return np.array([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1]
        ])
    else:
        return np.array([tx, ty, tz])

def apply_translation_to_point(translation, point):
    """
    Applies the translation to a 3D point.

    Args:
    - translation (np.array): The translation matrix or vector.
    - point (np.array): The 3D point.

    Returns:
    - np.array: The translated 3D point.
    """
    if len(translation) == 4:  # Homogeneous matrix
        return np.dot(translation, point)
    else:  # Regular 3D translation
        return point + translation

def apply_translation_to_points(tx, ty, tz, points, is_homogeneous=False):
    """
    Applies the translation to an array of 3D points.

    Args:
    - tx (float): Translation along the X-axis.
    - ty (float): Translation along the Y-axis.
    - tz (float): Translation along the Z-axis.
    - points (list): List of 3D points.
    - is_homogeneous (bool): If True, uses homogeneous coordinates.

    Returns:
    - list: List of translated 3D points.
    """
    translation = generate_translation_matrix(tx, ty, tz, is_homogeneous)
    return [apply_translation_to_point(translation, point) for point in points]

def translate_points_based_on_mouse_movement_(deltaX, deltaY, points):
    return apply_translation_to_points(deltaX/1000, deltaY/1000, 0, points)


def main():
    # A 3D point in homogeneous coordinates [X,Y,Z,1]
    point_homogeneous = np.array([2, 3, 6, 1])

    # Apply the translation to the 3D point
    translated_point = apply_translation_to_point(generate_translation_matrix(3, 5, 2,is_homogeneous=True), point_homogeneous)

    print(translated_point)

if __name__ == '__main__':
    main()
