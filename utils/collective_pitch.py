import numpy as np
import bemt

def collectivePitch(blade: bemt.Blade, position: float, desiredTwist: float):
    return np.deg2rad(desiredTwist - np.rad2deg(blade.twist(position)))