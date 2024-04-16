import os
import numpy as np
import matplotlib.pyplot as plt

# List polar files
files = os.listdir('./airfoil_polars')
polars = []
for f in files:
    if f.startswith('Polar'):
        polars.append(f)

for path in polars:
    polar = np.loadtxt('./airfoil_polars/'+path, skiprows=12)
    if len(polar.shape) != 2:
        continue
    alphas = polar[:,0]
    cls = polar[:,1]
    cds = polar[:,2]
    cms = polar[:,2]
    plt.plot(alphas, cds, label=path)
plt.legend()
plt.xlabel('Cd')
plt.ylabel('Cl')
plt.show()