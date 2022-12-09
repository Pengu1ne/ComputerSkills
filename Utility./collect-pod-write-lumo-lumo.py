"""
This program will find the POD values from CP2K .out file

-Vilhelmiina/Pengu1ne
"""
###############################################################################
import time
import sys
import pandas as pd
import numpy as np
###############################################################################
###############################################################################
start = time.time()
###############################################################################
###############################################################################
# Patterns
lookup = 'Coupling elements [meV]:'
filename = sys.argv[1]
file_out = filename.split('.')[0]

# Define collectables
# elec = nro of electrons in block
# ao = nro of atomic orbital functions in block
# homo, lumo = HOMO and LUMO states
# pod = Coupling energy in meV
elec,ao   = [],[]
homo,lumo = [],[]
pod       = []

# Dummy values
# b1 = First blocks
# b2 = Second block
# st_l = starting value for the lines
# r_line = lines to be read
b1,b2,st_l = [],[],0
r_line     = []

# Find the line number

with open(filename, 'r') as fn:
    for num, line in  enumerate(fn,1):
        if lookup in line:
            st_l = num

# Collect the values
with open(filename, 'r') as fn:
    for line in fn:
        if 'Number of block electrons' in line:
            elec.append(int(line.split()[-1]))
        if 'Number of block AO functions' in line:
            ao.append(int(line.split()[-1]))

print('-------------------------------------------------------------------------------')
with open(file_out+'-elec.dat','w') as eout:
    eout.write('-------------------------------------------------------------------------------\n')
    eout.write('Number of electrons per block\n')
    eout.write('Block\telectrons\n')
    eout.write('-------------------------------------------------------------------------------\n')
    for i in range(len(elec)):
        eout.write('%i\t%i\n'% (i+1,elec[i]))

with open(file_out+'-ao.dat','w') as eout:
    eout.write('-------------------------------------------------------------------------------\n')
    eout.write('Number of AOs per block\n')
    eout.write('Block\tAOs\n')
    eout.write('-------------------------------------------------------------------------------\n')
    for i in range(len(ao)):
        eout.write('%i\t%i\n'% (i+1,ao[i]))

end    = time.time()
calc_s = end - start
calc_m = calc_s / 60.
calc_h = calc_m / 60.
print('-------------------------------------------------------------------------------')
print('Collected nro of electrons and AO')
print('Number of blocks by electrons: %i'% (len(elec)))
print('Number of blocks by AO       : %i'% (len(ao)))
print('-------------------------------------------------------------------------------')
print('Time used [s]   : %.2f'% (calc_s))

print('Time used [min] : %.2f'% (calc_m))
print('Time used [h]   : %.2f'% (calc_h))
print('-------------------------------------------------------------------------------')

matr_d = int(len(elec)) - 1
print('-------------------------------------------------------------------------------')
print('1D of matrix : %i'% (matr_d))
print('-------------------------------------------------------------------------------')

# Define HOMO and LUMO for homo-lumo coupling
#for i in elec:
#    if (i%2) == 0:
#        homo.append(i//2)
#        lumo.append((i//2)+1)
#    elif (i%2) ==1:
#        homo.append((i//2)+1)
#        lumo.append((i//2)+1)

# Define LUMO and LUMO for lumo-lumo coupling
'''
The homo is defined as the orbital that can donate the electron (after receiving one from
previous residue). The lumo is defined as a first place where residue can take the electron.
In single-occupied MO (SOMO) case:
- because HOMO can receive one electron, which is passed in the next step, HOMO = SOMO
- the same MO can also receive an electron, thus, LUMO = SOMO
In double-occupied (DOMO) MO case:
- because HOMO cannot receive one electron, the donor orbital is (empty) LUMO, which is passed in the next step, HOMO = DOMO +1
- the same DOMO cannot either receive an electron, thus, LUMO = DOMO +1
'''
for i in elec:
    if (i%2) == 0:
        homo.append((i//2)+1)
        lumo.append((i//2)+1)
    elif (i%2) == 1:
        homo.append(i//2)
        lumo.append(i//2)

with open(file_out+'-homo-donor.dat','w') as eout:
    eout.write('-------------------------------------------------------------------------------\n')
    eout.write('Number of HOMO of block\n')

    eout.write('Block\tHOMO\n')
    eout.write('-------------------------------------------------------------------------------\n')
    for i in range(len(homo)):
        eout.write('%i\t%i\n'% (i+1,homo[i]))

with open(file_out+'-lumo-acceptor.dat','w') as eout:
    eout.write('-------------------------------------------------------------------------------\n')
    eout.write('Number of LUMO of block\n')
    eout.write('Block\tLUMO\n')
    eout.write('-------------------------------------------------------------------------------\n')
    for i in range(len(lumo)):
        eout.write('%i\t%i\n'% (i+1,lumo[i]))

end    = time.time()
calc_s = end - start
calc_m = calc_s / 60.
calc_h = calc_m / 60.
print('-------------------------------------------------------------------------------')
print('Defined HOMO and LUMO states')
print('Number of blocks by HOMOs : %i'% (len(homo)))
print('Number of blocks by LUMOs : %i'% (len(lumo)))
print('-------------------------------------------------------------------------------')
print('Time used [s]   : %.2f'% (calc_s))
print('Time used [min] : %.2f'% (calc_m))

print('Time used [h]   : %.2f'% (calc_h))
print('-------------------------------------------------------------------------------')

# Define block combinations
for i in range(len(homo)-1):
    for j in range(i+1,len(homo)):
        b1.append(i)
        b2.append(j)

print('-------------------------------------------------------------------------------')
print('Sanity check: how many blocks')
print('Number of blocks / rows : %i'% (len(b1)))
print('Number of blocks / columns : %i'% (len(b2)))
print('-------------------------------------------------------------------------------')

end    = time.time()
calc_s = end - start
calc_m = calc_s / 60.
calc_h = calc_m / 60.
print('-------------------------------------------------------------------------------')
print('Defined Possible block combinations')
print('Number of rows    : %i'% (len(b1)))
print('Number of columbs : %i\n'% (len(b2)))
print('Number of first blocks   : %i -- %i'% (b1[1],b2[1]))
print('Number of last blocks    : %i -- %i'% (b1[-1],b2[-1]))
print('-------------------------------------------------------------------------------')
print('Time used [s]   : %.2f'% (calc_s))
print('Time used [min] : %.2f'% (calc_m))
print('Time used [h]   : %.2f'% (calc_h))
print('-------------------------------------------------------------------------------')

# Define the POD coupling line
def pod_coupling():
    aa = st_l + 1
    for i in range(len(homo)-1):
        for j in range(i+1,(len(homo))):
            print('Determining line for : %i -- %i'% (i,j))
            bb = (ao[j] * (homo[i]-1) + lumo[j])
            ab = aa + bb
            r_line.append(ab)
            aa = aa + (ao[i] * ao[j])

###############################################################################
# Run the collecting
pod_coupling()
###############################################################################

with open(file_out+'-lines.dat','w') as eout:
    eout.write('-------------------------------------------------------------------------------\n')
    eout.write('Number of the line\n')
    eout.write('Block\tLine\n')
    eout.write('-------------------------------------------------------------------------------\n')
    for i in range(len(r_line)):
        eout.write('%i\t%i\n'% (i+1,r_line[i]))

end    = time.time()
calc_s = end - start

calc_m = calc_s / 60.
calc_h = calc_m / 60.
print('-------------------------------------------------------------------------------')
print('Found / defined the readable lines')
print('Number of lines to be read : %i'% (len(r_line)))
print('-------------------------------------------------------------------------------')
print('Time used [s]   : %.2f'% (calc_s))
print('Time used [min] : %.2f'% (calc_m))
print('Time used [h]   : %.2f'% (calc_h))
print('-------------------------------------------------------------------------------')


print('-------------------------------------------------------------------------------')
print('----- ----- -----STARTING TO FIND THE COUPLINGS FROM THE FILE ----- ----- -----')
print('-------------------------------------------------------------------------------')
print('-------------------------------------------------------------------------------')

line_corr = [] 


# Correct readable lines 
for i in r_line:
    line_corr.append(i-1)

with open(filename,'r') as fn:
    for i,line in enumerate(fn):
        if i in line_corr:
            pod.append(float(line.split()[-1]))

###############################################################################
print('-------------------------------------------------------------------------------')
print('----- ----- -----STARTING TO WRITE THE VALUES INTO TO THE FILES---- ----- -----')
print('-------------------------------------------------------------------------------')
# Write the values in a separate file
with open(file_out+'.dat','w') as fn:
    fn.write('-------------------------------------------------------------------------------\n')
    fn.write('Block # (state #)\t\tPOD coupl. [meV]\n')
    fn.write('-------------------------------------------------------------------------------\n')
    for i in range(len(pod)):
        fn.write('%i (%i)\t-\t%i (%i)\t\t%.7f\n'% (b1[i]+1,homo[b1[i]],b2[i]+1,
                                                   homo[b2[i]],pod[i]))
###############################################################################
###############################################################################
# Create a data for excel
triu      = np.zeros((matr_d,matr_d))   # Zero matrix
ind       = np.triu_indices(matr_d)   # Define upper triagonal
triu[ind] = pod   # Add the data
pod_data  = pd.DataFrame(data=triu,index=b1,columns=[b2])   # Create a dataframe

# Write the data into excel
xls_name = file_out+'.xlsx'
pod_data.to_excel(xls_name, sheet_name='POD')
###############################################################################
###############################################################################
# Statistics - measure time
end    = time.time()
calc_s = end - start
calc_m = calc_s / 60.
calc_h = calc_m / 60.
###############################################################################
#### Testing - start
print('-------------------------------------------------------------------------------')
print('Time used [s]   : %.2f'% (calc_s))
print('Time used [min] : %.2f'% (calc_m))
print('Time used [h]   : %.2f'% (calc_h))
print('-------------------------------------------------------------------------------')
#### Testing - end
###############################################################################
