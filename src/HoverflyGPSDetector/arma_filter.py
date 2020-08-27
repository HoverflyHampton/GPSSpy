import numpy as np

class ARMA(object):
    def __init__(self, theta, phi, filter_len=5, ar_constant=0):
        self.epsilon = np.random.normal(size=len(theta)+1)
        self.filter_response = np.zeros(filter_len)
        self.theta = theta
        self.phi = phi
        self.ar_constant = ar_constant

    def advance_noise(self):
        next_epislon = np.random.normal()
        self.epsilon = np.roll(self.epsilon, 1)
        self.epsilon[0] = next_epislon

    def step(self):   
        self.advance_noise()
        next_x = (self.ar_constant + 
                  self.epsilon[0] + 
                  sum([self.theta[i]*self.epsilon[i+1] for i in range(len(self.theta))]) +
                  sum([self.phi[i]*self.filter_response[i] for i in range(len(self.phi))]))
        self.filter_response = np.roll(self.filter_response, 1)
        self.filter_response[0] = next_x
        return next_x

