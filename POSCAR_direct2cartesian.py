#! /usr/bin/env python
# 02/07/2022 Zheting

import subprocess as sub
import sys
import numpy as np

#
# goes through POSCAR in vasp calculation and transform direct 
# coordinates to Cartesian coordinates
#

try:
  fn_pos=sys.argv[1]

except:
  print('Usage: ',sys.argv[0],' poscar')
  print('       POSCAR: a vasp file containing atomic position')
  sys.exit(1)

# read list of states to project on
state_list=[]
fin = open(fn_pos,'r')
lines = fin.readlines()
fin.close()
nline = 0
lattice = np.zeros([3,3])
for line in lines:
  if ("." in line):
    # get atom number
    if nline == 0:
      print(line, end = '')
    if nline > 0 and nline <= 3:
      print(line, end = '')
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
      atomic_v = np.dot(atomic_v, lattice)

      print('%5.6f %5.6f %5.6f ' % (atomic_v[0], atomic_v[1], atomic_v[2]), end = ' ')
      try:
        otherstaff = line.split()[3].strip()
        print(otherstaff)
      except:
        print(' ')
    nline += 1
  else:
    print(line, end = '')
