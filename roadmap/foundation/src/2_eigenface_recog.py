# Project 2: Eigenface Recognition

#     Objective: Use eigenvalues and eigenvectors to implement a basic face recognition system.
#     Skills Gained: Understanding of how eigen decomposition can be used in feature extraction and dimensionality reduction.
from roadmap.utils.utils import load_yale_faces_dataset \
                                ,convert_image_to_1D, get_mean_face_vector, get_sub_mean_face_vector



def main():
    images, labels = load_yale_faces_dataset("./roadmap/foundation/assets/data")
    print(f"Loaded {len(images)} images from the Yale Face Database.")

    # convert images to one-dimensional array
    images_1D = convert_image_to_1D(images)
    print(f"processed {len(images_1D)} images to 1D")

    # Mean Calculation
    mean_face_vector = get_mean_face_vector(images_1D)
    # Subtract mean face from each face vector to the center of the data
    sub_mean = get_sub_mean_face_vector(images_1D, mean_face_vector)
    print(len(sub_mean))

if __name__ == '__main__':
    main()