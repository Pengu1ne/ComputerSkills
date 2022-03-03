'''
The program plots dE (y) and sample (x) from qm-energy.dat file

OBS! .dat has to have the samples in order before running this!
'''
##########################################################################
import matplotlib.pyplot as plt
fig = plt.gcf()
import matplotlib.cbook as cbook
from matplotlib import rc
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
import numpy as np
import pandas as pd
##########################################################################

##########################################################################
rc('font',**{'family':['Helvetica']})
# Presentations
#plt.rcParams['font.size'] = 20
# Articles - cannot be smaller than 6pt, -> 4x6 = 24pt
plt.rcParams['font.size'] = 36
rc('text',usetex=True)
#------------------------------------------------------------------------------
# Figure data
legnd = ['Ox2', 'Rd2']
#legnd = ['Stokes','VarO','VarR']
#--------------------------------------------
ttle = 'Azurin on Au(111) -- QM/MM -- Convergion'
xn,yn = 'Number of samples','Vertical energy gap [eV]'
# Transparency
a1 = 0.8
a2 = 1.0
# Linewidth
d1 = 3.0
d2 = 1.5

# Axises
ymin,ymax = 2.,5.
Mloc_y    = abs(ymax - ymin) / 5
mloc_y    = Mloc_y / 2
xmin,xmax = 3,500
Mloc_x    = abs(xmax - 0) / 5
mloc_x    = Mloc_x / 2


# Base name for figure
step = '50'
name = 'conv-dE-az-au-vac-2-'+step
##########################################################################

##########################################################################
# Import data from file
o_f_name = 'dE-e-avg-'+step+'-o2.dat'
r_f_name = 'dE-e-avg-'+step+'-r2.dat'
#--------------------------------------------
#f1_name = 'sys-e-l_st.dat'
#f2_name = 'sys-e-l_var-x.dat'
#f3_name = 'sys-e-l_var-r.dat'

x_oe = pd.read_csv(o_f_name, usecols=[1])
x_oe = (np.array(x_oe)) / 1.35
x_re = pd.read_csv(r_f_name, usecols=[1])
x_re = (np.array(x_re)) / 1.35
#--------------------------------------------
#x_f1 = pd.read_csv(f1_name, usecols=[1])
#x_f2 = pd.read_csv(f2_name, usecols=[1])
#x_f3 = pd.read_csv(f3_name, usecols=[1])
##########################################################################

##########################################################################
# Plot the data
#--------------------------------------------
# Axis manipulation
ax = plt.axes()

plt.xlim(xmin,xmax)
plt.ylim(ymin,ymax)
ax.xaxis.set_major_locator(MultipleLocator(Mloc_x))
ax.yaxis.set_major_locator(MultipleLocator(Mloc_y))
ax.xaxis.set_minor_locator(MultipleLocator(mloc_x))
ax.yaxis.set_minor_locator(MultipleLocator(mloc_y))
#--------------------------------------------
plt.plot(x_oe, c='red', alpha=a1, linewidth=d1)
plt.plot(x_re, c='blue', alpha=a1, linewidth=d1)
#--------------------------------------------
#plt.plot(x_f1, c='black', alpha=a1, linewidth=d1)
#plt.plot(x_f2, c='red', alpha=a1, linewidth=d1)
#plt.plot(x_f3, c='blue', alpha=a1, linewidth=d1)

##########################################################################

##########################################################################
# Plot the data
plt.xlabel(xn)
plt.ylabel(yn)
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
plt.legend(legnd,loc=7)
#---------------------------------------------------------
#plt.title(ttle)
##########################################################################

##########################################################################
# ACS : must fit in [3.25,1.75] in inches -> ratio : [1.86,1]
# Eg = [19.53,10.5]
# ACS : dpi=300 min for color, dpi=1200 min for black-white

# For presentations
#fig.set_size_inches(19.53,10.5)
#fig.savefig(name+'-pre.png', dpi=300)
# For articles - the recommended lenghts are 4x to maintain good quality
#
# The total size : 19.5 x 10.5 cm
fig.set_size_inches(19.5,10.5)
fig.savefig('figSI-'+name+'.pdf', dpi=1200, format='pdf',bbox_inches='tight')
#fig.savefig('fig-'+name+'.png', dpi=1200, bbox_inches='tight')

plt.show()
##########################################################################
