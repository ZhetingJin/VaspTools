import math
import numpy as np
# from vaspwfc import vaspwfc, save2vesta
from unfold import make_kpath, removeDuplicateKpoints, find_K_from_k, save2VaspKPOINTS

# Create the supercell from the primitive cell
# The tranformation matrix between supercell and primitive cell.
s2 = 1/math.sqrt(2)
M = [[s2, s2, 0.0],
    [-s2, s2, 0.0],
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
kpath = make_kpath(kpts, nseg=10)
K_in_sup = []
for kk in kpath:
    kg, g = find_K_from_k(kk, M)
    K_in_sup.append(kg)
# remove the duplicate K-points
reducedK, kid = removeDuplicateKpoints(K_in_sup, return_map=True)
# Do not remove the duplicate K-points
# reducedK = np.asarray(K_in_sup)

# save to VASP KPOINTS
save2VaspKPOINTS(reducedK)