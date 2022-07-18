import os
import numpy as np
import math
from procar import procar
from unfold import unfold, EBS_scatter
from unfold import make_kpath, removeDuplicateKpoints, find_K_from_k, save2VaspKPOINTS

# Create the supercell from the primitive cell
# The tranformation matrix between supercell and primitive cell.
s2 = math.sqrt(2)
M = [[1.0, 1.0, 0.0],
    [-1.0, 1.0, 0.0],
    [0.0, 0.0, 1.0]]

npM = np.array(M)

# Generate band path in the primitive Brillouin Zone (PBZ) and find the correspondig K points of the supercell BZ (SBZ) onto which they fold.
# high-symmetry point in fractional coordinate
kpts = [[0.0, 0.0, 0.0],            # G
        [0.25, 0.25, 0.0],          # Mp
        [0.5, 0.5, 0.0],            # X
        [0.5, 0.0, 0.0],            # M
        [0.0, 0.0, 0.0]]            # G
# create band path from the high-symmetry points, 30 points inbetween each pair
# high-symmetry points
num_kpoints = 10
kpath = make_kpath(kpts, nseg=num_kpoints)
K_in_sup = []
for kk in kpath:
    kg, g = find_K_from_k(kk, M)
    K_in_sup.append(kg)
# remove the duplicate K-points
reducedK, kmap = removeDuplicateKpoints(K_in_sup, return_map=True)
# Do not remove the duplicate K-points
# reducedK = np.asarray(K_in_sup)

# save to VASP KPOINTS
if not os.path.isfile('KPOINTS'):
    # save to VASP KPOINTS
    save2VaspKPOINTS(reducedK)

# basis vector of the supercell
scell = [[-3.8562711460158638,   -3.8573601627428253,    0.0053588657782055],
         [-3.8566498147294728,    3.8579689844973197,   -0.0072523241795060],
         [-0.0054515730511260,    0.0438727579184608,  -46.8762315333175579]]

# basis vector of the primitive cell
cell = np.matmul(scell,np.linalg.inv(npM))
# print(cell)

# cell = [[ 3.1850, 0.0000000000000000,  0.0],
#         [-1.5925, 2.7582909110534373,  0.0],
#         [ 0.0000, 0.0000000000000000, 35.0]]

# WaveSuper = unfold(M=M, wavecar='WAVECAR')

# sw = WaveSuper.spectral_weight(kpath)
# # show the effective band structure with scatter
# EBS_scatter(kpath, cell, sw, nseg=num_kpoints, eref=-4.01,
#         ylim=(-6, 3), 
#         factor=5)

# e0, sf = WaveSuper.spectral_function(nedos=4000)
# # or show the effective band structure with colormap
# EBS_cmaps(kpath, cell, e0, sf, nseg=num_kpoints, eref=-4.01,
#         show=False,
#         ylim=(-6, 3))

if os.path.isfile('WAVECAR'):
    if os.path.isfile('awht.npy'):
        atomic_whts = np.load('awht.npy')
    else:
        p           = procar()
        # The atomic contribution to each KS states
        atomic_whts = [p.get_pw(atoms="12:20", spd=8)[:,kmap,:], p.get_pw(atoms="12:20", spd=[5,7])[:,kmap,:], p.get_pw(atoms="12:20", spd=[4,6])[:,kmap,:]]
        np.save('awht.npy', atomic_whts)

    if os.path.isfile('sw.npy'):
        sw = np.load('sw.npy')
    else:
        WaveSuper   = unfold(M=M, wavecar='WAVECAR')
        sw = WaveSuper.spectral_weight(kpath)
        np.save('sw.npy', sw)

    EBS_scatter(kpath, cell, sw,
                atomic_whts,
                atomic_colors=['blue', "red", 'green'],
                nseg=num_kpoints, eref=2.0360,
                ylim=(-6, 3), 
                kpath_label = ['G', 'Mp', "X", "M/Xp", "G"],
                factor=20,
                save='ebs_s.png')
    ax.legend(['', 'Second line'])
