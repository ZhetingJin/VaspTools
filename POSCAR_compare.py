#! /usr/bin/env python
# 03/15/2022 Zheting

import subprocess as sub
import sys
import numpy as np

#
# compare two poscar structure from vasp calculation and print 
# out the largest displacement among all atoms
#

try:
  fn_pos = [sys.argv[1], sys.argv[2]]

except:
  print('Usage: ',sys.argv[0],' poscar_file1, poscar_file2')
  print('       POSCAR: a vasp file containing atomic position')
  print('       The input POSCAR MUST be in direct coordinates')
  print('       Output: the largest displacement among all atoms')
  sys.exit(1)

# read files
lines = []
for ifile in range(2):
    fin = open(fn_pos[ifile],'r')
    lines.append(fin.readlines())
    fin.close()

# read lines
atominfo = []
for ifile in range(2):
    nline = 0
    lattice = np.zeros([3,3])
    atomlist = []
    for line in lines[ifile]:
      if ("." in line):
        # get atom number
        if nline > 0 and nline <= 3:
          for i in range(3):
            try:
              lattice[nline - 1, i] = float(line.split()[i].strip())
            except:
              print('problem with line', line)
              print('line.split result is ', line.split())
              sys.exit(1)
        if nline > 3:
          atomic_v = np.zeros(3)
          for i in range(3):
            atomic_v[i] = np.array(float(line.split()[i].strip()))
#           atomic_v = np.dot(atomic_v, lattice)
          atomlist.append(atomic_v)
        nline += 1
    
    # finish reading one file, save stuffs
    atominfo.append(atomlist)

def min_array_elementwise(nparray_a, nparray_b):
    ind = nparray_a > nparray_b
    nparray_a[ind] = nparray_b[ind]
    return nparray_a

# Compute difference
diff = [
    max(min_array_elementwise(
        abs(atominfo[0][i]-atominfo[1][i]),
        abs(abs(atominfo[0][i]-atominfo[1][i])-1))
           ) for i in range(len(atominfo[0]))
    ]
maxdiff = max(diff)
print('The maximum difference of atomic position in direct coordinates is ',maxdiff)
maxindex = diff.index(maxdiff)
print('The index of maximum different is ', maxindex+1, '(index starts from 1)')
print('The former atomic position is ', atominfo[0][maxindex])
print('The latter atomic position is ', atominfo[1][maxindex])

