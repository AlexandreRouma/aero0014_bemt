import numpy as np
from bemt.blade import *
from bemt.fluid import *

class Configuration:
    def __init__(self, blade: Blade, bladeCount: int, collectivePitch: float, rotationSpeed: float, freeStreamVelocity: float, fluid: Fluid, elemCount: int = 50):
        # Save configuration
        self.blade = blade
        self.bladeCount = bladeCount
        self.collectivePitch = collectivePitch
        self.rotationSpeed = rotationSpeed
        self.freeStreamVelocity = freeStreamVelocity
        self.fluid = fluid
        self.elemCount = elemCount
        
        # Generate blade elements
        self.__generateElements()

    def setBlade(self, blade: Blade):
        # Save blade
        self.blade = blade

        # Regenerate elements
        self.__generateElements()

    def setBladeCount(self, bladeCount):
        self.bladeCount = bladeCount

    def setCollectivePitch(self, collectivePitch):
        # Save value
        self.collectivePitch = collectivePitch

        # Regenerate elements
        self.__generateElements()

    def setRotationSpeed(self, rotationSpeed):
        # Save value
        self.rotationSpeed = rotationSpeed

        # Update rotation velocities at each radius
        self.__generateRotationVelocity()

    def setFreeStreamVelocity(self, freeStreamVelocity):
        self.freeStreamVelocity = freeStreamVelocity

    def setFluid(self, fluid):
        self.fluid = fluid

    def __generateElements(self):
        # Compute the radius of each element
        self.dr = self.blade.length / self.elemCount
        self.r = np.linspace(self.blade.minRadius, self.blade.maxRadius - self.dr, self.elemCount)

        # Compute twists
        self.X = self.blade.twist(self.r) + self.collectivePitch
        self.C = self.blade.chord(self.r)

        # Update rotation velocities at each radius
        self.__generateRotationVelocity()
    
    def __generateRotationVelocity(self):
        # Convert rotational speed from RPM to rotations per second
        self.n = self.rotationSpeed / 60

        # Compute the linear velocity at each radius
        self.Omegar = 2.0*np.pi*self.n*self.r