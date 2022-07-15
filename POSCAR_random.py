#! /usr/bin/env python
# 06/28/2022 Zheting
from pymatgen.core import Lattice, Structure, Molecule
import random
import sys
import numpy as np

# Read a POSCAR and write to a CIF.
structure = Structure.from_file("/home/zheting/data/vasp/supercell/addFe_lowsym/addFeO/random/1/POSCAR")
# structure.to(filename="CsCl.cif")

# Read an xyz file and write to a Gaussian Input file.
# methane = Molecule.from_file("methane.xyz")
# methane.to(filename="methane.gjf")
# print(structure)

# Get the distance between position1 and position2 in Cartesian coordinates
# Usage: 
# position1 and position2 are 3d-vector indicating two positions, either in fractional or Cartesian coordinates
# When using fractional coordinates, cubic lattice is ASSUMED: lattice = [a, b, c]
# When using Cartesian coordinates, lattice = [1, 1, 1] or "Cartesian", only the first letter matters
def get_bond_length(position1, position2, lattice):
    if lattice[0]=="C" or lattice[0]=="c":
        lattice = np.array([1,1,1])
    else:
        lattice = np.array(lattice)
    position1 = np.array(position1)
    position2 = np.array(position2)
    # get the difference
    diff = abs(position1 - position2)
    # consider the periodic boundary condition
    diff = np.minimum(diff, 1.0 - diff)
    # get the difference in Cartesian
    diff = diff * lattice
    # get the bond length
    bond = np.linalg.norm(diff)**2
    return bond

# Randomly generate an atomic position
# Usage:
# pos_range is the position range like [[xmin, xmax], [ymin, ymax], ...]
def gen_random_atom(pos_range):
    pos_atom = []
    for axis_range in pos_range:
        pos_atom.append(random.uniform(axis_range[0], axis_range[1]))
    return pos_atom

# Determine if we can accept the new atomic position (too close to other atoms?)
# Usage: 
# new_atom and old_atoms are 3d-vector(s) for new atomic position and old atomic positions
# When using fractional coordinates, cubic lattice is ASSUMED: lattice = [a, b, c]
# When using Cartesian coordinates, lattice = [1, 1, 1] or "Cartesian", only the first letter matters
# tol is the smallest tolerance distance between two atoms in Cartesian coordinates
def atom_isgood(new_atom, old_atoms, lattice, tol):
    isgood = True
    for iatom in old_atoms:
        ibond = get_bond_length(new_atom, iatom, lattice)
        isgood = isgood and (ibond > tol)
    return isgood

# atoms_label starts from 0!!!!
atoms_label = [24, 25, 50, 51, 60, 61]
atoms_element = ["Bi", "Bi", "O", "O", "O", "Fe"]
num_atoms = len(atoms_label)
lattice = [5.454364, 5.455064, 46.876252]
pos_range = [[0, 1], [0, 1], [0.62, 0.7]]
old_atoms = []
tol = 0.8
num_structures = 30

# Generate several atoms randomly in a given range. The distance between two atoms are larger than a smallest tolerance
# label of the structure
istruct = sys.argv[1]
count = 0
while len(old_atoms) < num_atoms:
    pos_atom = []
    for axis_range in pos_range:
        pos_atom.append(random.uniform(axis_range[0], axis_range[1]))
    if atom_isgood(pos_atom, old_atoms, lattice, tol):
        old_atoms.append(pos_atom)
    if count > 100:
        print("Impossible to find good atom position")
        break

# Insert the generated atoms in the structure
new_struct = structure
for iat in range(num_atoms):
    atom_label = atoms_label[iat]
    new_struct[atom_label] = atoms_element[iat], old_atoms[iat]

# save structure
namestruct = "/home/zheting/data/vasp/supercell/addFe_lowsym/addFeO/random/random_struct/POSCAR_" + istruct
new_struct.to(filename=namestruct)
