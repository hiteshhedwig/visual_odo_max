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

def get_translation_matrix(Tx, Ty, Tz):
    """
    Generates a 4x4 translation matrix based on the given translations along the X, Y, and Z axes.
    
    Args:
    - Tx (float): Translation along the X-axis.
    - Ty (float): Translation along the Y-axis.
    - Tz (float): Translation along the Z-axis.

    Returns:
    - np.array: A 4x4 translation matrix.
    """
    return np.array([
                    [1, 0, 0, Tx],
                    [0, 1, 0, Ty],
                    [0, 0, 1, Tz],
                    [0, 0, 0, 1]
                ])

def apply_translation(translation_matrix, object_xyz_homogeneous):
    """
    Applies the translation to a 3D point (in homogeneous coordinates) using the translation matrix.

    Args:
    - translation_matrix (np.array): The 4x4 translation matrix.
    - object_xyz_homogeneous (np.array): The 3D point in homogeneous coordinates.

    Returns:
    - np.array: The translated 3D point.
    """
    return np.dot(translation_matrix, object_xyz_homogeneous)

def main():
    # A 3D point in homogeneous coordinates [X,Y,Z,1]
    object_xyz_homogeneous = np.array([2, 3, 6, 1])

    # Get a translation matrix
    translation_matrix = get_translation_matrix(3, 5, 2)

    # Apply the translation to the 3D point
    translated_object_xyz = apply_translation(translation_matrix, object_xyz_homogeneous)

    print(translated_object_xyz)


if __name__ == '__main__':
    main()