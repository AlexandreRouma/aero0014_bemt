import numpy as np

# All values are given in the problem statement
PROP_D = 3.048
BLADE_R = PROP_D/2.0
BLADE_RADII = np.array([ 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0 ]) * BLADE_R
BLADE_CHORDS = np.array([ 0.036, 0.0525, 0.07, 0.076, 0.0735, 0.066, 0.0565, 0.045, 0.0 ]) * PROP_D
BLADE_TWISTS = np.arctan(np.array([ 0.67, 0.84, 0.94, 0.98, 1.02, 1.09, 1.125, 1.19, 1.255 ]) * PROP_D / (2.0*np.pi*BLADE_RADII))
BLADE_COUNT = 3