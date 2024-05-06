# BEMT Simulator Implementation

This software was written for the BEMT project of the AERO0014 Aerospace Propulsion class at the University of Liège.

## How to Install

### Step 1: Create a Virtual Environement
```
python -m venv .venv
```

### Step 2: Activate the Virtual Environment
On windows
```
.venv/Scripts/Activate.ps1
```

On unix (Linux, BSD and MacOS)
```
source .venv/bin/activate
```

### Step 3: Install dependencies
```
pip install -r ./requirements.txt
```

# How to Run
```
python ./main.py
```

# Viewing Results
The software creates the `output` directory to write out every plot. Non-plot results are printed directly to the terminal along with the progress.

# Source Structure
The structure of the code is as follows

* `airfoils` contains for the data for the airfoils to be used in simulation. At the moment, only the Clark-Y airfoil is provided
* `bemt` is the main python module responsible for implementing the BEMT method
* `experimental_data` contains data extracted from the NACA experiments from Biermann et al.
* `questions` contains the code used to generate the answer to each question of the statement.
* `statement` contains values given in the project statement
* `utils` contains various utility files
* `main.py` creates the `output` directory if it doesn't exist and calls every question code.

# Acknowledgements

The API of this BEMT library was inspired by the [Rotare](https://gitlab.uliege.be/rotare/rotare) project by Thomas Lamber.

Copyright(c) 2024 Alexandre Rouma