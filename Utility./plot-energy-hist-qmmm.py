##########################################################################
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridp
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
# Linewidth
d1 = 1.5
d2 = 1.5
# Scaling
fct = 30

# Axises
ymin, ymax = 1.6,5.5
y_lim      = [2.,3.,4.,5.]
#Mloc_y     = abs(ymax - ymin) / 5
#mloc_y     = Mloc_y / 2
xmin, xmax = 0,500
x_lim      = [0,100,200,300,400,500]
#Mloc_x1    = abs(xmax1 - xmin1) / 5
#mloc_x     = Mloc_x / 2

# Readable file(s)
fn_o = 'dEe-o2.dat'
fn_r = 'dEe-r2.dat'

conv_o = 'dE-e-avg-50-o2.dat'
conv_r = 'dE-e-avg-50-r2.dat'
# base name for saving
name  = 'de-hist-conv-az-au-vac-qmmm2-e'
##########################################################################
#
#                      READ DATA
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

cnv_o = np.loadtxt(conv_o,delimiter=',',usecols=[1])
cnv_o = (np.array(cnv_o))/1.35
cnv_r = np.loadtxt(conv_r,delimiter=',',usecols=[1])
cnv_r = (np.array(cnv_r))/1.35
cnv_y = np.loadtxt(conv_r,delimiter=',',usecols=[0])
cnv_y = np.array(cnv_y)
##########################################################################
#
#                      PLOTTING -- I
#
##########################################################################
# Adding subplots
#-------------------------------------------------------------------------
figr = plt.figure(1)
spec = gridp.GridSpec(ncols=2,nrows=1,wspace=0,
                      width_ratios=widths)
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
plt.plot(y,x_rd,c='b', alpha=a1, linewidth=d1, label='Rd')
plt.plot(y,x_ox,c='r', alpha=a1, linewidth=d1, label='Ox')
plt.plot(cnv_y,cnv_r,c='b', alpha=a2, linewidth=d1)
plt.plot(cnv_y,cnv_o,c='r', alpha=a2, linewidth=d1)
plt.axhline(y=rd_avg, c='b', alpha=a2, linewidth=d2, linestyle='dotted')
plt.axhline(y=ox_avg, c='r', alpha=a2, linewidth=d2, linestyle='dotted')
##########################################################################
#
#                      HISTOGRAM
#
##########################################################################
# Axises
#-------------------------------------------------------------------------
hist_e = figr.add_subplot(spec[0,1])
hist_e.get_xaxis().set_ticks([])
hist_e.get_yaxis().set_ticks([])
hist_e.set_ylim(ymin,ymax)
#-------------------------------------------------------------------------
# Plotting
#-------------------------------------------------------------------------
mu1, sigma1 = norm.fit(rd_avg)
mu2, sigma2 = norm.fit(ox_avg)
#-------------------------------------------------------------------------
rd_yh = np.linspace(rd_avg - 5*rd_var05, rd_avg + 5*rd_var05,5000)
rd_xh = (norm.pdf(rd_yh, rd_avg, rd_var05)) *fct
ox_yh = np.linspace(ox_avg - 5*ox_var05, ox_avg + 5*ox_var05,5000)
ox_xh = (norm.pdf(ox_yh, ox_avg, ox_var05)) *fct
#-------------------------------------------------------------------------
plt.plot(rd_xh,rd_yh,c='b',alpha=a2,linewidth=d2, label='Rd2')
plt.plot(ox_xh,ox_yh,c='r',alpha=a2,linewidth=d2, label='Ox2')

n1, bins1, patches1 = plt.hist(x_rd,30,orientation='horizontal',
                               facecolor='blue', alpha=a1)
n2, bins2, patches2 = plt.hist(x_ox,30,orientation='horizontal',
                               facecolor='red', alpha=a1)
plt.axhline(y=rd_avg, c='b', alpha=a2, linewidth=d2, linestyle='dotted')
plt.axhline(y=ox_avg, c='r', alpha=a2, linewidth=d2, linestyle='dotted')

plt.legend(loc=1)
##########################################################################
#
#                      PLOTTING -- I
#
##########################################################################
# Show and safe plot
#-------------------------------------------------------------------------
figr.set_size_inches(w,h)

figr.savefig('fig-'+name+'.pdf', dpi=rs, format='pdf',bbox_inches='tight')
plt.show()
##########################################################################
