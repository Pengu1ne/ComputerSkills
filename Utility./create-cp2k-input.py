'''
This program creates an input for CP2K calculations from .pbd file with a
separate POD block for each amino acids and surface separately.

-wilhelmiina/Pengu1ne
'''
###############################################################################
# Import modules
import numpy as np
import sys,os
###############################################################################
###############################################################################
#Determine the amino acid(s) and atoms
def collect_aa(file_pbd):
    aa_n,aa_i,at_n,at_i = [],[],[],[]
    'Open file'
    with open(file_pbd,'r') as pbd:
        for line in pbd:
            'Collect names and ndx'
            if 'ATOM' in line:
                aa_n.append(line.split()[3])
                aa_i.append(int(line.split()[4]))
                at_n.append(line.split()[2])
    'Count atoms per residue'
    for i in range(max(aa_i)):
        at_i.append(aa_i.count(i+1))

    return aa_n,aa_i,at_n,at_i

###############################################################################
###############################################################################
# Define starting and ending atoms per residue and remove dublicates
# aa_first = list of first index numbers, aa_last = list of last index numbers
def define_blocks(aan,aai,ati):
    aa_first,aa_last = [],[]
    an,ai            = [],[]
    ll = len(ati) + 1

    'Index of the last atom per residue'
    for i in range(ll):
        aa_last.append(sum(ati[:i]))

    'Index of the first atom per residue'
    for i in range(ll):
        aa_first.append((aa_last[i])+1)

    'Remove out of range values'
    aa_last.pop(0)
    aa_first.pop(-1)

    'Remove dublicates for naming'
    for i in aa_first:
        an.append(aan[i-1])
        ai.append(aai[i])
    return aa_first,aa_last,an,ai

###############################################################################
###############################################################################
# Determine atoms
def define_atoms(atn):
    atoms = []

    'Collect the elements'
    for i in atn:
        if i == 'CU':
            atoms.append('Cu')
        elif i[0] == 'A':
            atoms.append('Au')
        else:
            atoms.append(i[0])

    return atoms

###############################################################################
###############################################################################
#Compute electrons
def define_electrons(start,end,elements):
    n_el = []
    'Sanity check'
    l1,l2 = len(start),len(end)
    if l1!=l2:
        print('Something is wrong. Inequalent amount of atoms etc.')
        sys.exit(1)
    else:
        for i in range(l1):
            'Cut the amino acids from the element list'
            a_acid = elements[(start[i]-1):(end[i])]
            'Electron count'
            n_el.append(atom_electrons(a_acid))

    return n_el
###############################################################################
###############################################################################
# Define charges for atoms
def atom_electrons(x):
    el = 0
    for i in x:
        if i=='H':
            el += 1
        elif i=='C':
            el += 4
        elif i=='N':
            el += 5
        elif i=='O':
            el += 6
        elif i=='S':
            el += 6
        elif i=='Cu':
            el += 11
        elif i=='Au':
            el += 11
    return el
###############################################################################
###############################################################################
#Write the input
def write_input_global(inp_name):
    with open(inp_name+'.inp', 'w') as inp_n:
        inp_n.write('# Global settings\n')
        inp_n.write('&GLOBAL\n')
        inp_n.write('  ECHO_INPUT .false.\n')
        inp_n.write('  PRINT_LEVEL medium\n')
        inp_n.write('  PROGRAM_NAME cp2k\n')
        inp_n.write('  PROJECT_NAME au-azu-junction-2-ec\n')
        inp_n.write('  RUN_TYPE energy\n')
        inp_n.write('  SAVE_MEM .true.\n')
        inp_n.write('  SEED 50801\n')
        inp_n.write('  WALLTIME 24:00:00\n')
        inp_n.write('  &TIMINGS\n')
        inp_n.write('    TRESHOLD 1.0e-3\n')
        inp_n.write('  &END\n')
        inp_n.write('&END GLOBAL\n')
        inp_n.write('&FORCE_EVAL\n')
        inp_n.write('  # Electronic structure\n')
        inp_n.write('  METHOD qs\n')
        inp_n.write('  STRESS_TENSOR none\n')

def write_input_dft_qs_scf_xc(inp_name):
    with open(inp_name+'.inp', 'a') as inp_n:
        inp_n.write('  # DFT settings\n')
        inp_n.write('  &DFT\n')
        inp_n.write('    # Basis set & pseudopotentials\n')
        inp_n.write('    BASIS_SET_FILE_NAME BASIS_MOLOPT\n')
        inp_n.write('    POTENTIAL_FILE_NAME POTENTIAL\n')
        inp_n.write('    # Charge\n')
        inp_n.write('    CHARGE 0\n')
        inp_n.write('    # Realspace multi-grids\n')
        inp_n.write('    &MGRID\n')
        inp_n.write('      CUTOFF 500.0\n')
        inp_n.write('      REL_CUTOFF 70.0\n')
        inp_n.write('    &END MGRID\n')
        inp_n.write('    # Quickstep solver setting\n')
        inp_n.write('    &QS\n')
        inp_n.write('      EPS_DEFAULT 1.0e-10\n')
        inp_n.write('      EXTRAPOLATION use_guess\n')
        inp_n.write('      EXTRAPOLATION_ORDER 3\n')
        inp_n.write('    &END QS\n')
        inp_n.write('    # SCF procedure\n')
        inp_n.write('    &SCF\n')
        inp_n.write('      MAX_SCF 1\n')
        inp_n.write('      SCF_GUESS restart\n')
        inp_n.write('      ADDED_MOS 957\n')
        inp_n.write('      EPS_SCF 1.0e-6\n')
        inp_n.write('      MAX_DIIS 5\n')
        inp_n.write('      CHOLESKY inverse\n')
        inp_n.write('      &OT off\n')
        inp_n.write('      &DIAGONALIZATION on\n')
        inp_n.write('        ALGORITHM standard\n')
        inp_n.write('        EPS_ITER 1.0e-8\n')
        inp_n.write('        MAX_ITER 50\n')
        inp_n.write('      &END DIAGONALIZATION\n')
        inp_n.write('      &MIXING on\n')
        inp_n.write('        METHOD broyden_mixing\n')
        inp_n.write('        ALPHA 0.20\n')
        inp_n.write('        NBUFFER 8\n')
        inp_n.write('      &END MIXING\n')
        inp_n.write('      &SMEAR on\n')
        inp_n.write('        METHOD fermi_dirac\n')
        inp_n.write('        ELECTRONIC_TEMPERATURE 298.15\n')
        inp_n.write('      &END SMEAR\n')
        inp_n.write('      &PRINT\n')
        inp_n.write('        &RESTART off\n')
        inp_n.write('        &END\n')
        inp_n.write('      &END\n')
        inp_n.write('    &END SCF\n')
        inp_n.write('    # Exchange-correlation functional\n')
        inp_n.write('    &XC\n')
        inp_n.write('      &XC_FUNCTIONAL pbe\n')
        inp_n.write('      &END XC_FUNCTIONAL\n')
        inp_n.write('    &END XC\n')
        inp_n.write('    # Poisson solver\n')
        inp_n.write('    &POISSON\n')
        inp_n.write('      POISSON_SOLVER analytic\n')
        inp_n.write('      PERIODIC xy\n')
        inp_n.write('    &END POISSON\n')
        inp_n.write('  &END DFT\n')

def write_input_e_coupling(inp_name,block_n,name_a,ndx_a,first_a,last_a,electr,atoms):
    with open(inp_name+'.inp', 'a') as inp_n:
        inp_n.write('  # Electronic coupling\n')
        inp_n.write('  &PROPERTIES\n')
        inp_n.write('    &ET_COUPLING\n')
        inp_n.write('      # POD method\n')
        inp_n.write('      &PROJECTION\n')
        for i in range(block_n):
            if name_a[i]=='AU':
                'For Gold surface'
                inp_n.write('        # Block #%i -- %i%s - 1\n'%(i+1,ndx_a[i],name_a[i]))
                inp_n.write('        &BLOCK\n')
                inp_n.write('          ATOMS %i...%i\n'% (first_a[i],((atoms[i]/2)+first_a[i]-1)))
                inp_n.write('          NELECTRON %i\n'% (electr[i]/2))
                inp_n.write('        &END BLOCK\n')
                inp_n.write('        # Block #%i -- %i%s - 2\n'%(i+1,ndx_a[i],name_a[i]))
                inp_n.write('        &BLOCK\n')
                inp_n.write('          ATOMS %i...%i\n'% (((atoms[i]/2)+first_a[i]),last_a[i]))
                inp_n.write('          NELECTRON %i\n'% (electr[i]/2))
                inp_n.write('        &END BLOCK\n')
            elif name_a[i]=='CUR':
                'For redox site'
                inp_n.write('        # Block #%i -- %i%s\n'%(i+1,ndx_a[i],name_a[i]))
                inp_n.write('        &BLOCK\n')
                inp_n.write('          ATOMS %i\n'% (first_a[i]))
                inp_n.write('          NELECTRON %i\n'% (electr[i]))
                inp_n.write('        &END BLOCK\n')
            else:
                'For amino acids'
                inp_n.write('        # Block #%i -- %i%s\n'%(i+1,ndx_a[i],name_a[i]))
                inp_n.write('        &BLOCK\n')
                inp_n.write('          ATOMS %i...%i\n'% (first_a[i],last_a[i]))
                inp_n.write('          NELECTRON %i\n'% (electr[i]))
                inp_n.write('        &END BLOCK\n')
        inp_n.write('        # Read data from files\n')
        inp_n.write('        RESTART off\n')
        inp_n.write('        # Output\n')
        inp_n.write('        &PRINT\n')
        inp_n.write('          &HAMILTONIAN on\n')
        inp_n.write('          &END HAMILTONIAN\n')
        inp_n.write('          &WAVEFUNCTION on\n')
        inp_n.write('          &END WAVEFUNCTION\n')
        inp_n.write('          &TRANSF_MATRIX_F on\n')
        inp_n.write('          &END TRANSF_MATRIX_F\n')
        inp_n.write('          &TRANSF_MATRIX_R on\n')
        inp_n.write('          &END TRANSF_MATRIX_R\n')
        inp_n.write('          &COUPLING_ELEMENTS on\n')
        inp_n.write('          &END COUPLING_ELEMENTS\n')
        inp_n.write('        &END PRINT\n')
        inp_n.write('      &END PROJECTION\n')
        inp_n.write('    &END ET_COUPLING\n')
        inp_n.write('  &END PROPERTIES\n')

def write_input_system(inp_name):
    with open(inp_name+'.inp', 'a') as inp_n:
        inp_n.write('  # System description\n')
        inp_n.write('  &SUBSYS\n')
        inp_n.write('    # Cell vectors [A]\n')
        inp_n.write('    &CELL\n')
        inp_n.write('      ABC 49.810000 50.749088 49.954000\n')
        inp_n.write('      PERIODIC xy\n')
        inp_n.write('    &END CELL\n')
        inp_n.write('    # Coordinates [A]\n')
        inp_n.write('    &TOPOLOGY\n')
        inp_n.write('      COORD_FILE_FORMAT xyz\n')
        inp_n.write('      COORD_FILE_name au-azu-junction.xyz\n')
        inp_n.write('      CONN_FILE_FORMAT off\n')
        inp_n.write('    &END TOPOLOGY\n')
        inp_n.write('    # Atomic types\n')
        inp_n.write('    &KIND H\n')
        inp_n.write('      BASIS_SET DZVP-MOLOPT-SR-GTH-q1\n')
        inp_n.write('      POTENTIAL GTH-PBE\n')
        inp_n.write('    &END KIND\n')
        inp_n.write('    &KIND C\n')
        inp_n.write('      BASIS_SET DZVP-MOLOPT-SR-GTH-q4\n')
        inp_n.write('      POTENTIAL GTH-PBE\n')
        inp_n.write('    &END KIND\n')
        inp_n.write('    &KIND N\n')
        inp_n.write('      BASIS_SET DZVP-MOLOPT-SR-GTH-q5\n')
        inp_n.write('      POTENTIAL GTH-PBE\n')
        inp_n.write('    &END KIND\n')
        inp_n.write('    &KIND O\n')
        inp_n.write('      BASIS_SET DZVP-MOLOPT-SR-GTH-q6\n')
        inp_n.write('      POTENTIAL GTH-PBE\n')
        inp_n.write('    &END KIND\n')
        inp_n.write('    &KIND S\n')
        inp_n.write('      BASIS_SET DZVP-MOLOPT-SR-GTH-q6\n')
        inp_n.write('      POTENTIAL GTH-PBE\n')
        inp_n.write('    &END KIND\n')
        inp_n.write('    &KIND Fe\n')
        inp_n.write('      BASIS_SET DZVP-MOLOPT-SR-GTH-q16\n')
        inp_n.write('      POTENTIAL GTH-PBE\n')
        inp_n.write('    &END KIND\n')
        inp_n.write('    &KIND Cu\n')
        inp_n.write('      BASIS_SET DZVP-MOLOPT-SR-GTH-q11\n')
        inp_n.write('      POTENTIAL GTH-PBE\n')
        inp_n.write('    &END KIND\n')
        inp_n.write('    &KIND Au\n')
        inp_n.write('      BASIS_SET DZVP-MOLOPT-SR-GTH-q11\n')
        inp_n.write('      POTENTIAL GTH-PBE\n')
        inp_n.write('    &END KIND\n')
        inp_n.write('  &END SUBSYS\n')
        inp_n.write('&END FORCE_EVAL\n')
###############################################################################
###############################################################################
#Main function
def main():
    if len(sys.argv)!=3:
        print('usage: python create-cp2k-input.py filename.gro inputname')
        sys.exit(1)
    else:
        'Collect data'
        coord, cp2k_inp = sys.argv[1], sys.argv[2]
        'Organize data'
        aa_name,aa_ndx,atom_name,atom_ndx = collect_aa(coord)
        aa_f,aa_l,aa_resn,aa_resi = define_blocks(aa_name,aa_ndx,atom_ndx)
        atoms = define_atoms(atom_name)
        electrons = define_electrons(aa_f,aa_l,atoms)
        n_acids = len(electrons)
        '''Sanity check(s) if needed'''
        'Write data'
        write_input_global(cp2k_inp)
        write_input_dft_qs_scf_xc(cp2k_inp)
        write_input_e_coupling(cp2k_inp,n_acids,aa_resn,aa_resi,
                               aa_f,aa_l,electrons,atom_ndx)
        write_input_system(cp2k_inp)

#------------------------------------------------------------------------------
if __name__=='__main__':
    main()
###############################################################################
