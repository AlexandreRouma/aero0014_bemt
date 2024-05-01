class Fluid:
    def __init__(self, density, viscosity):
        self.density = density
        self.viscosity = viscosity

    def setDensity(self, density):
        self.density = density

    def setViscosity(self, viscosity):
        self.viscosity = viscosity