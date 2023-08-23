# The primary aim is to implement a basic Bayesian filter 
# to estimate the state of a system, especially when the 
# measurements from sensors (like cameras or lidars) are noisy 
# or uncertain. By the end of this module, 
# you should have a clear understanding of how Bayesian filters work 
# and be capable of implementing one

#  Bayes theorem, the geometry of changing beliefs  : https://www.youtube.com/watch?v=HZGCoVF3YvM

import numpy as np
import math

class VehicleMotionModel:
    def __init__(self, initial_state):
        # Initial state is [x, y, theta]
        self.state = initial_state

    def move(self, control_input):
        # Control input is [distance, delta_theta]
        d, delta_theta = control_input

        # Update state based on motion model
        self.state[0] += d * math.cos(self.state[2] + delta_theta)
        self.state[1] += d * math.sin(self.state[2] + delta_theta)
        self.state[2] += delta_theta

        # Normalize theta to be between -pi and pi
        self.state[2] = (self.state[2] + math.pi) % (2 * math.pi) - math.pi

        return self.state


class VehicleMeasurementModel:
    def __init__(self, gps_variance, theta_variance):
        """
        Initialize the measurement model with GPS and theta variance.
        
        :param gps_variance: Variance of the GPS sensor for position measurements.
        :param theta_variance: Variance of the compass/IMU for orientation measurements.
        """
        self.gps_variance = gps_variance
        self.theta_variance = theta_variance

    def likelihood(self, true_state, measured_state):
        """
        Compute the likelihood of a measured state given a true state.
        
        :param true_state: Estimated true state [x, y, theta].
        :param measured_state: State reported by the sensors [x, y, theta].
        :return: Likelihood value.
        """
        # Compute likelihood for position measurements
        gps_likelihood = (1 / (2 * np.pi * self.gps_variance)) * \
                         np.exp(-0.5 * ((measured_state[0] - true_state[0])**2 + 
                                        (measured_state[1] - true_state[1])**2) / self.gps_variance)
        
        # Compute likelihood for orientation measurement
        theta_diff = (measured_state[2] - true_state[2] + np.pi) % (2 * np.pi) - np.pi
        theta_likelihood = (1 / np.sqrt(2 * np.pi * self.theta_variance)) * \
                           np.exp(-0.5 * (theta_diff ** 2) / self.theta_variance)
        
        # Combine the likelihoods (assuming independence between position and orientation measurements)
        return gps_likelihood * theta_likelihood


if __name__ == "__main__":
    vehicle = VehicleMotionModel([0, 0, 0])  # Starting at (0, 0) with a heading of 0 radians
    new_state = vehicle.move([5, math.pi/4])  # Move forward by 5 units and turn by 45 degrees
    print(new_state)

    # Example usage:
    gps_variance = 2.0  # Assume the GPS has a variance of 2.0 units^2 for position measurements
    theta_variance = 0.1  # Assume the compass/IMU has a variance of 0.1 rad^2
    model = VehicleMeasurementModel(gps_variance, theta_variance)

    # Simulate a measurement around the true state
    true_state = new_state
    measured_state = [np.random.normal(true_state[0], np.sqrt(gps_variance)),
                    np.random.normal(true_state[1], np.sqrt(gps_variance)),
                    np.random.normal(true_state[2], np.sqrt(theta_variance))]

    # Compute the likelihood of the measured state given the true state
    likelihood = model.likelihood(true_state, measured_state)
    print(f"Likelihood of measured state given true state: {likelihood}")
