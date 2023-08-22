import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

# Function to plot 2D Gaussian with given mean and covariance matrix
def plot_2d_gaussian(mean, cov_matrix):
    # Generate grid of points
    x, y = np.mgrid[-3:3:.01, -3:3:.01]
    pos = np.dstack((x, y))
    
    # Evaluate the Gaussian distribution on the grid
    rv = multivariate_normal(mean, cov_matrix)
    plt.contourf(x, y, rv.pdf(pos), levels=50, cmap="viridis")
    
    # Plot settings
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("2D Gaussian Distribution")
    plt.colorbar(label="Probability Density")
    plt.axis("equal")
    plt.show()

# Mean vector
mean = [0, 0]

# Different covariance matrices to visualize
cov1 = [[1, 0], [0, 1]]
cov2 = [[1, 0.8], [0.8, 1]]
cov3 = [[1, -0.8], [-0.8, 1]]

# Plot Gaussian distributions
print("Circular (Independent Variables):")
plot_2d_gaussian(mean, cov1)

print("Positive Covariance (Tilted Counterclockwise):")
plot_2d_gaussian(mean, cov2)

print("Negative Covariance (Tilted Clockwise):")
plot_2d_gaussian(mean, cov3)


# Fixed mean
mean = [0, 0]

# Different covariance matrices
cov1 = [[1, 0], [0, 1]]  # Circle (equal variances, zero covariance)
cov2 = [[2, 0], [0, 0.5]]  # Ellipse oriented along axes (different variances, zero covariance)
cov3 = [[2, 1], [1, 2]]  # Tilted ellipse (positive covariance)
cov4 = [[2, -1], [-1, 2]]  # Opposite tilted ellipse (negative covariance)

distributions = [cov1, cov2, cov3, cov4]

plt.figure(figsize=(10, 8))

for i, cov in enumerate(distributions, 1):
    x, y = np.random.multivariate_normal(mean, cov, 5000).T
    plt.subplot(2, 2, i)
    plt.scatter(x, y, s=2, alpha=0.6)
    plt.xlim(-8, 8)
    plt.ylim(-8, 8)
    plt.title(f"Covariance Matrix:\n{cov}")

plt.tight_layout()
plt.show()