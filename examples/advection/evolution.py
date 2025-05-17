from advection import *
from ncviewer import NcView
from initial_conditions import *

x0 = -1
xf = 101
nx = 10200
T = 1001
a = 1
cfl = 0.8

filepath = cir(x0, xf, nx, T, cfl, a, bumping(1, 8), sns=1250)

ncv = NcView(filepath)
ncv.evolution(0)

ncv.close(remove=True)