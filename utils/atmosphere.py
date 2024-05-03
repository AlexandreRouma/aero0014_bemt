import numpy as np
from physics import *
from units import *

# Source for this equation: https://en.wikipedia.org/wiki/Barometric_formula

# Values at reference altitude (sea level)
Pb = 101325.0
T_Mb = 288.15
L_Mb = 0.0065
H_b = 0

"""
Compute the temperature at a given altitude in the atmosphere

Parameters
----------
altitude: Altitude in meters

Returns
-------
Temperature in Kelvin

"""
def temperature(altitude):
    return T_Mb - L_Mb*(altitude - H_b)

"""
Compute the pressure at a given altitude in the atmosphere

Parameters
----------
altitude: Altitude in meters

Returns
-------
Pressure in Pascal

"""
def pressure(altitude):
    return Pb * np.power(T_Mb/(T_Mb + L_Mb*(altitude - H_b)), (g*M_air)/(R*L_Mb))

"""
Compute the density of the atmosphere at a given altitude

Parameters
----------
altitude: Altitude in meters

Returns
-------
Density in kg/m^3

"""
def density(altitude):
    T = temperature(altitude)
    P = pressure(altitude)
    return M_air*P/(R*T)

