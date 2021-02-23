'''
Projection-operated-diabatization (POD).

A program to extract electronic coupling (and state energies) from 
H and S matrices.

---wilhelmiina/pengu1ne
'''
### Libraries
import numpy as np
import scipy as sci
from scipy.linalg import eig
from scipy.linalg import fractional_matrix_power as mat_power


### Constants
ev    = 27.211        # au -> eV
ry    = 2.0           # au -> Ry
ry_ev = 13.606        # Ry -> eV

### Just for testing
def line_f():
    print('''-------------------------------------------------------------''')

def test_():
    line_f()
    print('''TEST''')
    line_f()

'''
Read the output files
Read the file and determine fragments
'''
#####################################################################
### CHANGE PART 

# Name of the output file
f_out = 'he2-dimer-25-631gp.out'
# General name for outputs
name  = 'he2-dimer-25-631gp-np'

# Found under the OVERLAP / HAMILTONIAN MATRIX
# The first rows, where S and H matrices start, the header
s1 = 371
h1 = 501
# The last rows: either the first blank row OR
# if the last block is different shape, its header
sn = 378
hn = 508
# The second header line for S matrix
s2 = 378

# Found under electronic coupling
# Number of first block atomic states
ao_n = 2
# Total number of AO basis functions
ao_tot = 4

### CHANGE PART : END
##########################################################################

#########################################################################
### Creating the numbers for Python
frag1 = np.arange(1,(ao_n+1))               # nr of ao's of 1. system
n     = len(frag1)
frag2 = range((ao_n+1),(ao_tot+1))          # nr of ao's of 2. system
m     = len(frag2)
nm    = n+m                                 # shape of the whole system (nm,nm)
n2    = n*m                                 # size of ad/da blocks
b     = s2 - s1                             # The number of lines between 'blocks'

h1 = h1 - b
s1 = s1 - b

hl = hn - b
sl = sn - b

H = []
S = []
x = 1
y = 1

### Creating numbers : END
#####################################################################

#####################################################################
### Creating Hamiltonian and overlap matrices


###                      Hamiltonian
while h1 < hl:
    h1 += b
    Hi = np.genfromtxt(f_out, skip_header=h1, max_rows=ao_tot, usecols=(4,5,6))
    if x == 1:
        x += 1
        H = Hi
    else:
        H = np.block([H,Hi])

# Uncommand if the last lines are different shapes
Hii = np.genfromtxt(f_out, skip_header=hn, max_rows=ao_tot, usecols=(4))
Hii = np.reshape(Hii,(ao_tot,1))
H   = np.block([H,Hii])


###                      Overlap
while s1 < sl:
    s1 += b
    Si = np.genfromtxt(f_out, skip_header=s1, max_rows=ao_tot, usecols=(4,5,6))
    if y == 1:
        y += 1
        S = Si
    else:
        S = np.block([S,Si])

# Uncommand if the last lines are different shapes
Sii = np.genfromtxt(f_out, skip_header=sn, max_rows=ao_tot, usecols=(4))
Sii = np.reshape(Sii,(ao_tot,1))
S   = np.block([S,Sii])

#line_f()
#print('''Check : H ''')
#print(H)
#line_f()
#line_f()
#print('''Check : S ''')
#print(S)
#line_f()

# For testing, uncommand
#print(np.shape(H),np.shape(Hii))
#print(np.shape(S),np.shape(Sii))

# Writing the files
np.savetxt(name+'-hamiltonian.out', H, fmt='%.10f', delimiter='\t')
np.savetxt(name+'-overlap.out', S, fmt='%.10f', delimiter='\t')

### Creating matrices and save them : END
##########################################################################

##########################################################################
### OPTIONAL: Reading the matrices from a file

### Hamiltonian
#H = np.genfromtxt(name+'hamiltonian.out', delimiter='\t')
#H = np.reshape(H,(nm,nm))
# Overlap matrix
#S = np.genfromtxt(name+'overlap.out', delimiter='\t')
#S = np.reshape(S,(nm,nm))

### Reading the matrices from a file : END
##########################################################################

##########################################################################
### Defining tools / functions

########## Defining eigenvalues and -vectors for matrix (Ma)
# ERRRO! Check the theory!
def eigen(Ma):
    eig_a,eig_A = np.linalg.eig(Ma)

    idx      = eig_a.argsort()[::1]
    eig_a    = eig_a[idx]
    eig_A    = eig_A[:,idx]
    a_t      = np.transpose(eig_A)
    
    return eig_a, eig_A, a_t

########## Lowdin orthogonalization
# reference: 1) doi: 10.1063/1.1747632, 2) doi: 10.1002/qua.981
# Ma1 = matrix 1 (S), Ma2, = matrix 2 (H)
def lowdin_orth(Ma1,Ma2):
    '''Formation of A^-1/2'''
    Sq_s = mat_power(Ma1,-0.5)

    '''Orthoganilzation'''
    orth_h = np.linalg.multi_dot([Sq_s,Ma2,Sq_s])
    return orth_h, Sq_s


########## Partition of blocks
# dd = upper left, da = lower left, ad = upper right, ad = lower right
# If all blocks are needed, modify accordingly
def partition(Ma):
    '''Separate the blocks'''
    dd = np.array(Ma[:n, :n])
    da = np.array(Ma[n:, :n])
    ad = np.array(Ma[:n, n:])
    aa = np.array(Ma[n:, n:])
    return dd,da,ad,aa

### Defining tools / functions : END
##########################################################################

##########################################################################
### Projector operator diagonalization

# doi: 10.1021/acs.jpcc.7b06566

def pod(h,s):
    '''Lowdin'''
    H_,s_sq = lowdin_orth(s,h)

    '''Partition'''
    h_dd, h_da, h_ad, h_aa = partition(H_)

    '''Fragment eigenstates and -vectors'''
    u,U,Ut = eigen(h_dd)
    v,V,Vt = eigen(h_aa)

    '''Diagonalization / E.couplings'''
    H_ad = np.linalg.multi_dot([Ut,h_ad,V])
    H_da = np.linalg.multi_dot([Vt,h_da,U])

    H_ad = np.reshape(H_ad,(n2,1))
    H_ad = 1000*ev*H_ad
    return H_ad

# doi: 10.1021/acs.jctc0c00887

def pod2(h,s):
    '''Partition of H and S'''
    h_dd, h_da, h_ad, h_aa = partition(h)
    s_dd, s_da, s_ad, s_aa = partition(s)

    ''' Lowdin'''
    H_dd,S_dd_sq = lowdin_orth(s_dd,h_dd)
    H_aa,S_aa_sq = lowdin_orth(s_aa,h_aa)

    ''' Fragment eigenstates / E.coupling'''
    H_dd_u, H_dd_U, H_dd_Ut = eigen(H_dd)
    H_aa_u, H_aa_U, H_aa_Ut = eigen(H_aa)

    H_aa_U  = np.matmul(S_aa_sq,H_aa_U)
    H_aa_Ut = np.transpose(H_aa_U)
    H_dd_U  = np.matmul(S_dd_sq,H_dd_U)
    H_dd_Ut = np.transpose(H_dd_U)

    Hdd = np.linalg.multi_dot([H_dd_Ut,h_dd,H_dd_U])
    Hda = np.linalg.multi_dot([H_dd_Ut,h_da,H_aa_U])
    Had = np.linalg.multi_dot([H_aa_Ut,h_ad,H_dd_U])
    Haa = np.linalg.multi_dot([H_aa_Ut,h_aa,H_aa_U])

    H  = np.block([[Hdd,Hda],[Had,Haa]])
    
    ''' If needed, here again: partition of blocks '''
    H_diag_dd,H_diag_da,H_diag_ad,H_diag_aa = partition(H)
    H_diag_ad = np.reshape(H_diag_ad,(n2,1))
    H_ad = 1000*ev*H_diag_ad
    
    return H_ad


# doi: 10.1021/acs.jctc0c00887

def pod2l(h,s):
    '''Partition of H and S'''
    h_dd, h_da, h_ad, h_aa = partition(h)
    s_dd, s_da, s_ad, s_aa = partition(s)

    ''' Lowdin --- I'''
    H_dd,S_dd_sq = lowdin_orth(s_dd,h_dd)
    H_aa,S_aa_sq = lowdin_orth(s_aa,h_aa)

    ''' Fragment eigenstates '''
    H_dd_u, H_dd_U, H_dd_Ut = eigen(H_dd)
    H_aa_u, H_aa_U, H_aa_Ut = eigen(H_aa)

    H_aa_U  = np.matmul(S_aa_sq,H_aa_U)
    H_aa_Ut = np.transpose(H_aa_U)
    H_dd_U  = np.matmul(S_dd_sq,H_dd_U)
    H_dd_Ut = np.transpose(H_dd_U)
    
    Hdd = np.linalg.multi_dot([H_dd_Ut,h_dd,H_dd_U])
    Hda = np.linalg.multi_dot([H_dd_Ut,h_da,H_aa_U])
    Had = np.linalg.multi_dot([H_aa_Ut,h_ad,H_dd_U])
    Haa = np.linalg.multi_dot([H_aa_Ut,h_aa,H_aa_U])

    H  = np.block([[Hdd,Hda],[Had,Haa]])

    ''' Lowdin --- II '''
    #H_eff,xx  = lowdin_orth(s,H)
    #H_eff_dd,H_eff_da,H_eff_ad,H_eff_aa = partition(H_eff)

    ''' Effective coupling '''
    s_ad2 = np.matmul(s_ad,s_ad)
    s_da2 = np.matmul(s_da,s_da)
    H_diag = Hdd + Haa

    x_ad = 0.5*(np.matmul(H_diag,s_ad))
    x_da = 0.5*(np.matmul(H_diag,s_da))
    x_ad = Had - x_ad
    x_da = Hda - x_da
    y_ad = 1.0 - s_ad2
    y_da = 1.0 - s_da2

    H_eff_ad = np.divide(x_ad,y_ad)
    H_eff_da = np.divide(x_da,y_da)

    '''Finalizing'''
    H_ad = np.reshape(H_eff_ad,(n2,1))
    H_ad = 1000*ev*H_ad
    return H_ad

### Projector operator diagonalization : END
##########################################################################

##########################################################################
### Printing the electronic couplings

# Print on screen
Hpod   = pod(H,S)
Hpod2  = pod2(H,S)
Hpod2l = pod2l(H,S)
line_f()
#print('''The electronic coupling for beta electrons in meV:''')
#line_f()
#line_f()
#print('\t'+name+'\t')
#line_f()
#line_f()
#print('''POD''')
#print(H_pod)
#line_f()
#print('''POD2''')
#print(H_pod2)
#line_f()
#print('''POD2L''')
#print(H_pod2l)

# Print into file

np.savetxt(name+'-pod.elcoup', Hpod, fmt='%.8f', delimiter='\t' )
np.savetxt(name+'-pod2.elcoup', Hpod2, fmt='%.8f', delimiter='\t' )
np.savetxt(name+'-pod2l.elcoup', Hpod2l, fmt='%.8f', delimiter='\t' )

### Printing the electronic couplings : END
##########################################################################

line_f()
print('''
Calculation DONE!
''')
line_f()

##########################################################################
#
#                             FIN
#
##########################################################################
