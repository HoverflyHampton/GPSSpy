import numpy as np
from arma_filter import ARMA


class GPSSpy(object):
    def __init__(self, signal_len, num_sats, filter_len=5, beta=0.5):
        self.num_sats = num_sats
        self.signal_len = signal_len
        self.signal = np.zeros((num_sats, signal_len))
        self.filter = ARMA([1-beta], [1, -beta], filter_len=filter_len)
        self.decision_variable = 0

    def step(self, c_n_inputs):
        self.filter.step()
        self.signal = np.roll(self.signal, 1, axis=1)
        self.signal[:, 0] = c_n_inputs

        # self.decision_variable = sum([sum([self.signal[i, k] - 
        #                                     ((1.0/self.signal_len) * sum([self.signal[i, m] 
        #                                     for m in range(self.signal_len)])) 
        #                                 for i in range(self.num_sats)])**2 
        #                             for k in range(self.signal_len)])
        # return self.decision_variable

        conv = [np.convolve(self.filter.filter_response, self.signal[i, :]) 
                for i in range(self.num_sats)]
        self.decision_variable = sum([sum([self.signal[i, n] - conv[i][n] 
                                           for i in range(self.num_sats)])**2
                                      for n in range(self.signal_len)])

        
        return self.decision_variable


