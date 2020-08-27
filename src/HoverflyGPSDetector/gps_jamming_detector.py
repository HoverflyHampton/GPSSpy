import numpy as np
from HoverflyGPSDetector.arma_filter import ARMA


class GPSSpy(object):
    def __init__(self, signal_len, num_sats, threshold=0.75,
                 filter_len=5, beta=0.75):
        self.num_sats = num_sats
        self.signal_len = signal_len
        self.signal = np.zeros((num_sats, signal_len))
        self.filter = ARMA([1-beta], [1, -beta], filter_len=filter_len)
        self.decision_variable = 0
        self.threshold = threshold

    def step(self, c_n_inputs):
        self.filter.step()
        np.roll(self.signal, 1, axis=1)
        self.signal[:, 0] = c_n_inputs
        conv = [np.convolve(self.filter.filter_response, self.signal[i, :]) 
                for i in self.num_sats if c_n_inputs[i] != 0]
        self.decision_variable = sum([sum([self.signal[i, n] - conv[i][n] 
                                           for i in range(self.num_sats) 
                                           if c_n_inputs[i] != 0])
                                      for n in range(self.signal_len)])

        return self.decision_variable < self.threshold


