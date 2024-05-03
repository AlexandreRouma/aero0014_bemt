import numpy as np
import sys

class Solution:
    def __init__(self, elemCount: int, freeStreamVelocity: float):
        # Save config
        self.elemCount = elemCount

        # Reset state
        self.reset(freeStreamVelocity)
    
    def reset(self, freeStreamVelocity):
        # Allocate arrays for unknowns
        self.va3 = np.ones(self.elemCount)*freeStreamVelocity
        self.vu2p = np.ones(self.elemCount)*sys.float_info.epsilon
        self.T = 0.0
        self.C = 0.0

        # Mark as not converted
        self.iterations = 0
        self.converged = False