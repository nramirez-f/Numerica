from advection import *
from ncviewer import NcView
from initial_conditions import *

x0 = -1
xf = 3
nx = 1100
T = 10
a = 1
cfl = 0.8

filepath = lax_friedrichs(x0, xf, nx, T, cfl, a, bumping(1, 8), sns=1)

ncv = NcView(filepath)
ncv.evolution(0)

ncv.close(remove=True)