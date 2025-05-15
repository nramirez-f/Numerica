from advection import *
from ncviewer import NcView
from initial_conditions import *

x0 = -0.5
xf = 1
nx = 1500
T = 1
a = 1
cfl = 0.5

filepath = method_of_characteristics(x0, xf, nx, T, 200, a, riemann())

ncv = NcView(filepath)
ncv.frame(100, 0, 1, line_mode='lines')

ncv.close(remove=True)