##########################################################################
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridp
import matplotlib.patches as patches
fig = plt.gcf()
import matplotlib.cbook as cbook
from matplotlib import rc
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
import numpy as np
import pandas as pd
from scipy.stats import norm
##########################################################################
#
#                      GENERAL
#
##########################################################################
# Style
#-------------------------------------------------------------------------
rc('font',**{'family':['Helvetica']})
#Articles usually want no smaller than 6pt -> fig will be shrinked
plt.rcParams['font.size'] = 36
rc('text',usetex=True)

# figure size (w = width (inch), l = lenght (inch)) and resolution
widths  = [3,1]
w       = 19.5
#hights  = [1,1]
h       = 10.5
rs = 1200
#-------------------------------------------------------------------------
# Legend, etc.
#-------------------------------------------------------------------------
ttle  = 'name of the title'
legnd = ['Rd','Ox']
xn,yn = 'Sample number','Vertical energy gap [eV]'

# Transparency
a1 = 0.5
a2 = 1.0
a3 = 0.3
# Linewidth
d1 = 1.5
d2 = 1.5
d3 = 10.0
# Scaling
fct = 30

# Axises
ymin, ymax = 2.,5.5
y_lim      = [2.,3.,4.,5.]
#Mloc_y     = abs(ymax - ymin) / 5
#mloc_y     = Mloc_y / 2
xmin, xmax = 0,500
x_lim      = [0,100,200,300,400,500]
#Mloc_x1    = abs(xmax1 - xmin1) / 5
#mloc_x     = Mloc_x / 2

# Readable file(s)
fn_o = 'dEe-o1.dat'
fn_r = 'dEe-r1.dat'

box_oa = 'ox1-a.dat'
box_ob = 'ox1-b.dat'
box_ra = 'rd1-a.dat'
box_rb = 'rd1-b.dat'
# base name for saving
name  = 'de-hist-az-au-vac-qmmm1-e'
##########################################################################
#
#                      READ DATA - all
#
##########################################################################
x_rd = np.loadtxt(fn_r,delimiter=',',usecols=[1])
x_rd = (np.array(x_rd))/1.35
x_ox = np.loadtxt(fn_o,delimiter=',',usecols=[1])
x_ox = (np.array(x_ox))/1.35
y    = np.loadtxt(fn_r,delimiter=',',usecols=[0])
y    = np.array(y)

rd_avg, rd_var     = np.average(x_rd), np.var(x_rd)
ox_avg, ox_var     = np.average(x_ox), np.var(x_ox)
rd_var05, ox_var05 = np.sqrt(rd_var),np.sqrt(ox_var)
##########################################################################
#
#                      READ DATA - drawing for boxes
#
##########################################################################
x_rab  = np.loadtxt(box_ra,delimiter=',',usecols=[1])
x_rab  = (np.array(x_rab))/1.35
y_rab  = np.loadtxt(box_ra,delimiter=',',usecols=[0])
y_rab  = np.array(y_rab)
ly_rab = len(y_rab)

x_rbb  = np.loadtxt(box_rb,delimiter=',',usecols=[1])
x_rbb  = (np.array(x_rbb))/1.35
y_rbb  = np.loadtxt(box_rb,delimiter=',',usecols=[0])
y_rbb  = np.array(y_rbb)
ly_rbb = len(y_rbb)

x_oab  = np.loadtxt(box_oa,delimiter=',',usecols=[1])
x_oab  = (np.array(x_oab))/1.35
y_oab  = np.loadtxt(box_oa,delimiter=',',usecols=[0])
y_oab  = np.array(y_oab)
ly_oab = len(y_oab)

x_obb  = np.loadtxt(box_ob,delimiter=',',usecols=[1])
x_obb  = (np.array(x_obb))/1.35
y_obb  = np.loadtxt(box_ob,delimiter=',',usecols=[0])
y_obb  = np.array(y_obb)
ly_obb = len(y_obb)

a_rd, b_rd   = np.average(x_rab), np.average(x_rbb)
xa_rd, xb_rd = [a_rd]*ly_rab, [b_rd]*ly_rbb
a_ox, b_ox   = np.average(x_oab), np.average(x_obb)
xa_ox, xb_ox = [a_ox]*ly_oab, [b_ox]*ly_obb
##########################################################################
#
#                      PLOTTING -- I
#
##########################################################################
# Adding subplots
#-------------------------------------------------------------------------
figr = plt.figure(1)
spec = gridp.GridSpec(ncols=1,nrows=1)
##########################################################################
#
#                      VERT. E.GAP
#
##########################################################################
# Axises
#-------------------------------------------------------------------------
vert_e = figr.add_subplot(spec[0,0])
vert_e.get_xaxis().set_ticks(x_lim)
vert_e.set_xlim(xmin,xmax)
#vert_e.get_yaxis().set_ticks([])
vert_e.get_yaxis().set_ticks(y_lim)
vert_e.set_ylim(ymin,ymax)
#-------------------------------------------------------------------------
# Legend and titles
#-------------------------------------------------------------------------
# loc = location
# 0 = best
# 1 = upper right
# 2 = upper left 
# 3 = lower left 
# 4 = lower right
# 5 = right
# 6 = center left
# 7 = center right
# 8 = lower center
# 9 = upper center
# 10 = center
#plt.legend(legnd,loc=1)

plt.xlabel(xn)
plt.ylabel(yn)
#-------------------------------------------------------------------------
# Plotting
#-------------------------------------------------------------------------
# Main plot
plt.plot(y,x_rd,c='b', alpha=a1, linewidth=d1)
plt.plot(y,x_ox,c='r', alpha=a1, linewidth=d1)
plt.axhline(y=rd_avg, c='b', alpha=a2, linewidth=d2, linestyle='dotted')
plt.axhline(y=ox_avg, c='r', alpha=a2, linewidth=d2, linestyle='dotted')

# Boxes for A and B structures
plt.scatter(y_rab,xa_rd,c='lime', alpha=a3, linewidth=d3, label="Rd-A")
plt.scatter(y_rbb,xb_rd,c='cyan', alpha=a3, linewidth=d3, label="Rd-B")
plt.scatter(y_oab,xa_ox,c='magenta', alpha=a3, linewidth=d3, label="Ox-A")
plt.scatter(y_obb,xb_ox,c='orange', alpha=a3, linewidth=d3, label="Ox-B")

plt.legend(loc=2, ncol=4)
##########################################################################
#
#                      PLOTTING -- I
#
##########################################################################
# Show and safe plot
#-------------------------------------------------------------------------
figr.set_size_inches(w,h)

#figr.savefig('fig-'+name+'.pdf', dpi=rs, format='pdf',bbox_inches='tight')
figr.savefig('fig-TESTING-sys1.pdf', dpi=rs, format='pdf',bbox_inches='tight')
plt.show()
##########################################################################
