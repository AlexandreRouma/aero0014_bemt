import numpy as np
import copy
from bemt.blade import *
from bemt.fluid import *
from bemt.solution import *
from bemt.configuration import *

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
        sol.va2 = 0.5*(config.freeStreamVelocity + sol.va3)
        sol.vu2 = 0.5*sol.vu2p
        sol.wu2 = sol.vu2 - config.Omegar

        # Compute the local mass flow
        dmn = 2*np.pi*config.r*config.dr*config.fluid.density*sol.va2

        # Compute the velocity magnitude and flow angle
        w2n = np.sqrt(sol.va2**2 + sol.wu2**2)
        beta2n = np.arctan(sol.wu2 / sol.va2)

        # Compute the angle of attack and reynolds number
        AOAn = config.X - (0.5*np.pi + beta2n)
        Ren = config.fluid.density*w2n*config.C / config.fluid.viscosity

        # Compute the lift and drag coefficients
        CL = config.blade.airfoil.cl(AOAn, Ren)
        CD = config.blade.airfoil.cd(AOAn, Ren)

        # Clamp reynolds to supported values
        #Ren = np.clip(Ren, 1e4, 1e7)
        #CL, CD = clarkypolarsRe(AOAn, Ren)

        # Compute the local lift and drag
        sol.dL = 0.5*config.fluid.density*config.C*config.dr*CL*(w2n**2)
        sol.dD = 0.5*config.fluid.density*config.C*config.dr*CD*(w2n**2)

        # Compute the local thrust and torque
        sol.dT = -config.bladeCount*(sol.dL*np.sin(beta2n) + sol.dD*np.cos(beta2n))
        dFun = config.bladeCount*(sol.dL*np.cos(beta2n) - sol.dD*np.sin(beta2n))
        sol.dC = config.r*dFun

        # Compute new estimate for the velocity components
        va3n1 = config.freeStreamVelocity + sol.dT/dmn
        vu2pn1 = dFun / dmn

        # Compute total thrust and torque
        sol.T = 0
        sol.C = 0
        for i in range(config.elemCount - 1):
            sol.T += 0.5*(sol.dT[i] + sol.dT[i+1])
            sol.C += 0.5*(sol.dC[i] + sol.dC[i+1])

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

    # If the convergence was successful, compute the remaining values
    if sol.converged:
        # Compute the shaft power
        sol.dP = 2.0*np.pi*config.n*sol.dC
        sol.P = 2.0*np.pi*config.n*sol.C

        # Compute the efficiency
        sol.eta = (config.freeStreamVelocity*sol.T) / sol.P
    
    # Return solution
    return sol
