import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import cupy as cp

def load_yale_faces_dataset(path):
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
    images_1D = []
    for img in images_array:
        images_1D.append(img.reshape(-1))
    return images_1D

def get_mean_face_vector(images_array):
    mean_vector = np.zeros(images_array[0].shape, np.uint8)
    for img in images_array:    
        mean_vector += img    
    mean_vector = mean_vector/len(images_array)
    return mean_vector.astype(np.float16)

def mean_adjusted_face_vector(images_array, mean_face_vector):
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
    idx = eigenvalues.argsort()[::-1]   
    sorted_eigenvalues = eigenvalues[idx]
    sorted_eigenvectors = eigenvectors[:, idx]
    
    return sorted_eigenvalues[:k], sorted_eigenvectors[:,:k]

def projected_data(eigenvectors_k, mean_centered_data):
    projected_vector = np.dot(mean_centered_data, eigenvectors_k)
    return projected_vector