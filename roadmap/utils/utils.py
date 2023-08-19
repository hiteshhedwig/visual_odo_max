import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import cupy as cp

def load_yale_faces_dataset(path):
    """
    The function `load_yale_faces_dataset` loads images from a directory, resizes them to a specific
    size, and extracts labels from the filenames.
    
    :param path: The path parameter is the directory path where the Yale Faces dataset is stored. This
    function loads the images from the dataset and returns two arrays: images and labels. The images
    array contains the loaded images, and the labels array contains the corresponding labels (person's
    ID) for each image
    :return: The function load_yale_faces_dataset returns two numpy arrays: images and labels. The
    images array contains the loaded images from the specified path, while the labels array contains the
    corresponding labels (person's ID) for each image.
    """
    images = []
    labels = []
    
    # List all files in the directory
    for filename in os.listdir(path):
        if "subject" in filename:  # Check if the filename starts with 'subject'
            # Construct full file path
            filepath = os.path.join(path, filename)
            
            # Read the image using OpenCV (convert it to grayscale)
            print("loading file " + filepath)
            img = plt.imread(filepath)

            # Ensure the image data type is uint8
            img = np.uint8(img)

            img = cv2.resize(img, (92,92))
            # Append the image and its label to the lists
            print(img.shape)
            images.append(img)
            
            # Extract label (person's ID) from the filename
            label = int(filename.split(".")[0].replace("subject", ""))  # Convert 'subject01' to 1, 'subject02' to 2, etc.
            labels.append(label)
    
    return np.array(images), np.array(labels)

def convert_image_to_1D(images_array):
    """
    The function `convert_image_to_1D` takes an array of images and converts each image into a 1D array.
    
    :param images_array: The `images_array` parameter is a list of images. Each image is represented as
    a 2D array or matrix
    :return: a list of 1D arrays, where each array represents a flattened version of an image from the
    input images_array.
    """
    images_1D = []
    for img in images_array:
        images_1D.append(img.reshape(-1))
    return images_1D

def get_mean_face_vector(images_array):
    """
    The function calculates the mean face vector by summing up all the images in the array and dividing
    by the number of images.
    
    :param images_array: The `images_array` parameter is an array of images. Each image in the array
    should be a numpy array representing the pixel values of the image
    :return: the mean face vector, which is the average of all the face vectors in the images_array.
    """
    mean_vector = np.zeros(images_array[0].shape, np.uint8)
    for img in images_array:    
        mean_vector += img    
    mean_vector = mean_vector/len(images_array)
    return mean_vector.astype(np.float16)

def mean_adjusted_face_vector(images_array, mean_face_vector):
    """
    The function subtracts the mean face vector from each image in the images_array and returns the
    result.
    
    :param images_array: An array of face images. Each image is represented as a vector
    :param mean_face_vector: The mean_face_vector is a vector that represents the average face in the
    dataset. It is used to adjust each face vector in the images_array by subtracting the
    mean_face_vector from it. This helps to normalize the data and remove any bias caused by variations
    in lighting or other factors
    :return: the images_array after subtracting the mean_face_vector from it and converting the result
    to a numpy float16 data type.
    """
    images_array -= mean_face_vector
    return images_array.astype(np.float16)

def compute_covariance_matrix(images_array_1D):
    """
    The function computes the covariance matrix using the images array.
    
    :param images_array_1D: A 2D array where each row represents an image and each column represents a
    pixel value of that image. The shape of the array is (num_images, num_pixels)
    :return: the covariance matrix of the images array.
    """
    images_array_1D = np.array(images_array_1D)
    num_images = images_array_1D.shape[0]

    # Compute the mean face vector
    mean_face_vector = np.mean(images_array_1D, axis=0)

    # Subtract the mean face from each face vector to center the data
    mean_adjusted_array = images_array_1D - mean_face_vector

    # Compute the covariance matrix using the smaller-dimensional approach
    # This results in an MxM covariance matrix
    cov_matrix_small = np.dot(mean_adjusted_array.T, mean_adjusted_array) / (num_images - 1)
    return cov_matrix_small, mean_adjusted_array

def eigen_decomposition(covariance_matrix):
    """
    The function `eigen_decomposition` performs eigen decomposition on a given covariance matrix using
    CuPy library for GPU acceleration.
    
    :param covariance_matrix: The covariance_matrix parameter is a square matrix that represents the
    covariance between variables. It is typically a symmetric matrix where each element represents the
    covariance between two variables. The size of the matrix determines the number of variables being
    considered
    :return: the eigenvectors and eigenvalues of the input covariance matrix.
    """
    # Convert your NumPy array to a CuPy array
    covariance_matrix_gpu = cp.array(covariance_matrix)
    
    # Compute eigenvalues and eigenvectors on GPU
    eigenvalues_gpu, eigenvectors_gpu = cp.linalg.eigh(covariance_matrix_gpu)
    
    # Convert results back to NumPy arrays (if needed)
    eigenvalues = cp.asnumpy(eigenvalues_gpu)
    eigenvectors = cp.asnumpy(eigenvectors_gpu)
    
    return eigenvectors, eigenvalues

def top_k_eigenvalues(eigenvalues):
    """
    The function `top_k_eigenvalues` calculates the number of eigenvalues needed to explain at least 95%
    of the total variance.
    
    :param eigenvalues: The parameter "eigenvalues" is a list of eigenvalues
    :return: the value of k, which represents the number of eigenvalues needed to explain at least 95%
    of the total variance.
    """
    idx = eigenvalues.argsort()[::-1]   
    eigenvalues = eigenvalues[idx]
    
    total_variance = sum(eigenvalues)
    explained_variance = 0
    k = 0
    for i,_ in enumerate(eigenvalues):
        explained_variance += eigenvalues[i]
        if explained_variance / total_variance >= 0.95:  # for 95% explained variance
            k = i + 1
            break
    return k

def get_top_k(eigenvalues, eigenvectors, k):
    """
    The function `get_top_k` takes in a list of eigenvalues and eigenvectors, and returns the top k
    eigenvalues and corresponding eigenvectors.
    
    :param eigenvalues: The eigenvalues are the values that are obtained when solving the characteristic
    equation of a matrix. They represent the "importance" or "magnitude" of the corresponding
    eigenvectors
    :param eigenvectors: A matrix where each column represents an eigenvector of a given matrix
    :param k: The parameter "k" represents the number of top eigenvalues and eigenvectors that you want
    to retrieve
    :return: The function `get_top_k` returns two arrays: `sorted_eigenvalues` and
    `sorted_eigenvectors`. The `sorted_eigenvalues` array contains the top `k` eigenvalues, sorted in
    descending order. The `sorted_eigenvectors` array contains the corresponding eigenvectors for the
    top `k` eigenvalues.
    """
    idx = eigenvalues.argsort()[::-1]   
    sorted_eigenvalues = eigenvalues[idx]
    sorted_eigenvectors = eigenvectors[:, idx]
    
    return sorted_eigenvalues[:k], sorted_eigenvectors[:,:k]

def projected_data(eigenvectors_k, mean_centered_data):
    """
    The function `projected_data` calculates the projection of mean-centered data onto a set of
    eigenvectors.
    
    :param eigenvectors_k: The eigenvectors_k parameter represents the k eigenvectors that were obtained
    from performing principal component analysis (PCA) on a dataset. These eigenvectors represent the
    directions of maximum variance in the data
    :param mean_centered_data: The mean_centered_data parameter is a matrix where each row represents a
    data point and each column represents a feature. The data points have been mean-centered, meaning
    that the mean of each feature has been subtracted from each data point
    :return: the projected vector, which is the result of multiplying the mean-centered data by the
    eigenvectors.
    """
    projected_vector = np.dot(mean_centered_data, eigenvectors_k)
    return projected_vector