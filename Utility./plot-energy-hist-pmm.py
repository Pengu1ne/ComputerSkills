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
kBT = 0.026
scl = 1.35
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

# stp = jump/step : 1 = all, 2 = joka toinen, etc
# crd = number of coordinated amino acids
# sts = number of transition states
stp = 1
crd = '6'
sts = '70'
# Transparency
a1 = 0.5
a2 = 1.0
# Linewidth
d1 = 1.5
d2 = 1.5
# Scaling
fct = 4000/stp

# Axises
ymin, ymax = -5.,9.
y_lim      = [-4.,-2.,0,2.,4.,6.,8.]
xmin, xmax = 0,100000/stp
x_lim      = [0,20000/stp,40000/stp,60000/stp,80000/stp,100000/stp]
#xmin, xmax = 0,100000
#x_lim      = [0,20000,40000,60000,80000,100000]

# Readable file(s)
fname = 'az-vac-pmm-pro-'+crd+'-'+sts+'.gap'
# base name for saving
name  = 'de-hist-az-vac-pmm-'+crd+'coord-'+sts+'st-'+str(stp)
##########################################################################
#
#                      READ DATA
#
##########################################################################
x_rd = np.loadtxt(fname,usecols=[1])
x_rd = np.array(x_rd)
x_rd = x_rd[::stp]
x_ox = np.loadtxt(fname,usecols=[2])
x_ox = np.array(x_ox)
x_ox = x_ox[::stp]
#y    = np.loadtxt(fname,usecols=[0])
#y    = np.array(y)
#y    = y[::fct]

#print(np.shape(y),np.shape(x_rd),np.shape(x_ox))
#print(np.shape(x_rd),np.shape(x_ox))

rd_avg, rd_var     = np.average(x_rd), np.var(x_rd)
ox_avg, ox_var     = np.average(x_ox), np.var(x_ox)
rd_var05, ox_var05 = np.sqrt(rd_var),np.sqrt(ox_var)
##########################################################################
#
#                      SAVE MANIPULATED DATA INTO FILES
#
##########################################################################
datas  = [x_rd,x_ox]
dat    = list(zip(*datas))

df_data = pd.DataFrame(data=dat)
df_data.to_csv(name+'.dat', sep='\t',
               float_format='%.5f', header=False)

lbd_var_rd = rd_var / (2.*kBT)
lbd_var_ox = ox_var / (2.*kBT)
lbd_stk    = 0.5*(rd_avg - ox_avg)

with open(name+'.lmbd','w') as outp:
    outp.write('--------------------------------------------------------\n')
    outp.write('Number of samples: %i\n'% (np.shape(x_rd)))
    outp.write('\t\t\tReduced\t\tOxidiced\n')
    outp.write('Vert. ion. E,avg [eV]:\t %.5f\t%.5f\n'% (rd_avg,ox_avg))
    outp.write('Vert. ion. E,var [eV]:\t %.5f\t%.5f\n\n'% (rd_var05,ox_var05))
    outp.write('Reorg. free E,[eV]   :\t %.5f\t%.5f\n'% (lbd_var_rd/scl,lbd_var_ox/scl))
    outp.write('\t\t\t\t%.5f\n'% (lbd_stk/scl))
    outp.write('--------------------------------------------------------')
#########################################################################
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
#plt.plot(y,x_rd,c='b', alpha=a1, linewidth=d1, label='Rd')
#plt.plot(y,x_ox,c='r', alpha=a1, linewidth=d1, label='Ox')
plt.plot(x_rd,c='b', alpha=a1, linewidth=d1, label='Rd')
plt.plot(x_ox,c='r', alpha=a1, linewidth=d1, label='Ox')
plt.axhline(y=rd_avg, c='b', alpha=a2, linewidth=d2, linestyle='dotted')
plt.axhline(y=ox_avg, c='r', alpha=a2, linewidth=d2, linestyle='dotted')

plt.legend(loc=1)
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
plt.plot(rd_xh,rd_yh,c='b',alpha=a2,linewidth=d2)
plt.plot(ox_xh,ox_yh,c='r',alpha=a2,linewidth=d2)

n1, bins1, patches1 = plt.hist(x_rd,50,orientation='horizontal',
                               facecolor='blue', alpha=a1)
n2, bins2, patches2 = plt.hist(x_ox,50,orientation='horizontal',
                               facecolor='red', alpha=a1)
plt.axhline(y=rd_avg, c='b', alpha=a2, linewidth=d2, linestyle='dotted')
plt.axhline(y=ox_avg, c='r', alpha=a2, linewidth=d2, linestyle='dotted')
##########################################################################
#
#                      PLOTTING -- I
#
##########################################################################
# Show and safe plot
#-------------------------------------------------------------------------
figr.set_size_inches(w,h)

figr.savefig('fig-'+name+'.pdf', dpi=rs, format='pdf',bbox_inches='tight')
#figr.savefig('fig-testing-'+str(fct)+'.pdf', dpi=rs, format='pdf',bbox_inches='tight')
plt.show()
##########################################################################
