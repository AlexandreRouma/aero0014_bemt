import bemt
import matplotlib.pyplot as plt
from statement.propeller import *
from utils.units import *
from utils.collective_pitch import *

def plotVelTriangle(elemId, config: bemt.Configuration, blade: bemt.Blade, res: bemt.Solution, forceScale: float = 1, velocityScale: float = 0.015, aoaXOffset = 0, aoaYOffset = 0, dDOffset = 0, w2Offset = 0):
    # Draw airfoil
    twist = config.X[elemId]
    blade.airfoil.plot(0, 0, 1, twist)

    # Compute useful locations
    vtTop = np.array([config.Omegar[elemId]*velocityScale - res.vu2[elemId]*velocityScale, res.va2[elemId]*velocityScale]) 

    # Draw dotted chord line
    dx = -np.cos(twist)
    dy = -np.sin(twist)
    plt.plot([-0.5*dx, 1.5*dx], [-0.5*dy, 1.5*dy], '--', color='black')

    # Draw dotted relative velocity line
    B2 = np.arctan2(res.va2[elemId]*velocityScale, -res.wu2[elemId]*velocityScale)
    dx = -np.cos(B2)
    dy = -np.sin(B2)
    plt.plot([0, 1.5*dx], [0, 1.5*dy], '--', color='blue')

    dEnd = np.array([dx*res.dD[elemId]*forceScale, dy*res.dD[elemId]*forceScale])
    lEnd = np.array([dy*res.dL[elemId]*forceScale, -dx*res.dL[elemId]*forceScale])

    # Draw dotted angle mark
    als = np.linspace(twist, B2, 100)
    xs = []
    ys = []
    for a in als:
        xs.append(-np.cos(a)*1.25)
        ys.append(-np.sin(a)*1.25)
    plt.plot(xs, ys, '--', color='blue')

    # Draw velocity arrows
    plt.arrow(0, 0, config.Omegar[elemId]*velocityScale, 0, head_width=0.05, length_includes_head=True, fc='red', ec='red')
    plt.arrow(vtTop[0], vtTop[1], res.vu2[elemId]*velocityScale, -res.va2[elemId]*velocityScale, head_width=0.05, length_includes_head=True, fc='green', ec='green')
    plt.arrow(vtTop[0], vtTop[1], res.wu2[elemId]*velocityScale, -res.va2[elemId]*velocityScale, head_width=0.05, length_includes_head=True, fc='blue', ec='blue')

    # Draw force arrows
    plt.arrow(0, 0, dEnd[0], dEnd[1], head_width=0.05, length_includes_head=True, fc='magenta', ec='magenta')
    plt.arrow(0, 0, lEnd[0], lEnd[1], head_width=0.05, length_includes_head=True, fc='magenta', ec='magenta')

    # Draw text
    plt.text(vtTop[0]-0.35, vtTop[1] + w2Offset, '$\\vec{\\mathcal{w}}_2$', color='blue', fontsize=20)
    plt.text(vtTop[0]+0.1, vtTop[1]-0.2, '$\\vec{\\mathcal{v}}_2$', color='green', fontsize=20)
    plt.text(vtTop[0]+0.1, -0.2, '$\\mathcal{u}$', color='red', fontsize=20)
    plt.text(dEnd[0]+0.05, dEnd[1]-0.15 + dDOffset, '$\\mathcal{dD}$', color='magenta', fontsize=20)
    plt.text(lEnd[0]-0.35, lEnd[1], '$\\mathcal{dL}$', color='magenta', fontsize=20)
    plt.text(1.5*dx+0.2+aoaXOffset, 1.5*dy + aoaYOffset, 'aoa = %.3f°' % (np.rad2deg(twist - B2)), color='blue', fontsize=20)
    

def Q1(outPath: str, blade: bemt.Blade, air: bemt.Fluid):
    # Simulate for 25° collective pitch and 90mph free-stream velocity
    print('[Q1] Computing for 25° and 90mph...')
    configA = bemt.Configuration(blade, 3, collectivePitch(blade, 0.75*BLADE_R, 25), 800, MPHtoMS(90), air)
    resA = bemt.solve(configA)

    # Simulate for 25° collective pitch and 90mph free-stream velocity
    print('[Q1] Computing for 35° and 135mph...')
    configB = bemt.Configuration(blade, 3, collectivePitch(blade, 0.75*BLADE_R, 35), 800, MPHtoMS(135), air)
    resB = bemt.solve(configB)

    # Plot thrust graph
    print('[Q1] Plotting thrust graph...')
    plt.plot(configA.r/BLADE_R, resA.dT/configA.dr, label='$\\theta_{75}$ = 25°, v = 90mph')
    plt.plot(configB.r/BLADE_R, resB.dT/configB.dr, label='$\\theta_{75}$ = 35°, v = 135mph')
    plt.legend()
    plt.xlabel('r/R [-]')
    plt.ylabel('dT/dr [N/m]')
    plt.savefig(outPath + '/q1_thrust.png', bbox_inches='tight')
    plt.close()

    # Plot power graph
    print('[Q1] Plotting power graph...')
    plt.plot(configA.r/BLADE_R, resA.dP, label='$\\theta_{75}$ = 25°, v = 90mph')
    plt.plot(configB.r/BLADE_R, resB.dP, label='$\\theta_{75}$ = 35°, v = 135mph')
    plt.legend()
    plt.xlabel('r/R [-]')
    plt.ylabel('dP/dr [W/m]')
    plt.savefig(outPath + '/q1_power.png', bbox_inches='tight')
    plt.close()

    # Plot velocity triangle in low radii
    plt.axis('off')
    plt.gca().set_aspect('equal')
    plotVelTriangle(0, configA, blade, resA)
    plt.savefig(outPath + '/q1_vel_tri_low.png', bbox_inches='tight')
    plt.close()

    # Plot velocity triangle in medium radii
    plt.axis('off')
    plt.gca().set_aspect('equal')
    plotVelTriangle(25, configA, blade, resA, 0.2)
    plt.savefig(outPath + '/q1_vel_tri_med.png', bbox_inches='tight')
    plt.close()

    # Plot velocity triangle in high radii
    plt.axis('off')
    plt.gca().set_aspect('equal')
    plotVelTriangle(47, configA, blade, resA, 0.2, aoaXOffset=0.5, aoaYOffset=-0.2, dDOffset=-0.1, w2Offset=0.1)
    plt.savefig(outPath + '/q1_vel_tri_high.png', bbox_inches='tight')
    plt.close()

    # Print results
    print('[Q1] Theta_75 = 25°, v = 90mph:  Thrust      = %s N' % (resA.T))
    print('[Q1] Theta_75 = 25°, v = 90mph:  Shaft Power = %s W' % (resA.P))
    print('[Q1] Theta_75 = 25°, v = 90mph:  Efficiency  = %s %%' % (resA.eta * 100.0))
    print('[Q1] Theta_75 = 35°, v = 135mph: Thrust      = %s N' % (resB.T))
    print('[Q1] Theta_75 = 35°, v = 135mph: Shaft Power = %s W' % (resB.P))
    print('[Q1] Theta_75 = 35°, v = 135mph: Efficiency  = %s %%' % (resB.eta * 100.0))