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
shift = np.array([0.6, -0.25, -1, -0.25, 0.6, 1, 0.25, -0.6, -0.6, 0.25])*0.02
for line in lines:
  if ("." in line):
    # get atom number
    if nline <= 3:
      print(line, end = '')
    if nline > 3:
      atomic_v = np.zeros(3)
      for i in range(3):
        atomic_v[i] = np.array(float(line.split()[i].strip()))
      
      nshift = shift[(nline % 5) - 4]
      if atomic_v[2] > 0.5:
        atomic_v[2] += nshift
      else:
        atomic_v[2] -= nshift

      print('%5.6f %5.6f %5.6f ' % (atomic_v[0], atomic_v[1], atomic_v[2]), end = ' ')
      try:
        otherstaff = line.split()[3].strip()
        print(otherstaff)
      except:
        print(' ')
    nline += 1
  else:
    print(line, end = '')
