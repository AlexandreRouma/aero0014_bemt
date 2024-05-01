import os
import bemt
import numpy as np
import matplotlib.pyplot as plt

# Simulation Configuration
OUTPUT_DIR  = 'output'
AIR_DENSITY = 1.225
AIR_DYN_VISCOSITY = 1.789e-5

# Propeller Configuration
PROP_D = 3.048
BLADE_R = PROP_D/2.0
BLADE_RADII = np.array([ 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9 ]) * BLADE_R
BLADE_CHORDS = np.array([ 0.036, 0.0525, 0.07, 0.076, 0.0735, 0.066, 0.0565, 0.045 ]) * PROP_D
BLADE_TWISTS = np.arctan(np.array([ 0.67, 0.84, 0.94, 0.98, 1.02, 1.09, 1.125, 1.19 ]) * PROP_D / (2.0*np.pi*BLADE_RADII))
BLADE_COUNT = 3

# Create output directory if it does not exist
if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

# Load airfoil
clarky = bemt.Airfoil('airfoils/clark-y')

# Configure blade
blade = bemt.Blade(BLADE_RADII, BLADE_TWISTS, BLADE_CHORDS, clarky)

# Configure fluid
air = bemt.Fluid(AIR_DENSITY, AIR_DYN_VISCOSITY)

# Create simulation configuration
config = bemt.Configuration(blade, BLADE_COUNT, 800, 40.2336, air)

# Run simulation
results, relErr = bemt.solve(config)

plt.plot(relErr)
plt.show()

# In case of non-convergence, print an error and exit
if not results.converged:
    print('Solution did not converge')
    exit(-1)

# Print out results
print('Converged in', results.iterations, 'iterations.')
print('Thrust:\t', results.T)
print('Torque:\t', results.C)
print('Efficiency:\t', (results.T*config.freeStreamVelocity) / (results.C*config.n*2.0*np.pi))

