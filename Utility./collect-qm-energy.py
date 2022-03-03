'''
This program creates a data file out of grep'ed energies from QM/MM calculation. 
'''

##########################################################################
import numpy as np
import pandas as pd
import os
import sys
##########################################################################
# One of these:
# ox, rd, o1, o2, r1, r2
syst='o2'
##########################################################################
def read_file(file):
    energy = []
    smpl1  = []
    smpl   = []
    em_ee  = []
    with open(file, 'r') as f:
        for line in f:
            if 'QM inner-part energy' in line:
                energy.append(float(line.split()[4]))
            if 'system.log' in line:
                smpl1.append(str(line.split('/')[1]))
                em_ee.append(str(line.split('/')[2]))
    for i in smpl1:
        #smpl.append(str('sample-'+i.split('-')[1]))
        smpl.append(str(i.split('-')[-1]))
    '''
    Sorting the values -for clarity
    '''
    energy = np.array(energy)
    smpl   = np.array(smpl)
    em_ee  = np.array(em_ee)
    ix     = smpl.argsort()[::1]
    #print(ix)
    smpl   = smpl[ix]
    energy = energy[ix]
    em_ee  = em_ee[ix]

    return energy, smpl, em_ee
##########################################################################

##########################################################################
def write_data(energ,smpl,em):
    en = len(energ)
    es = len(smpl)
    el = len(em)
    data_s1 = []
    data_m1 = []
    title = 'Energy [au]'

    if en == es and en==el:
        '''
        Remove dublicates
        '''
        data_s = list(dict.fromkeys(smpl))
        for i in data_s:
            data_s1.append(str('sample-'+i))
        data_s = data_s1
        es = len(data_s)
        
        data_m = list(dict.fromkeys(em))
        for i in data_m:
            data_m1.append(str(i))
        data_m = data_m1
        el = len(data_m)

        '''
        Create a data frame of data
        '''
        #samps = [data_s,data_m]
        samps = [smpl,em]
        print(samps)
        #all_samps = pd.MultiIndex.from_product(samps)
        all_samps = list(zip(*samps))
        print(np.shape(all_samps))
        print(all_samps)

        df = pd.DataFrame(data=energ, index=all_samps)
        print(df)
       
        ''' 
        Write data into a new file
        sample me-0/ee-1 energy
        '''
        #np.savetxt('r-qm-energies.dat', data, newline='\n')
        #pd.DataFrame.to_csv('r-qm-eneries.dat', sep=' ', index=False, header=False,columns=data)
        df.to_csv(syst+'-qmmm-energy.dat')

    else:
        print("Incocnsistent amount of samples!")
##########################################################################

##########################################################################
def main():
    if len(sys.argv)!=2:
        print('try: python <program.py> <filename>')
        sys.exit(1)
    if os.path.isfile(sys.argv[1]):
        qm_energies,sample,em_e = read_file(sys.argv[1])
        write_data(qm_energies,sample,em_e)
    else:
        print('What are you trying to do? There is no such file.')
##########################################################################

##########################################################################
if __name__=='__main__':
    main()
##########################################################################
