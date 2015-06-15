from pylab import plot, show
from matplotlib.mlab import normpdf
from math import sqrt
from random import randint, random

class NormalDistribution:
    def __init__(self, mu, sigma2):
        self.mu = float(mu)
        self.sigma2 = float(sigma2)

def kalman_filter(belief, control, measurement):
    # belief - previous position
    # control - model of movement
    # measurement - measurement distribution
    
    prediction = NormalDistribution(belief.mu + control.mu, belief.sigma2 + control.sigma2)  # Motion

    K = prediction.sigma2 / (prediction.sigma2 + measurement.sigma2) # Kalman Gain
    correction = NormalDistribution(prediction.mu + K * (measurement.mu - prediction.mu), (1 - K) * prediction.sigma2)  # Measurement

    return (prediction, correction)

def plot_normal(normal, arena, color = 'b', linewidth = 3):
    plot([normpdf(x, normal.mu, sqrt(normal.sigma2)) for x in range(*arena)], color = color, linewidth = linewidth)


if __name__ == '__main__':
    arena_1d = (0, 1000)
    
    start_position = 50

    position = NormalDistribution(start_position, 1)
    plot_normal(position, arena_1d)

    # Generate controls and measurements

    controls  = [(100 + (-1) ** (randint(0, 1)) * random() * randint(0, 10), 10 ** 2)] * 10

    p = start_position
    measurements = []
    for c in controls:
        p += c[0]
        measurements.append((p + (-1) ** (randint(0, 1)) * random() * randint(0, 10), 7 ** 2))

    # Movement - measurement cycle

    for i in range(len(controls)):
        control = NormalDistribution(controls[i][0], controls[i][1])
        measurement = NormalDistribution(measurements[i][0], measurements[i][1])

        (prediction, position) = kalman_filter(position, control, measurement)

        plot_normal(prediction, arena_1d, color = 'r')
        plot_normal(measurement, arena_1d, color = 'g')
        plot_normal(position, arena_1d)

    show()
