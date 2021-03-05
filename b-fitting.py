'''
A program to fit Hab values in contrast? to distances to get beta.

keyword(s): linear regresion

-wilhelmiian/pengu1ne
'''
import os
import sys
import pandas as pd
import numpy as np

###   Read the data
#
# Get the data from .dat file
def read_file(fname):
    data  = np.loadtxt(fname)
    dist  = data[:,:1]
    hab   = data[:,1:2]
    lnhab = data[:,2:3]
    #print('--------------------------------------------------')
    #print('--------------------------------------------------')
    return dist,hab,lnhab

### Linear regresion
#
# Fit the distance (x) and natural logarithm of Hab11 (y) to return beta
def b_fitting(x,y):
    len_x = len(x)
    sum_x = 0.
    sum_y = 0.
    sum_x_sq = 0.
    xi_yi = 0.
    
    for i in x:
        sum_x    += i
        sum_x_sq += i**2
    for j in y:
        sum_y += j
    for k in range(len_x):
        xi_yi += x[k]*y[k]
    
    term1 = xi_yi * len_x
    term2 = sum_x * sum_y
    
    term3 = sum_x*sum_x
    term4 = len_x*sum_x_sq
    divisor  = term4 - term3
    dividend = term1 - term2
    beta = dividend / divisor
    beta = -2 * beta
    return beta

### Saving the beta value
#
# Save the beta value together with Hab11 table
def print_to_file(table,dimer,funct,beta):
    df = pd.read_excel(table,index_col=[0,1])
    df.loc[(dimer,'beta'), funct] = beta
    df.to_excel(table,'hab11-pod2l')

### Main function
# 
def main():
    if len(sys.argv) != 2:
        print('Try: b_fitting output.dat')
        sys.exit(1)
    if os.path.isfile(sys.argv[1]):
        name = sys.argv[1]
        name = name.split('.')
        name = name[0]
        name = name.split('-',1)
        dim, func = name[0], name[1]
        d,ab,ln = read_file(sys.argv[1])
        b = b_fitting(d,ln)
        print_to_file('hab11-copy.xlsx',dim,func,b)

###############################################################################

if __name__=='__main__':
    main()

###############################################################################
