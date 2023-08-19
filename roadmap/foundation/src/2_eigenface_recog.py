# Project 2: Eigenface Recognition

#     Objective: Use eigenvalues and eigenvectors to implement a basic face recognition system.
#     Skills Gained: Understanding of how eigen decomposition can be used in feature extraction and dimensionality reduction.
from roadmap.utils.utils import load_yale_faces_dataset \
                                ,convert_image_to_1D, \
                                eigen_decomposition, compute_covariance_matrix, top_k_eigenvalues,get_top_k, projected_data
import roadmap.utils.cache as cache
from sklearn.model_selection import train_test_split
import numpy as np

EIGEN_FILE = "roadmap/foundation/assets/eigen_save"  
load_from_cache = True

def main():
    images, labels = load_yale_faces_dataset("./roadmap/foundation/assets/data")
    print(f"Loaded {len(images)} images from the Yale Face Database.")

    # convert images to one-dimensional array
    images_1D = convert_image_to_1D(images)
    print(f"processed {len(images_1D)} images to 1D")

    eigenvalues = []
    eigenvectors = []
    cov_mat, mean_adjusted_array = compute_covariance_matrix(images_1D)

    if not load_from_cache:
        ## compute covariance matrix
        print(cov_mat.shape)

        # ## eigenvectors, values
        print("processing eigenvectors")
        eigenvectors, eigenvalues = eigen_decomposition(cov_mat)
        cache.save_to_pickle(EIGEN_FILE, eigenvalues, eigenvectors)
    else :
        eigenvectors, eigenvalues = cache.load_from_pickle(EIGEN_FILE)

    print("EIGENVEC ", eigenvectors.shape)
    print("EIGENVAL ",eigenvalues.shape)

    k = top_k_eigenvalues(eigenvalues)
    print("Top K values used ", k)

    eigenvalues_k , eigenvectors_k = get_top_k(eigenvalues, eigenvectors, k)
    print("top k values eigenvalues_k used ", eigenvalues_k.shape)
    print("top k values eigenvectors_k used ", eigenvectors_k.shape)


    # Assuming you've already computed eigenvectors_k somewhere earlier
    projected_all_data = projected_data(eigenvectors_k, mean_adjusted_array)
    print("projected_eigenvector used ", projected_all_data.shape)


    ### what you have done so far is PCA

    # Split the reduced data and corresponding labels into training and testing sets
    X_train, X_test, labels_train, labels_test = train_test_split(projected_all_data, labels, test_size=0.2, random_state=42)

    # Compute average representations for each label in the training set
    unique_labels = np.unique(labels_train)
    average_representations = {}
    for label in unique_labels:
        label_data = X_train[labels_train == label]
        average_representations[label] = np.mean(label_data, axis=0)

    # Classification
    def classify(face, avg_reps):
        distances = {}
        for label, avg_rep in avg_reps.items():
            dist = np.linalg.norm(face - avg_rep)
            distances[label] = dist
        return min(distances, key=distances.get)
    
    predictions = [classify(face, average_representations) for face in X_test]
    
    # Evaluation
    correct_predictions = np.sum(np.array(predictions) == labels_test)
    accuracy = correct_predictions / len(labels_test)
    print(f"Eigenface recognition accuracy: {accuracy:.2f}")

if __name__ == '__main__':
    main()