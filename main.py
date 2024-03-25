import os

# Configuration
OUTPUT_DIR  = 'output'

# Create output directory if it does not exist
if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)