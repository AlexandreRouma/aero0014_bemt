import numpy as np
from subprocess import Popen, PIPE

def xfoil(airfoil: str, reynolds: float, a: float, polar: str):
    p = Popen(['xfoil'], stdin=PIPE)
    script = 'plop\n'
    script += 'G F\n'
    script += '\n'
    script += 'load %s\n'%(airfoil)
    script += 'oper\n'
    script += 'iter 500\n'
    script += 'visc %e\n'%(reynolds)
    script += 'pacc\n'
    script += '%s\n'%(polar)
    script += '\n'
    script += 'a %lf\n'%(a)
    script += 'pacc\n'
    script += '\n'
    script += 'quit\n'
    p.stdin.write(script.encode('ascii'))
    p.stdin.flush()
    p.stdin.close()
    p.wait()

reynolds = [ 1e5, 2e5, 5e5, 1e6, 2e6, 5e6, 1e7 ]
alphas = np.linspace(-20, 20, 40*4+1)

for r in reynolds:
    for a in alphas:
        xfoil('airfoil_geometries/clark_y.dat', r, a, 'airfoil_polars/Polar_%e_clark_y.txt'%(r))
