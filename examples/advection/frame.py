from advection import *
from ncviewer import NcView
from initial_conditions import *

x0 = -0.5
xf = 1
nx = 600
T = 1
a = 1
cfl = 0.5

filepath = cir(x0, xf, nx, T, cfl, a, riemann(), sns=1)

ncv = NcView(filepath)
ncv.frame(400, 0, 1, line_color='blue')

ncv.close(remove=True)