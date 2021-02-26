#!/usr/bin/python3

import os
import sys
import numpy as np
from scipy.linalg import fractional_matrix_power as mat_power

def line_f():
    print('-----------------------------------------------------------------------')

line_f()
line_f()

H1,H2 = 21,21
print('\tThe HOMO states are :  %.i - %.i states'% (H1,H2))
H1,H2 = H1-2,H2-2

# Number of states - total
x = 228

###############################################################################
x1,x2 = H1+1,H2+1
line_f()
print('\tThe coupling is between %.i - %.i states'% (x1,x2))
line_f()
line_f()

# Constants
ev    = 27.211      # au -> eV
ry    = 2.0         # au -> Ry
ry_ev = 13.606      # Ry -> eV

################################################################################

# Read matrix from CP2K output
#
# m  - storage for the matrix elements
# nb - number of basis functions
# kd - atomic kinds
# bf - number of basis functions per atomic kind
# f  - open data file
def read_matrix(m,nb,kd,bf,f):
  n_blocks = nb//3 + (1 if nb%3 else 0)
  next(f)
  for i in range(nb):
    m.append([])
  ic = 0
  for i in range(n_blocks):
    n_cols = 3 if i+1<n_blocks else nb-3*i
    # header (column numbers)
    line = next(f)
    # atomic kinds
    for j in range(len(kd)):
      # basis functions
      for k in range(bf[kd[j]-1]):
        line = next(f)
        # matrix elements
        w = line.split()
        for l in range(n_cols):
          m[ic+l].append(float(w[4+l]))
      # free line 
      next(f)
    ic += n_cols

# Read input data from the CP2K output
#
# fn - name of the file
def read_data(fn):
  # initialization 
  n_atoms = 0
  n_kinds = 0
  n_bfce = 0
  kind = []
  bfce = []
  mat_s = []
  mat_h = []
  # read the file
  with open(fn,"r") as f:
    # read number of basis functions per atomic kinds
    for line in f:
      # number of atoms
      if ('- Atoms: ' in line):
        n_atoms = int(line.split()[2])
      # number of atomic kinds
      if ('- Atomic kinds: ' in line):
        n_kinds = int(line.split()[6])
      # number of basis functions
      if ('- Spherical basis functions:' in line):
        n_bfce = int(line.split()[4])
      # basis functions per atomic kind
      if ('. Atomic kind:' in line):
        for i in range(10):
          line = next(f)
          if ('Number of spherical basis functions:' in line):
            bfce.append(int(line.split()[5]))
      # atomic kinds
      if ('ATOMIC COORDINATES' in line):
        for i in range(3):
          next(f)
        for i in range(n_atoms):
          line = next(f)
          kind.append(int(line.split()[1]))
        break
    # sanity check
    if (len(kind) != n_atoms):
      raise Exception("Inconsistent number of atoms")
    if (len(bfce) != n_kinds):
      raise Exception("Inconsistent number of atomic kinds")
    n = 0
    for i in range(len(kind)):
      n += bfce[kind[i]-1]
    if (n != n_bfce):
      raise Exception("Inconsistent number of basis functions")
    # read overlap matrix
    for line in f:
      if ('OVERLAP MATRIX' in line):
        read_matrix(mat_s,n_bfce,kind,bfce,f)
      if ('KOHN-SHAM MATRIX FOR BETA SPIN' in line):
        read_matrix(mat_h,n_bfce,kind,bfce,f)
  # return overlap matrix, hamiltonian matrix and their dimensions
  #return mat_s,mat_h,n_bfce
  return mat_s,mat_h

##########################################################################
### Defining tools / functions

########## Defining eigenvalues and -vectors for matrix (Ma)
def eigen(M):
    eig_a,eig_A = np.linalg.eig(M)

    idx      = eig_a.argsort()[::1]
    eig_a    = eig_a[idx]
    eig_A    = eig_A[:,idx]
    a_t      = np.transpose(eig_A)
    
    return eig_a, eig_A, a_t

########## Lowdin orthogonalization
# reference: 1) doi: 10.1063/1.1747632, 2) doi: 10.1002/qua.981
# Ma1 = matrix 1 (S), Ma2, = matrix 2 (H)
def lowdin_orth(M1,M2):
    '''Formation of A^-1/2'''
    Sq_s = mat_power(M1,-0.5)

    '''Orthoganilzation'''
    orth_h = np.linalg.multi_dot([Sq_s,M2,Sq_s])
    return orth_h, Sq_s


########## Partition of blocks
# dd = upper left, da = lower left, ad = upper right, ad = lower right
# Ma = matrix, N = number of states
def partition(M,n):
    '''Separate the blocks'''
    #n = int(n)
    #print(isinstance(n,int))
    #print('Type of matrix')
    #print(type(M))
    #print('Shape')
    #print(np.shape(M))
    #print('Slice')
    #print(n,n)
    n = int(n)
    dd = np.array(M[:n, :n])
    da = np.array(M[n:, :n])
    ad = np.array(M[:n, n:])
    aa = np.array(M[n:, n:])
    #print('New shape')
    #print(np.shape(ad))
    #line_f()
    return dd,da,ad,aa

### Defining tools / functions : END
##########################################################################

##########################################################################
### Projector operator diagonalization

# doi: 10.1021/acs.jpcc.7b06566

def pod(h,s,n):
    #print('POD')
    #print('Dimensions')
    #print(n)
    #print('New dimensions')
    
    n = n // 2
    #print(n)
    '''Lowdin'''
    H_,s_sq = lowdin_orth(s,h)

    '''Partition'''
    h_dd, h_da, h_ad, h_aa = partition(H_,n)
    
    '''Fragment eigenstates and -vectors'''
    u,U,Ut = eigen(h_dd)
    v,V,Vt = eigen(h_aa)

    '''Diagonalization / E.couplings'''
    H_ad = np.linalg.multi_dot([Ut,h_ad,V])
    H_da = np.linalg.multi_dot([Vt,h_da,U])
    
    HH_ad = H_ad[H1,H2]
    HH_ad = 1000*ev*HH_ad

    #H_ad = np.reshape(H_ad,(n2,1))
    H_ad = 1000*ev*H_ad
    H_ad_re = 1000*ev*H_ad
    
    #return H_ad, HH_ad
    return HH_ad

# doi: 10.1021/acs.jctc0c00887

def pod2(h,s,n):
    #print('POD2')
    #print('Dimensions')
    #print(n)
    #print('New dimensions')
    
    n = n // 2
    #print(n)
    '''Partition of H and S'''
    h = np.reshape(h,((n*2),(n*2)))
    s = np.reshape(s,((n*2),(n*2)))
    h_dd, h_ad, h_da, h_aa = partition(h,n)
    s_dd, s_ad, s_da, s_aa = partition(s,n)

    '''Lowdin'''
    H_dd,S_dd_sq = lowdin_orth(s_dd,h_dd)
    H_aa,S_aa_sq = lowdin_orth(s_aa,h_aa)

    '''Fragment eigenstates / E.coupling'''
    H_dd_u, H_dd_U, H_dd_Ut = eigen(H_dd)
    H_aa_u, H_aa_U, H_aa_Ut = eigen(H_aa)

    #H_aa_U  = np.matmul(S_aa_sq,H_aa_U)
    H_aa_Ut = np.transpose(H_aa_U)
    #H_dd_U  = np.matmul(S_dd_sq,H_dd_U)
    H_dd_Ut = np.transpose(H_dd_U)

    Had = np.linalg.multi_dot([S_aa_sq,h_ad,S_dd_sq])
    Hda = np.linalg.multi_dot([S_dd_sq,h_da,S_aa_sq])

    #Hdd = np.linalg.multi_dot([H_dd_Ut,h_dd,H_dd_U])
    Had = np.linalg.multi_dot([H_aa_Ut,Had,H_dd_U])
    Hda = np.linalg.multi_dot([H_dd_Ut,Hda,H_aa_U])
    #Haa = np.linalg.multi_dot([H_aa_Ut,h_aa,H_aa_U])

    ''' If needed, here again: partition of blocks '''
    HH_diag_ad = Had[H1,H2]
    #H_diag_ad = np.reshape(Had,(n2,1))
    H_ad = 1000*ev*Had
    HH_diag_ad = 1000*ev*HH_diag_ad
    
    #return H_ad, HH_diag_ad
    return HH_diag_ad


# doi: 10.1021/acs.jctc0c00887

def pod2l(h,s,n):
    #print('POD2L')
    #print('Dimensions')
    #print(n)
    #print('New dimensions')
    
    n = n // 2
    #print(n)
    '''Partition of H and S'''
    h = np.reshape(h,((n*2),(n*2)))
    s = np.reshape(s,((n*2),(n*2)))
    h_dd, h_ad, h_da, h_aa = partition(h,n)
    s_dd, s_ad, s_da, s_aa = partition(s,n)

    ''' Lowdin'''
    H_dd,S_dd_sq = lowdin_orth(s_dd,h_dd)
    H_aa,S_aa_sq = lowdin_orth(s_aa,h_aa)

    ''' Fragment eigenstates / E.coupling'''
    H_dd_u, H_dd_U, H_dd_Ut = eigen(H_dd)
    H_aa_u, H_aa_U, H_aa_Ut = eigen(H_aa)

    ed = H_aa_u[H1]
    ea = H_dd_u[H2]

    '''Print eigenvalues around HOMO states'''
    line_f()
    print('''Eigenstates : ea,ed''')
    print(ea,ed)
    line_f()
    aaa = H_aa_u[H1-4:H1+4]
    ddd = H_dd_u[H2-4:H2+4]
    print('''eigenvalues : HOMO-4 --- LUMO+3   *** ea, ed''')
    print(aaa)
    line_f()
    print(ddd)
    line_f()
    '''END print eigenvalues'''

    H_aa_Ut = np.transpose(H_aa_U)
    H_dd_Ut = np.transpose(H_dd_U)

    Had = np.linalg.multi_dot([S_aa_sq,h_da,S_dd_sq])
    Hda = np.linalg.multi_dot([S_dd_sq,h_ad,S_aa_sq])
    Sad = np.linalg.multi_dot([S_aa_sq,s_ad,S_dd_sq])
    Sda = np.linalg.multi_dot([S_dd_sq,s_da,S_aa_sq])

    line_f()
    print('''S element before and after transform''')
    print(s_ad[H1,H2],Sad[H1,H2])
    line_f()
    sad = Sad[H1,H2]

    print('''H element : After S-transform''')
    print(Had[H1,H2])
    line_f()
    
    #Hdd = np.linalg.multi_dot([H_dd_Ut,h_dd,H_dd_U])
    Had = np.linalg.multi_dot([H_aa_Ut,Had,H_dd_U])
    Hda = np.linalg.multi_dot([H_dd_Ut,Hda,H_aa_U])
    #Haa = np.linalg.multi_dot([H_aa_Ut,h_aa,H_aa_U])

    print('''H element : After Unitary transform''')
    print(Had[H1,H2])
    line_f()
    had_pod2 = Had[H1,H2]
    
    '''Effective coupling / Lowdin'''
    H_eff_ad = (had_pod2 - 0.5*(ea+ed)*sad) / (1.0 - (sad**2))
    return 1000*ev*H_eff_ad

### Projector operator diagonalization : END
##########################################################################

##########################################################################

def main():
    if (len(sys.argv)!=2):
        print('usage: pod-method <cp2k-output>')
        sys.exit(1)
    if (os.path.isfile(sys.argv[1])):
        s,h     = read_data(sys.argv[1])
        #print('H matrix')
        #print(h)
        a_pod   = pod(h,s,x)
        a_pod2  = pod2(h,s,x)
        a_pod2l = pod2l(h,s,x)

        line_f()
        print('''POD''')
        print(a_pod)
        line_f()
        print('''POD2''')
        print(a_pod2)
        line_f()
        print('''POD2L''')
        print(a_pod2l)
        line_f()
    else:
        print('ERROR')

if __name__=='__main__':
    main()

### Printing the electronic couplings : END
##########################################################################
#
#                             FIN
#
##########################################################################
