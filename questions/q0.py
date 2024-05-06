import bemt
import matplotlib.pyplot as plt
from statement.propeller import *
from utils.units import *
from utils.collective_pitch import *
from utils.plot_dat import *

def Q0(outPath: str, blade: bemt.Blade, air: bemt.Fluid):
    # Plot blade geometry
    print('[Q0] Plotting blade geometry...')
    rs = np.linspace(blade.minRadius, blade.maxRadius, 1000)
    chords = blade.chord(rs)
    twists = blade.twist(rs)
    fig, ax1 = plt.subplots()
    ax1.plot(rs/BLADE_R, chords, color='tab:blue', label='Chord')
    ax1.set_ylabel('Chord [m]')
    ax2 = ax1.twinx()
    ax2.plot(rs/BLADE_R, np.rad2deg(twists), color='tab:orange', label='Pitch')
    ax2.set_ylabel('Pitch [°]')
    ax1.set_xlabel('r/R [-]')
    plt.legend()
    plt.savefig(outPath + '/blade_geom.png')
    plt.close()