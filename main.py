import os
from airfoil import *

# Configuration
OUTPUT_DIR  = 'output'

# Create output directory if it does not exist
if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

# Load airfoil polar
POLARS = {
    0.1e6: 'airfoil_polars/Polar_0.1e6_clark_y.txt',
    0.2e6: 'airfoil_polars/Polar_0.2e6_clark_y.txt',
    0.5e6: 'airfoil_polars/Polar_0.5e6_clark_y.txt',
    1e6: 'airfoil_polars/Polar_1e6_clark_y.txt',
    2e6: 'airfoil_polars/Polar_2e6_clark_y.txt',
    5e6: 'airfoil_polars/Polar_5e6_clark_y.txt',
    10e6: 'airfoil_polars/Polar_10e6_clark_y.txt',
}
af = Airfoil(POLARS)