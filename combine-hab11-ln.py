import pandas as pd
import numpy as np

def line_f():
    print('-----------------------------------------------------------------')
    print('-----------------------------------------------------------------')

n = 1

# Read the Hab11 values and the natural log values
hab = pd.read_excel('hab11.xlsx', index_col=[0,1])
ln  = pd.read_excel('hab11-ln.xlsx', index_col=[0,1])

# Name of the columns from Hab11 / POD2L
# Functionals
functs = hab.columns
l_col = len(functs)

# DF -> np.array
hab = np.asarray(hab)
ln = np.asarray(ln)
hab = hab[~np.isnan(hab)]
ln = ln[~np.isnan(ln)]
hab = np.reshape(hab,(44,10))
ln = np.reshape(ln,(44,10))

# Collect name of the dimers
dimer = ['ete','ace','cpr','cbd','cpd','fur','pyr','thp','imi','ben','phe']
l_dim = len(dimer)

# The new indeces
# Distances
distances = [3.5,4.0,4.5,5.0]
dist = np.array(distances)
dist = np.reshape(dist,(4,1))
#print(distances)
# The new columns
cols = ['Hab11[meV]','ln']

# Collect the values into .dat
x = 4*n
y = 0

while x < 47:
    x += 4
    while y < 12:
        y += 1
        print(dimer[n])
        print(functs[y-1])
        name = dimer[n]+'-'+functs[y-1]+'.dat'
        print(name)
        m1 = hab[x-4:x,y-1:y]
        m2 = ln[x-4:x,y-1:y]
        #print(m1)
        #print(m2)
        M = np.concatenate((dist,m1), axis=1)
        M = np.concatenate((M,m2), axis=1)
        print(M)
        np.savetxt(name,M,delimiter='   ',fmt='%5.10f')
