from pylab import plot, show
from random import randint
from DiscreteDistribution import *

def convolve(a, b):
    # a, b - distributions
    
    new_distrib = [0. for i in range(len(b.values) - 1)]
    b_reversed = b.values[::-1]
    for val in a.values:
        new_distrib.append(0.)
        for j in range(len(b_reversed)):
            new_distrib[-j - 1] += val * b_reversed[j]
    
    return DiscreteDistribution(a.offset + b.offset, new_distrib)

def multiply(a, b):
    # a, b - distributions
    
    new_distrib = []

    min_index = min(a.start(), b.start())
    max_index = max(a.end(), b.end())
    
    for i in range(min_index, max_index):
        new_distrib.append(a.value(i) * b.value(i))

    normalizer = sum(new_distrib)

    for i in range(len(new_distrib)):
        new_distrib[i] /= normalizer
    
    return DiscreteDistribution(min_index, new_distrib)

def histogram_filter(belief, control, measurement):
    # belief - previous position
    # control - model of movement
    # measurement - measurement distribution
    
    prediction = convolve(belief, control)
    correction = multiply(prediction, measurement)
    return (prediction, correction)

def plot_distribution(distribution, arena, color = 'b', linestyle = 'steps'):
    plot([i + 0.5 for i in range(arena[0], arena[1])], [distribution.value(i) for i in range(arena[0], arena[1])], color = color, linestyle = linestyle)


if __name__ == '__main__':
    arena_1d = (0, 1000)
    
    start_position = 50

    position = DiscreteDistribution.unit_pulse(start_position)
    plot_distribution(position, arena_1d)

    # Generate controls and measurements

    controls  = [(100 + (-1) ** (randint(0, 1)) * randint(0, 5), 10)] * 10

    p = start_position
    measurements = []
    for c in controls:
        p += c[0]
        measurements.append((p + (-1) ** (randint(0, 1)) * randint(0, 5), 7))

    # Movement - measurement cycle

    for i in range(len(controls)):
        control = DiscreteDistribution.triangle(controls[i][0], controls[i][1])
        measurement = DiscreteDistribution.triangle(measurements[i][0], measurements[i][1])

        (prediction, position) = histogram_filter(position, control, measurement)

        plot_distribution(prediction, arena_1d, color = 'r')
        plot_distribution(measurement, arena_1d, color = 'g')
        plot_distribution(position, arena_1d)

    show()
