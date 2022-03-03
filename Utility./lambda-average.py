'''
This program creates a data set of average values of lamdba
'''

###############################################################################
import numpy as np
import pandas as pd
kBT = 0.026
###############################################################################
# Read the data file
# Parameters
f1 = 'dE-e-avg-o2.dat'
f2 = 'dE-e-avg-r2.dat'
f3 = 'dEe-o2.dat'
f4 = 'dEe-r2.dat'

###############################################################################
def write_data(set_st, set_v_x, set_v_r):
    set_st = pd.DataFrame(set_st)
    set_st.to_csv('2-e-l_st'+'.dat')
    
    set_v_x = pd.DataFrame(set_v_x)
    set_v_x.to_csv('2-e-l_var-x'+'.dat')

    set_v_r = pd.DataFrame(set_v_r)
    set_v_r.to_csv('2-e-l_var-r'+'.dat')
###############################################################################
def lambda_avg(set_xs, set_rs, set_xv, set_rv):
    l_st     = []
    l_var_ox = []
    l_var_rd = []
    
    ls = len(set_rs)
    lv = len(set_xv)

    # Stokes
    for i in range(ls):
        a = 0.5 * (set_rs[i] - set_xs[i])
        l_st.append(a)

    # Variational
    for i in range(lv):
        a = np.var(set_xv[1:i])
        a = 0.5 * (a / kBT)

        b = np.var(set_rv[1:i])
        b = 0.5 * (b / kBT)
        
        l_var_ox.append(a)
        l_var_rd.append(b)

    return l_st, l_var_ox, l_var_rd
###############################################################################
# Run program
ox_s = np.loadtxt(f1,delimiter=',', usecols=[1])
rd_s = np.loadtxt(f2,delimiter=',', usecols=[1])
ox_v = np.loadtxt(f3,delimiter=',', usecols=[1])
rd_v = np.loadtxt(f4,delimiter=',', usecols=[1])

stok, var_x, var_r = lambda_avg(ox_s,rd_s, ox_v, rd_v)
write_data(stok,var_x,var_r)
