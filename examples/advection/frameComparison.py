from advection import *
from ncviewer import NcView
from initial_conditions import *
import os

x0 = -1
xf = 1
nx = 600
T = 1
a = 1
cfl = 0.8

ic = bumping(1, 8)

exact_ncf = method_of_characteristics(-0.5, 1, 1500, T, 200, a, ic)

cir_ncf = cir(x0, xf, nx, T, cfl, a, ic)

lf_ncf = lax_friedrichs(x0, xf, nx, T, cfl, a, ic)

lw_ncf = lax_wendroff(x0, xf, nx, T, cfl, a, ic)

bw_ncf = beam_warming(x0, xf, nx, T, cfl, a, ic)

iterPos = 400

framesList = [{"ncfile_path": cir_ncf,
               "iterPos": iterPos,
               "varName": "u",
               "dimName": "x",
               "iterName": "t",
               "varNameInPlot" : "CIR",
               "line_mode": "markers", 
               "line_color": "blue"},

               {"ncfile_path": lf_ncf,
               "iterPos": iterPos,
               "varName": "u",
               "dimName": "x",
               "iterName": "t",
               "varNameInPlot" : "Lax-Friedichs",
               "line_mode": "markers", 
               "line_color": "yellow"},

               {"ncfile_path": lw_ncf,
               "iterPos": iterPos,
               "varName": "u",
               "dimName": "x",
               "iterName": "t",
               "varNameInPlot" : "Lax-Wendroff",
               "line_mode": "markers", 
               "line_color": "brown"},

               {"ncfile_path": bw_ncf,
               "iterPos": iterPos,
               "varName": "u",
               "dimName": "x",
               "iterName": "t",
               "varNameInPlot" : "Beam-Warmming",
               "line_mode": "markers", 
               "line_color": "purple"}
               ]

ncv = NcView(exact_ncf)
ncv.frameComparison(100, 0, 1, framesList, line_color='black', line_mode='lines')

for frame in framesList:
    os.remove(frame["ncfile_path"])

ncv.close(remove=True)
