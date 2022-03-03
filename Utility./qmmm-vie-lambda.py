'''
Calculates the vertical energy gap from .dat file that contains QM energies
of the system
'''

##########################################################################
import numpy as np
import pandas as pd
import os, sys
ev = 27.211
kBT = 0.026

# A step for rolling average
step_i = 50                 # Step as an intereger for functions
step_s = str(step_i)        # Step as string for file names
##########################################################################

##########################################################################
#    Read the data from a file
# m_ = mechanical, e_ = electric, _e = embedding
# 0 = ground state, 1 = excited states
def read_data(fn):
    me_0 = []
    me_1 = []
    ee_0 = []
    ee_1 = []
    with open(fn, 'r') as f:
        for line in f:
            if 'me-0' in line:
                me_0.append(float(line.split(',')[-1]))
            if 'me-1' in line:
                me_1.append(float(line.split(',')[-1]))
            if 'ee-0' in line:
                ee_0.append(float(line.split(',')[-1]))
            if 'ee-1' in line:
                ee_1.append(float(line.split(',')[-1]))
    return me_0,me_1,ee_0,ee_1
##########################################################################

##########################################################################
#    Calculating the vertical gap depending the system - both mechanical
#    and electric
# m = mechanical, e = electric, 0 = ground st., 1 = excited st.,
# l = sample-#
def vertical_gap(m0,m1,e0,e1,b,lm,le):
    dE_m = []
    dE_e = []
    if b == 'o':
        for i in range(lm):
            dE_m.append(m0[i]-m1[i])
        for i in range(le):
            dE_e.append(e0[i]-e1[i])
    if b == 'r':
        for i in range(lm):
            dE_m.append(m1[i]-m0[i])
        for i in range(le):
            dE_e.append(e1[i]-e0[i])
    
    return dE_m, dE_e
##########################################################################

##########################################################################
# dex = list of vertical gaps, y = ox/rd
def IE_average(dem,dee,y,yn):
    l_all   = len(dem)
    dem_avg,dee_avg     = [], []
    dem_avg_a,dee_avg_a = [], []

    '''
    Vertical energy gap in eV
    '''
    avr_m = np.average(dem)
    avr_m = avr_m*ev

    avr_e = np.average(dee)
    avr_e = avr_e*ev

    '''
    Convergence of the energy gap in au
    '''

    for i in range(l_all):
        if i> 450:
            a     = 500 - (i+50)
            b     = 500 + a
            x1,x2 = sum(dem[i:]),sum(dem[b:])
            x3,x4 = sum(dee[i:]),sum(dee[b:])
            dem_avg.append((x1+x2)/50)
            dee_avg.append((x3+x4)/50)
        else:
            dem_avg.append((sum(dem[i:50+i]))/50)
            dee_avg.append((sum(dee[i:50+i]))/50)
            
    for i in range(l_all):
        dem_avg_a.append((sum(dem[0:i]))/(i+1))
        dee_avg_a.append((sum(dee[0:i]))/(i+1))
    
    if y == 'o':
        system = 'Oxidized'
    if y == 'r':
        system = 'Reduced'

    '''
    Write the convergence array into a file in eV
    '''
    dem_avg = pd.DataFrame(dem_avg)
    dee_avg = pd.DataFrame(dee_avg)
    dem_avg = dem_avg*ev
    dee_avg = dee_avg*ev
    dem_avg.to_csv('dE-m-avg-'+step_s+'-'+yn+'.dat', header='dE-m'+y, index='Sample nro')
    dee_avg.to_csv('dE-e-avg-'+step_s+'-'+yn+'.dat', header='dE-e'+y, index='Sample nro')
    
    dem_avg_a = pd.DataFrame(dem_avg_a)
    dee_avg_a = pd.DataFrame(dee_avg_a)
    dem_avg_a = dem_avg_a*ev
    dee_avg_a = dee_avg_a*ev
    dem_avg_a.to_csv('dE-m-avg-'+yn+'.dat', header='dE-m'+y, index='Sample nro')
    dee_avg_a.to_csv('dE-e-avg-'+yn+'.dat', header='dE-e'+y, index='Sample nro')

    '''
    Printing the results on screen
    '''
    print('''------------------------------------------------------------\n''')
    print('------------- Mechanical, %s'% (system))
    print('The average vertical gap [eV]      : %.3f\n'% (avr_m))
    print('------------- Electric, %s'% (system))
    print('The average vertical gap [eV]      : %.3f'% (avr_e))
    print('''------------------------------------------------------------\n''')
    return avr_e,avr_m
##########################################################################

##########################################################################
# Lambda values
# e1 = IE_av of ox, e2 = IE_av of rd
# ee1 = electric emb of ox in ground st., ee0 = electric emb. of rd in ground st.
def lambda_value(e1,e2,ee1,ee0):
    '''
    Stokes in eV
    '''
    L_st = 0.5*(e2-e1)

    '''
    Variational in eV
    '''
    var_o = np.var(ee1)
    L_var_o = 0.5*(var_o / kBT)
    ###########DEBUGGING#############################
    var_o_s  = np.sqrt(var_o)
    var_o_2  = var_o*var_o

    var_r = np.var(ee0)
    L_var_r = 0.5*(var_r / kBT)
    ###########DEBUGGING#############################
    var_r_s  = np.sqrt(var_r)
    var_r_2  = var_r*var_r

    print('#########################################################################')
    print('-----DEBUGGING---------VARIANCE TEST-------------------------------------')
    print('#########################################################################')
    print('Variance - as it is, ox   : %.6f'% (var_o))
    print('Variance - sqrt, ox       : %.6f'% (var_o_s))
    print('Variance - power to 2, ox : %.6f'% (var_o_2))
    print('-------------------------------------------------------------------------')
    print('Variance - as it is, rd   : %.6f'% (var_r))
    print('Variance - sqrt, rd       : %.6f'% (var_r_s))
    print('Variance - power to 2, rd : %.6f'% (var_r_2))
    print('#########################################################################')
    print('-----DEBUGGING---------LAMBDA TEST---------------------------------------')
    print('#########################################################################')
    print('Variance - as it is, ox   : %.6f'% (0.5*(var_o/kBT)))
    print('Variance - sqrt, ox       : %.6f'% (0.5*(var_o_s/kBT)))
    print('Variance - power to 2, ox : %.6f'% (0.5*(var_o_2/kBT)))
    print('-------------------------------------------------------------------------')
    print('Variance - as it is, rd   : %.6f'% (0.5*(var_r/kBT)))
    print('Variance - sqrt, rd       : %.6f'% (0.5*(var_r_s/kBT)))
    print('Variance - power to 2, rd : %.6f'% (0.5*(var_r_2/kBT)))
    print('#########################################################################')
    print('------------------------DEBUGGING END------------------------------------')
    print('#########################################################################')
    
    '''
    Print the results on screen in eV
    '''
    print('''------------- Lambda''')
    print('The lambda (var) value [eV] for ox : %.3f'% (L_var_o))
    print('The lambda (var) value [eV] for rd : %.3f'% (L_var_r))
    print('The lambda (stk) value [eV]        : %.3f'% (L_st))
    print('''------------------------------------------------------------''')
##########################################################################

##########################################################################
def main():
    if len(sys.argv) > 4:
        print(('Try : this_program x-name.dat r-name.dat'))
        sys.exit(1)
    if (os.path.isfile(sys.argv[1]) or os.path.isfile(sys.argv[2])):
        x1,x2 = str((sys.argv[1]).split('-')[0]),str((sys.argv[2].split('-')[0]))
        x1 = str((sys.argv[1]).split('-')[0])
        x2 = str((sys.argv[2].split('-')[0]))
        #------------------------------------------------------------
        if x1 == 'ox':
            o,on = 'o','o'
        if x1 == 'o1' or x1 == 'o2':
            o,on = 'o',x1
        #------------------------------------------------------------
        if x2 == 'rd':
            r,rn = 'r','r'
        if x2 == 'r1' or x2 == 'r2':
            r,rn = 'r',x2
        #------------------------------------------------------------

        me0_o,me1_o,ee0_o,ee1_o = read_data(sys.argv[1])
#        me0_o,me1_o,ee0_o,ee1_o = me0_o[129:],me1_o[129:],ee0_o[129:],ee1_o[129:]
        me0_r,me1_r,ee0_r,ee1_r = read_data(sys.argv[2])
        lm_o,le_o = len(me0_o), len(ee0_o)
        lm_r,le_r = len(me0_r), len(ee0_r)
        
        dEm_o,dEe_o = vertical_gap(me0_o,me1_o,ee0_o,ee1_o,o,lm_o,le_o)
        dEm_r,dEe_r = vertical_gap(me0_r,me1_r,ee0_r,ee1_r,r,lm_r,le_r)

        '''
        Collect datas into separate files - just in case
        
        OBS! Filenames are printed so plot-x.py programs work
        automatically!
        '''
        ee0_df_o = pd.DataFrame(ee0_o)
        ee1_df_o = pd.DataFrame(ee1_o)
        ee0_df_o.to_csv('ee0-'+step_s+'-'+on+'.dat')
        ee1_df_o.to_csv('ee1-'+step_s+'-'+on+'.dat')
        #------------------------------------------------------------
        me0_df_o = pd.DataFrame(me0_o)
        me1_df_o = pd.DataFrame(me1_o)
        me0_df_o.to_csv('me0-'+step_s+'-'+on+'.dat')
        me1_df_o.to_csv('me1-'+step_s+'-'+on+'.dat')
        #############################################################
        ee0_df_r = pd.DataFrame(ee0_r)
        ee1_df_r = pd.DataFrame(ee1_r)
        ee0_df_r.to_csv('ee0-'+step_s+'-'+rn+'.dat')
        ee1_df_r.to_csv('ee1-'+step_s+'-'+rn+'.dat')
        #------------------------------------------------------------
        me0_df_r = pd.DataFrame(me0_r)
        me1_df_r = pd.DataFrame(me1_r)
        me0_df_r.to_csv('me0-'+step_s+'-'+rn+'.dat')
        me1_df_r.to_csv('me1-'+step_s+'-'+rn+'.dat')
        #############################################################
        dEm_df_o = pd.DataFrame(dEm_o)
        dEm_df_o = dEm_df_o*ev
        dEm_df_o.to_csv('dEm-'+step_s+'-'+on+'.dat')
        dEe_df_o = pd.DataFrame(dEe_o)
        dEe_df_o = dEe_df_o*ev
        dEe_df_o.to_csv('dEe-'+step_s+'-'+on+'.dat')
        #------------------------------------------------------------
        dEm_df_r = pd.DataFrame(dEm_r)
        dEm_df_r = dEm_df_r*ev
        dEm_df_r.to_csv('dEm-'+step_s+'-'+rn+'.dat')
        dEe_df_r = pd.DataFrame(dEe_r)
        dEe_df_r = dEe_df_r*ev
        dEe_df_r.to_csv('dEe-'+step_s+'-'+rn+'.dat')
        #############################################################

        shape_o = np.shape(dEe_df_o)
        shape_r = np.shape(dEe_df_r)
        if shape_o == shape_r:
            dEe_gap = np.concatenate((dEe_df_o,dEe_df_r), axis=1)
            dEe_gap = pd.DataFrame(dEe_gap)
            dEe_gap.to_csv('dEe-'+step_s+'-'+on+'-'+rn+'.dat')
        if shape_o < shape_r:
            dEe_d_rx = dEe_df_r[:shape_o[0]]
            dEe_gap = np.concatenate((dEe_df_o,dEe_d_rx), axis=1)
            dEe_gap = pd.DataFrame(dEe_gap)
            dEe_gap.to_csv('dEe-'+step_s+'-'+on+'-'+rn+'.dat')
        if shape_o > shape_r:
            dEe_d_ox = dEe_df_o[:shape_r[0]]
            dEe_gap = np.concatenate((dEe_d_ox,dEe_df_r), axis=1)
            dEe_gap = pd.DataFrame(dEe_gap)
            dEe_gap.to_csv('dEe-'+step_s+'-'+on+'-'+rn+'.dat')

        '''
        Calculating the:
        - VIE
        - lambda
        '''

        # Returns values for electric embedding
        e_o,m_o = IE_average(dEm_o,dEe_o,o,on)
        e_r,m_r = IE_average(dEm_r,dEe_r,r,rn)

        print('------------------------Elstat.emb.-----------------------------------')
        #lambda_value(e_o,e_r,ee0_o,ee0_r)
        lambda_value(e_o,e_r,dEe_df_o,dEe_df_r)
        print('------------------------Mech..emb.------------------------------------')
        #lambda_value(e_o,e_r,ee0_o,ee0_r)
        lambda_value(m_o,m_r,dEm_df_o,dEm_df_r)
    else:
        print('What are you doing?')
        print(('Try : this_program x-name.dat r-name.dat'))
##########################################################################

##########################################################################
if __name__ == '__main__':
    main()
##########################################################################
