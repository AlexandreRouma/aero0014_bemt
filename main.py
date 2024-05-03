import os
import bemt
import numpy as np
import matplotlib.pyplot as plt
from utils.units import *
import time

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

# Simulation configuration
COLLECTIVE_PITCH_75 = 35

# Create output directory if it does not exist
if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

# Load airfoil
clarky = bemt.Airfoil('airfoils/clark-y')

# Configure blade
blade = bemt.Blade(BLADE_RADII, BLADE_TWISTS, BLADE_CHORDS, clarky)
collective = np.deg2rad(COLLECTIVE_PITCH_75 - np.rad2deg(blade.twist(0.75*BLADE_R)))

# Configure fluid
air = bemt.Fluid(AIR_DENSITY, AIR_DYN_VISCOSITY)

# Create simulation configuration
config = bemt.Configuration(blade, BLADE_COUNT, collective, 800, MPHtoMS(135), air)

# Run simulation reusing the last solution for faster convergence
results = bemt.solve(config)

# Print out results
print('Converged in', results.iterations, 'iterations.')
print('Thrust:\t', results.T)
print('Torque:\t', results.C)

thrustPower = results.T*config.freeStreamVelocity
torquePower = results.C*config.n*2.0*np.pi

print('Efficiency:\t', thrustPower/torquePower, thrustPower, torquePower)

