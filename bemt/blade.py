import numpy as np
import scipy.interpolate as interp
from bemt.airfoil import *

class Blade:
    def __init__(self, radii, twists, chords, airfoil: Airfoil):
        # Check that there are the same number of radii, twists and chords
        if len(radii) != len(twists):
            raise "Wrong number of blade twists given"
        if len(radii) != len(chords):
            raise "Wrong number of blade chords given"
        
        # Save length of blade
        self.minRadius = np.min(radii)
        self.maxRadius = np.max(radii)
        self.length = self.maxRadius - self.minRadius
        
        # Save airfoil
        self.airfoil = airfoil

        # Create interpolators
        self.cinterp = interp.CubicSpline(radii, chords)
        self.tinterp = interp.CubicSpline(radii, twists)

    def twist(self, r: float):
        return self.tinterp(r)
    
    def chord(self, r: float):
        return self.cinterp(r)