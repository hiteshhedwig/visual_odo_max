# The primary aim is to implement a basic Bayesian filter 
# to estimate the state of a system, especially when the 
# measurements from sensors (like cameras or lidars) are noisy 
# or uncertain. By the end of this module, 
# you should have a clear understanding of how Bayesian filters work 
# and be capable of implementing one

#  Bayes theorem, the geometry of changing beliefs  : https://www.youtube.com/watch?v=HZGCoVF3YvM

import numpy as np
import matplotlib.pyplot as plt


def bayes_theorem(prior, likelihood, evidence):
    return (likelihood * prior) / evidence

class VehicleMotionModel:
    def __init__(self, initial_position, velocity):
        self.position = initial_position
        self.velocity = velocity

    def move(self, time_interval):
        self.position += self.velocity * time_interval
        return self.position
    
class NoisySensor:
    def __init__(self, noise_std_dev):
        self.noise_std_dev = noise_std_dev

    def measure(self, true_position):
        return true_position + np.random.normal(0, self.noise_std_dev)

class BayesianFilter:
    def __init__(self, initial_estimate, initial_uncertainty):
        self.estimate = initial_estimate
        self.uncertainty = initial_uncertainty

    def predict(self, motion, motion_uncertainty):
        self.estimate += motion
        self.uncertainty += motion_uncertainty

    def update(self, measurement, measurement_uncertainty):
        # Compute Kalman Gain
        kalman_gain = self.uncertainty / (self.uncertainty + measurement_uncertainty)
        
        # Update estimate and uncertainty
        self.estimate = self.estimate + kalman_gain * (measurement - self.estimate)
        self.uncertainty = (1 - kalman_gain) * self.uncertainty



# Initialize vehicle and sensor
vehicle = VehicleMotionModel(0, 1)  # Start at position 0 with velocity 1
sensor = NoisySensor(0.5)  # Sensor with noise standard deviation of 0.5

# Initialize Bayesian filter
filter = BayesianFilter(0, 1)  # Initial estimate of position 0 with uncertainty 1

# Lists to store true positions, measurements, and estimates
true_positions = []
measurements = []
estimates = []

# Simulate for 100 time steps
for _ in range(100):
    # Move vehicle
    true_position = vehicle.move(1)
    true_positions.append(true_position)
    
    # Take measurement
    measurement = sensor.measure(true_position)
    measurements.append(measurement)
    
    # Prediction step
    filter.predict(1, 0.1)  # Predict motion of 1 with uncertainty 0.1
    
    # Update step
    filter.update(measurement, 0.5)  # Update with measurement and its uncertainty
    estimates.append(filter.estimate)

# Plot results
plt.plot(true_positions, label="True Position")
plt.plot(measurements, label="Measurements", linestyle="dotted")
plt.plot(estimates, label="Estimates", linestyle="dashed")
plt.legend()
plt.show()

    