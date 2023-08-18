import cv2
from matplotlib import pyplot as plt
import numpy as np
import os

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

            img = cv2.resize(img, (320,320))
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
    return mean_vector.astype(np.uint8)

def get_sub_mean_face_vector(images_array, mean_face_vector):
    for idx, fv in enumerate(images_array):
        images_array[idx] -= mean_face_vector
    return images_array