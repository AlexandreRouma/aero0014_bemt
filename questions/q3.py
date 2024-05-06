import bemt
import matplotlib.pyplot as plt
from statement.propeller import *
from utils.units import *
from utils.collective_pitch import *

def Q3(outPath: str, blade: bemt.Blade, air: bemt.Fluid):
    # Compute for a range of velocities
    vs = np.linspace(40, 220, 100)

    vvs = []
    tthetas = []
    effs = []

    for v in vs:
        # Find interval containing the pitch at which the shaft power is 275 HP
        hp275 = HPtoW(275)
        thetaLow = -1
        thetaHigh = -1
        thetas = np.linspace(10, 90, 19)
        res = None
        for theta in thetas:
            # Compute results
            config = bemt.Configuration(blade, 3, collectivePitch(blade, 0.75*BLADE_R, theta), 800, MPHtoMS(v), air)
            res = bemt.solve(config, initialSolution=(res if res != None and res.converged else None))

            # If no convergence, go to the next pitch
            if not res.converged or res.eta < 0.0 or res.eta >= 1.0:
                continue

            # If the upper bound is reached, save it and stop searching
            if res.P > hp275:
                thetaHigh = theta
                break
            
            # Save lower bound
            thetaLow = theta
        
        # If no interval is found, give up
        if thetaLow < 0 or thetaHigh < 0:
            print('Nothing found for %s' % (v))
            continue
        print('Found for', v)

        # Use bisection to find exact value
        eff = 0
        for i in range(100):
            # Compute midpoint
            t = 0.5*(thetaLow + thetaHigh)

            # Compute results
            config = bemt.Configuration(blade, 3, collectivePitch(blade, 0.75*BLADE_R, t), 800, MPHtoMS(v), air)
            res = bemt.solve(config, initialSolution=(res if res != None and res.converged else None))
            eff = res.eta

            # Update bounds
            if res.P > hp275:
                thetaHigh = t
            else:
                thetaLow = t

        vvs.append(v)
        tthetas.append(0.5*(thetaLow + thetaHigh))
        effs.append(eff)
    
    plt.plot(vvs, tthetas)
    plt.xlabel('Free-Stream Velocity [mph]')
    plt.ylabel('Collective Pitch [°]')
    plt.savefig(outPath + '/q3_colpitch.png', bbox_inches='tight')
    plt.close()

    plt.plot(vvs, effs*100.0)
    plt.xlabel('Free-Stream Velocity [mph]')
    plt.ylabel('Efficiency [%]')
    plt.savefig(outPath + '/q3_efficiency.png', bbox_inches='tight')
    plt.close()