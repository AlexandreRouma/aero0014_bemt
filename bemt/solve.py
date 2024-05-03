import numpy as np
import copy
from bemt.blade import *
from bemt.fluid import *
from bemt.solution import *
from bemt.configuration import *
from bemt.vendor.clarkypolarsRe import *

def solve(config: Configuration, convergenceTolerance: float = 0.0001, maxIterations: int = 500, initialSolution: Solution = None):
    # Init solution to either a new one or the privided initial guess
    sol = None
    if initialSolution != None:
        sol = copy.deepcopy(initialSolution)
        sol.iterations = 0
        sol.converged = False
    else:
        sol = Solution(config.elemCount, config.freeStreamVelocity)

    # Solve iteratively
    for it in range(maxIterations):
        # Compute velocity components at disk
        va2n = 0.5*(config.freeStreamVelocity + sol.va3)
        vu2n = 0.5*sol.vu2p
        wu2n = vu2n - config.Omegar

        # Compute the local mass flow
        dmn = 2*np.pi*config.r*config.dr*config.fluid.density*va2n

        # Compute the velocity magnitude and flow angle
        w2n = np.sqrt(va2n**2 + wu2n**2)
        beta2n = np.arctan(wu2n / va2n)

        # Compute the angle of attack and reynolds number
        AOAn = config.X - (0.5*np.pi + beta2n)
        Ren = config.fluid.density*w2n*config.C / config.fluid.viscosity

        # Compute the lift and drag coefficients
        # CL = config.blade.airfoil.cl(AOAn, Ren)
        # CD = config.blade.airfoil.cd(AOAn, Ren)
        CL, CD = clarkypolarsRe(AOAn, Ren)

        # Compute the local lift and drag
        dLn = 0.5*config.fluid.density*config.C*config.dr*CL*(w2n**2)
        dDn = 0.5*config.fluid.density*config.C*config.dr*CD*(w2n**2)

        # Compute the local thrust and torque
        dTn = -config.bladeCount*(dLn*np.sin(beta2n) + dDn*np.cos(beta2n))
        dFun = config.bladeCount*(dLn*np.cos(beta2n) - dDn*np.sin(beta2n))
        dCn = config.r*dFun

        # Compute new estimate for the velocity components
        va3n1 = config.freeStreamVelocity + dTn/dmn
        vu2pn1 = dFun / dmn

        # Compute total thrust and torque
        sol.T = 0
        sol.C = 0
        for i in range(config.elemCount - 1):
            sol.T += 0.5*(dTn[i] + dTn[i+1])
            sol.C += 0.5*(dCn[i] + dCn[i+1])

        # Compute relative error
        relErrVa3 = np.abs((va3n1 / sol.va3) - 1)
        relErrVu2p = np.abs((vu2pn1 / sol.vu2p) - 1)
        maxRelErr = np.max([ np.max(relErrVa3), np.max(relErrVu2p) ]) # TODO: Find faster way

        # Update solution
        sol.va3 = va3n1
        sol.vu2p = vu2pn1

        # If it converged enough, mark as converged and stop iterating
        if maxRelErr < convergenceTolerance:
            sol.converged = True
            sol.iterations = it+1
            break
    
    # Return solution
    return sol
