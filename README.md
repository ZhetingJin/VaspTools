# VaspTools
A set of useful scripts for vasp calculations.

Most of the scripts are based on python or bash. 

Possible dependency packages/softwares used:

1. pymatgen (https://pymatgen.org/index.html)

2. vaspkit (https://vaspkit.com/index.html)

3. VaspBandUnfolding (https://github.com/QijingZheng/VaspBandUnfolding)

The following are the usage and descriptions of the scripts:
## POSCAR_Supercell.ipynb
A jupyter notebook to generate supercell structure from a given primitive cell structure. 

## POSCAR_compare.py
Compare two vasp crystal structure and print out the largest displacement among all atoms. 

Usage:  POSCAR_compare.py  [poscar_file1]  [poscar_file2]

where POSCAR is a vasp file containing atomic position

Output: the largest displacement among all atoms

Note: The input POSCAR MUST be in direct coordinates

## POSCAR_direct2cartesian.py
Convert POSCAR from direct coordinates to cartesian coordinates.

Usage:  POSCAR_direct2cartesian.py  [poscar_file]

and then replace the "direct" flag (could be any strings beginning with "D" or "d") to "cartesian" flag (could be any strings beginning with "C" or "c") in the outputs

Note: Naively assuming that there is no "." symbol in the description line(s) on the top of POSCAR files

## POSCAR_interpolation.ipynb
A jupyter notebook to generate interpolation structures between two given structures. 

## POSCAR_random.py
Move the atoms in a given range randomly and output the new POSCAR files. Simple constraint applied: the distance between two atom cores are forced to be larger than a smallest tolerance

Note: Read the script to modify necessary input information.

## band.ipynb
A jupyter notebook to plot projected band structure and corresponding density of states (example plots are included).

## band.py
Use the band.dat to plot band structure with the output file band.jpg

## band.sh
Extracts data of band structure from OUTCAR file, and write the output file band.dat 

## fix_atom.sh
Set fixed atoms in the structure relaxation

## makeslab.sh
Add vacuum to z=0 in POSCAR to generate a structure for slab calculations

## plotbanddos.sh
Automatically generate combined figures of specified projected band structures and density of states.  

## postprocess.sh
Prepare input files for bandstructure, density of states, fermi surface after SCF calculations

## pull_materialproject.py
Pull structure file from material project

## run.slurm
An example slurm script to submit jobs to compute nodes. 

Usage: sbatch run.slurm

## scancel_all.sh
Cancel slurm jobs by specified keywords.

## siesta2POSCAR.sh
Convert siesta output structure (case.STRUCT_OUT) to vasp structure (POSCAR).

## unfolding.py
Unfolding band structure calculations and plottings. 

Usage: 

1. Do a regular SCF calculation

2. Prepare the files for regular band structure calculation. Make sure there is no KPOINTS and WAVECAR in the working directory. Make sure LWAVE = TRUE in INCAR.

3. Define necessary inputs in the script to generate KPOINTS by "python unfolding.py"

4. Run the NSCF calculation with the generated KPOINTS and get WAVECAR

5. Run "python unfolding.py" to plot the unfolding band structure. 

5. Plot 
