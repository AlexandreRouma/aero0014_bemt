import numpy as np
import mat4py as m4p
import matplotlib.pyplot as plt
import scipy.interpolate as int

class Airfoil:
    def __init__(self, polarPath: str, geometryPath):
        # Load airfoil polars from MATLAB file
        mat = m4p.loadmat(polarPath)
        polarData = mat['polarData']

        # Create CL and CD interpolators
        self._clInt = int.RegularGridInterpolator((np.array(polarData['aoa'])[:, 0], np.array(polarData['reynolds'])), np.array(polarData['cl']), bounds_error=False, fill_value=None)
        self._cdInt = int.RegularGridInterpolator((np.array(polarData['aoa'])[:, 0], np.array(polarData['reynolds'])), np.array(polarData['cd']), bounds_error=False, fill_value=None)

        # Load airfoil geometry
        self._sect = np.loadtxt(geometryPath, skiprows=1)
        self._vps = len(self._sect)

        # Move section back by c/4
        for i in range(self._vps):
            self._sect[i][0] = -self._sect[i][0]

    def cl(self, alpha: float, Re: float):
        return self._clInt((alpha, Re))

    def cd(self, alpha: float, Re: float):
        return self._cdInt((alpha, Re))
    
    def plot(self, x, y, scale, rotation):
        # Create transformation matrix
        A = np.array([
            [ np.cos(rotation), -np.sin(rotation) ],
            [ np.sin(rotation),  np.cos(rotation) ]
        ]) * scale

        # Transform geometry
        sect = np.zeros((self._vps, 2))
        offset = np.array([x,y])
        for i in range(self._vps):
            sect[i] = np.dot(A, self._sect[i]) + offset

        # Append first vertex to close the loop
        sect = np.vstack([sect, sect[0]])

        # Plot the geometry
        plt.plot(sect[:,0], sect[:,1], color='black')