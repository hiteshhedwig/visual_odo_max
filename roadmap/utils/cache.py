import pickle

def save_to_pickle(name, eigenvalues, eigenvectors):
    print("saving to pickle ")
    with open(f'{name}.pkl', 'wb') as f:
        pickle.dump({'eigenvalues': eigenvalues, 'eigenvectors': eigenvectors}, f)

def load_from_pickle(name):
    with open(f'{name}.pkl', 'rb') as f:
        data = pickle.load(f)
        eigenvalues = data['eigenvalues']
        eigenvectors = data['eigenvectors']
        return eigenvectors, eigenvalues