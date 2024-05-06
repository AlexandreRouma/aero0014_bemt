import bemt
import numpy as np
import matplotlib.pyplot as plt
import copy
import experimental_data as exp
from statement.propeller import *
from utils.units import *
from utils.collective_pitch import *

def Q2(outPath: str, blade: bemt.Blade, air: bemt.Fluid):
    # Precompute 115mph in m/s
    mph115 = MPHtoMS(115)

    # Plot efficiency for various collective pitches
    ps = np.linspace(15, 45, 7)

    vars = []
    tcs = []
    pcs = []
    effs = []

    for p in ps:
        var = []
        tc = []
        pc = []
        eff = []
        res = None
        first = True

        # Simulate for various advance ratios
        print('[Q2] Computing for Theta_75 = %d°...' % (p))
        ars = np.linspace(0.01, 2.6, 1000)
        for ar in ars:
            # Choose rotationial and freestream velocities
            v = ar*(800*PROP_D/60)
            rpm = 800
            if v > mph115:
                # If airspeed to fast, reduce rpm instead
                v = mph115
                rpm = 60*v/(ar*PROP_D)

            # Compute results
            config = bemt.Configuration(blade, 3, collectivePitch(blade, 0.75*BLADE_R, p), rpm, v, air)
            res = bemt.solve(config, initialSolution=(res if res != None and res.converged else None))

            if not res.converged or res.eta < 0.0 or res.eta >= 1.0:
                continue

            # Compute thrust coefficient
            C_T = res.T / (config.fluid.density*(config.n**2)*(PROP_D**4))

            # Compute power coefficient
            C_P = res.P/((config.fluid.density)*(config.n**3)*((PROP_D)**5))
            
            # Save results
            var.append(ar)
            eff.append(res.eta*100.0)
            tc.append(C_T)
            pc.append(C_P)

        # Add result to map
        vars.append(copy.deepcopy(var))
        tcs.append(copy.deepcopy(tc))
        pcs.append(copy.deepcopy(pc))
        effs.append(copy.deepcopy(eff))
    
    # Plot thrust coefficient graph
    print('[Q2] Plotting thrust coefficient graph...')
    ax = plt.gca()
    ax.set_ylim([0, 0.22])
    for i in range(len(ps)):
        plt.plot(vars[i], tcs[i], label='$\\theta_{75}=%d$°' % (ps[i]))

    arExp = np.linspace(0, exp.NACA_THRUST_15_MAX, 1000)
    thrustExp = exp.NACAThrust15(arExp)
    plt.plot(arExp, thrustExp, '--', color='tab:blue')
    arExp = np.linspace(0, exp.NACA_THRUST_20_MAX, 1000)
    thrustExp = exp.NACAThrust20(arExp)
    plt.plot(arExp, thrustExp, '--', color='tab:orange')
    arExp = np.linspace(0, exp.NACA_THRUST_25_MAX, 1000)
    thrustExp = exp.NACAThrust25(arExp)
    plt.plot(arExp, thrustExp, '--', color='tab:green')
    arExp = np.linspace(0, exp.NACA_THRUST_30_MAX, 1000)
    thrustExp = exp.NACAThrust30(arExp)
    plt.plot(arExp, thrustExp, '--', color='tab:red')
    arExp = np.linspace(0, exp.NACA_THRUST_35_MAX, 1000)
    thrustExp = exp.NACAThrust35(arExp)
    plt.plot(arExp, thrustExp, '--', color='tab:purple')
    arExp = np.linspace(0, exp.NACA_THRUST_40_MAX, 1000)
    thrustExp = exp.NACAThrust40(arExp)
    plt.plot(arExp, thrustExp, '--', color='tab:brown')
    arExp = np.linspace(0, exp.NACA_THRUST_45_MAX, 1000)
    thrustExp = exp.NACAThrust45(arExp)
    plt.plot(arExp, thrustExp, '--', color='tab:pink')

    plt.xlabel('Advance Ratio [-]')
    plt.ylabel('Thrust Coefficient [-]')
    plt.legend()
    plt.savefig(outPath + '/q2_thrust_coef.png', bbox_inches='tight')
    plt.close()

    # Plot power coefficient graph
    print('[Q2] Plotting power coefficient graph...')
    ax = plt.gca()
    ax.set_ylim([0, 0.45])
    for i in range(len(ps)):
        plt.plot(vars[i], pcs[i], label='$\\theta_{75}=%d$°' % (ps[i]))

    arExp = np.linspace(0, exp.NACA_THRUST_15_MAX, 1000)
    thrustExp = exp.NACAThrust15(arExp)
    plt.plot(arExp, thrustExp, '--', color='tab:blue')
    arExp = np.linspace(0, exp.NACA_POWER_20_MAX, 1000)
    thrustExp = exp.NACAPower20(arExp)
    plt.plot(arExp, thrustExp, '--', color='tab:orange')
    arExp = np.linspace(0, exp.NACA_POWER_25_MAX, 1000)
    thrustExp = exp.NACAPower25(arExp)
    plt.plot(arExp, thrustExp, '--', color='tab:green')
    arExp = np.linspace(0, exp.NACA_POWER_30_MAX, 1000)
    thrustExp = exp.NACAPower30(arExp)
    plt.plot(arExp, thrustExp, '--', color='tab:red')
    arExp = np.linspace(0, exp.NACA_POWER_35_MAX, 1000)
    thrustExp = exp.NACAPower35(arExp)
    plt.plot(arExp, thrustExp, '--', color='tab:purple')
    arExp = np.linspace(0, exp.NACA_POWER_40_MAX, 1000)
    thrustExp = exp.NACAPower40(arExp)
    plt.plot(arExp, thrustExp, '--', color='tab:brown')
    arExp = np.linspace(0, exp.NACA_POWER_45_MAX, 1000)
    thrustExp = exp.NACAPower45(arExp)
    plt.plot(arExp, thrustExp, '--', color='tab:pink')
    
    plt.xlabel('Advance Ratio [-]')
    plt.ylabel('Power Coefficient [-]')
    plt.legend()
    plt.savefig(outPath + '/q2_power_coef.png', bbox_inches='tight')
    plt.close()

    # Plot efficiency graph
    print('[Q2] Plotting efficiency graph...')
    ax = plt.gca()
    ax.set_ylim([0, 100])
    ax.figure.set_figwidth(6.4*2)
    for i in range(len(ps)):
        plt.plot(vars[i], effs[i], label='$\\theta_{75}=%d$°' % (ps[i]))

    arExp = np.linspace(0, exp.NACA_EFF_15_MAX, 1000)
    effExp = exp.NACAEfficiency15(arExp)
    plt.plot(arExp, effExp*100.0, '--', color='tab:blue')
    arExp = np.linspace(0, exp.NACA_EFF_20_MAX, 1000)
    effExp = exp.NACAEfficiency20(arExp)
    plt.plot(arExp, effExp*100.0, '--', color='tab:orange')
    arExp = np.linspace(0, exp.NACA_EFF_25_MAX, 1000)
    effExp = exp.NACAEfficiency25(arExp)
    plt.plot(arExp, effExp*100.0, '--', color='tab:green')
    arExp = np.linspace(0, exp.NACA_EFF_30_MAX, 1000)
    effExp = exp.NACAEfficiency30(arExp)
    plt.plot(arExp, effExp*100.0, '--', color='tab:red')
    arExp = np.linspace(0, exp.NACA_EFF_35_MAX, 1000)
    effExp = exp.NACAEfficiency35(arExp)
    plt.plot(arExp, effExp*100.0, '--', color='tab:purple')
    arExp = np.linspace(0, exp.NACA_EFF_40_MAX, 1000)
    effExp = exp.NACAEfficiency40(arExp)
    plt.plot(arExp, effExp*100.0, '--', color='tab:brown')
    arExp = np.linspace(0, exp.NACA_EFF_45_MAX, 1000)
    effExp = exp.NACAEfficiency45(arExp)
    plt.plot(arExp, effExp*100.0, '--', color='tab:pink')

    plt.xlabel('Advance Ratio [-]')
    plt.ylabel('Efficiency [%]')
    plt.legend()
    plt.savefig(outPath + '/q2_efficiency.png', bbox_inches='tight')
    plt.close()