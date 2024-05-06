# BEMT Simulator Implementation

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

# Acknowledgements

This software was written for the BEMT project of the AERO0014 Aerospace Propulsion class at the University of Liège. It's API was inspired by the [Rotare](https://gitlab.uliege.be/rotare/rotare) project by Thomas Lamber.

Copyright(c) 2024 Alexandre Rouma