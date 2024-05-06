import os
import bemt
import time
from statement.propeller import *
from questions.q0 import *
from questions.q1 import *
from questions.q2 import *
from questions.q3 import *

# Simulation Configuration
OUTPUT_DIR  = 'output'
AIR_DENSITY = 1.2255
AIR_DYN_VISCOSITY = 1.789e-5

# Create output directory if it does not exist
if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

# Load airfoil
clarky = bemt.Airfoil('airfoils/clarky/polars.mat', 'airfoils/clarky/geometry.dat')

# Configure blade
blade = bemt.Blade(BLADE_RADII, BLADE_TWISTS, BLADE_CHORDS, clarky)

# Configure fluid
air = bemt.Fluid(AIR_DENSITY, AIR_DYN_VISCOSITY)

# Start timer
startTime = time.time()

# Run Question 0
print('========== QUESTION 0 ==========')
Q0(OUTPUT_DIR, blade, air)
print('')

# Run Question 1
print('========== QUESTION 1 ==========')
Q1(OUTPUT_DIR, blade, air)
print('')

# Run Question 2
print('========== QUESTION 2 ==========')
Q2(OUTPUT_DIR, blade, air)
print('')

# Run Question 3
print('========== QUESTION 3 ==========')
Q3(OUTPUT_DIR, blade, air)
print('')

# Stop timer
stopTime = time.time()

# Print some useful statistics
print('========== STATISTICS ==========')
print('Computation Time: %s s' % (stopTime - startTime))