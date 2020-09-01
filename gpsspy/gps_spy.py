import numpy as np

class GPSSpy(object):
    def __init__(self, signal_len, num_sats, threshold=40000):
        """Tracks signals from a gps reciever in order to determine if it is being jammed 

        Args:
            signal_len (int): The Number of datapoints to store for each satallite
            num_sats (int): The maximum number of satallites in the constilation
        """         
        self.num_sats = num_sats
        self.signal_len = signal_len
        self.signal = np.zeros((num_sats, signal_len))
        self.decision_variable = 0
        self.initialized = False
        self._num_steps = 0
        self.threshold = threshold
        self.jammed = False

    def step(self, c_n_inputs):
        """Advances the detector by a single step, and returns the filtered variable.

        The detector is looking for changes in the C/No values, and will return a low value if
        there is little change, or a large number (~> 40000) if there is a change in value

        Args:
            c_n_inputs (np.array<int>): Array of C/No values for each satallite in the constellation, indexed by id.

        Returns:
            int: A decision value
        """        
        self.signal = np.roll(self.signal, 1, axis=1)
        self.signal[:, 0] = c_n_inputs
        self._num_steps += 1

        self.decision_variable = sum([sum([self.signal[i, k] - 
                                            ((1.0/self.signal_len) * sum([self.signal[i, m] 
                                            for m in range(self.signal_len)])) 
                                        for i in range(self.num_sats)])**2 
                                    for k in range(self.signal_len)])

        if not self.initialized and self._num_steps > self.signal_len*2 and self.decision_variable < 1000:
            self.initialized = True
        
        if self.initialized and self.decision_variable > self.threshold:
            self.jammed = not self.jammed
            self.initialized = False
            self._num_steps = 0
        
        return self.decision_variable


