from math import exp, ceil

class DiscreteDistribution:
    def __init__(self, offset = 0, values = [1.0]):
        self.offset = offset
        self.values = values[:]

    def start(self):
        return self.offset

    def end(self):
        return self.offset + len(self.values)

    def normalize(self):
        s = float(sum(self.values))
        if s != 0.0:
            self.values = [i / s for i in self.values]

    def value(self, index):
        index -= self.offset
        if index < 0 or index >= len(self.values):
            return 0.0
        else:
            return self.values[index]

    @staticmethod
    def unit_pulse(center):
        return DiscreteDistribution(center, [1.0])

    @staticmethod
    def triangle(center, half_width):
        w = int(half_width)
        c = int(center)
        values = []
        for i in xrange(-w + 1, 0):
            values.append(w + i)
        for i in xrange(0, w):
            values.append(w-i)
        d = DiscreteDistribution(center - w + 1, values)
        d.normalize()
        return d

    @staticmethod
    def gaussian(mu, sigma):
        sigma2 = sigma * sigma
        extent = int(ceil(5 * sigma))
        values = []
        for x in xrange(mu - extent, mu + extent + 1):
            values.append(exp((-0.5 * (x - mu) ** 2) / sigma2))
        d = DiscreteDistribution(mu - extent, values)
        d.normalize()
        return d
