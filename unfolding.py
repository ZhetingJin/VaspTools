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

def EBS_plotting(kpts, cell, spectral_weight,
                atomic_weights=None,
                atomic_colors=[],
                eref=0.0,
                nseg=None, save='ebs_s.png',
                kpath_label=[],
                factor=20, figsize=(3.0, 4.0),
                ylim=(-3, 3), show=True,
                color='b',legend=["Line1"]):
    '''
    plot the effective band structure with scatter, the size of the scatter
    indicates the spectral weight.
    The plotting function utilizes Matplotlib package.
    inputs:
        kpts: the kpoints vectors in fractional coordinates.
        cell: the primitive cell basis
        spectral_weight: self-explanatory
    '''

    import matplotlib as mpl
    mpl.use('agg')
    import matplotlib.pyplot as plt

    mpl.rcParams['axes.unicode_minus'] = False

    nspin = spectral_weight.shape[0]
    kpt_c = np.dot(kpts, np.linalg.inv(cell).T)
    kdist = np.r_[0, np.cumsum(
        np.linalg.norm(
            np.diff(kpt_c, axis=0),
            axis=1
        ))]
    nk = kdist.size
    nb = spectral_weight.shape[2]
    # x0 = np.outer(np.ones(nb), kdist).T
    x0 = np.tile(kdist, (nb, 1)).T

    if atomic_weights is not None:
        atomic_weights = np.asarray(atomic_weights)
        assert atomic_weights.shape[1:] == spectral_weight.shape[:-1]
        
        if not atomic_colors:
            atomic_colors = mpl.rcParams['axes.prop_cycle'].by_key()['color']

    fig = plt.figure()
    fig.set_size_inches(figsize)
    if nspin == 1:
        axes = [plt.subplot(111)]
        fig.set_size_inches(figsize)
    else:
        axes = [plt.subplot(121), plt.subplot(122)]
        fig.set_size_inches((figsize[0] * 2, figsize[1]))

    for ispin in range(nspin):
        ax = axes[ispin]
        if atomic_weights is not None:
            for iatom in range(atomic_weights.shape[0]):
                ax.scatter(x0, spectral_weight[ispin, :, :, 0] - eref,
                            s=spectral_weight[ispin, :, :, 1] * factor * atomic_weights[iatom][ispin,:,:],
                           lw=0.0, color=atomic_colors[iatom])
        else:
            ax.scatter(x0, spectral_weight[ispin, :, :, 0] - eref,
                       s=spectral_weight[ispin, :, :, 1] * factor,
                       lw=0.0, color=color)

        ax.set_xlim(0, kdist.max())
        ax.set_ylim(*ylim)
        ax.set_ylabel('Energy [eV]', labelpad=5)

        if nseg:
            for kb in kdist[::nseg]:
                ax.axvline(x=kb, lw=0.5, color='k', ls=':', alpha=0.8)

            if kpath_label:
                ax.set_xticks(kdist[::nseg])
                kname = [x.upper() for x in kpath_label]
                for ii in range(len(kname)):
                    if kname[ii] == 'G':
                        kname[ii] = r'$\mathrm{\mathsf{\Gamma}}$'
                    else:
                        kname[ii] = r'$\mathrm{\mathsf{%s}}$' % kname[ii]
                ax.set_xticklabels(kname)
                
        ax.legend(legend)

    plt.tight_layout(pad=0.2)
    plt.savefig(save, dpi=360)
    if show:
        plt.show()

if os.path.isfile('WAVECAR'):
    if os.path.isfile('awht.npy'):
        atomic_whts = np.load('awht.npy')
    else:
        p           = procar()
        # The atomic contribution to each KS states
        '''
        Get site/k-points/spd-orbital projected weight for each KS orbital.
        atoms : selected atoms index.
                Valid values:
                    ":"       -> for all atoms
                    "0::2"    -> for even index atoms
                    [0, 1, 2] -> atom indices specified by list
                    0         -> atom indices specified by integer
        kpts  : selected k-points index
                Valid values:
                    ":"       -> for all k-points
                    "0::2"    -> for even index k-points
                    [0, 1, 2] -> k-points indices specified by list
                    0         -> k-points indices specified by integer
        spd   : selected s/p/d-orbitals, the s/p/d-orbital and the corresponding
                index are:
                    's' : 0,
                    'py' : 1, 'pz' : 2, 'px' : 3,
                    'dxy' : 4, 'dyz' : 5, 'dz2' : 6, 'dxz' : 7, 'dx2' : 8
                Valid values:
                    ":"         -> for all s/p/d-orbitals
                    "0::2"      -> for even index
                    [0, 1, 2]   -> s/p/d-orbitals specified by list of integer
                    ['s', 'py'] -> s/p/d-orbitals specified by list of names
                    0           -> s/p/d-orbitals indices specified by integer
        '''
        atomic_whts = [p.get_pw(atoms="12:20", spd=8)[:,kmap,:], 
                       p.get_pw(atoms="12:20", spd=[5,7])[:,kmap,:], 
                       p.get_pw(atoms="12:20", spd=[4,6])[:,kmap,:]]
        np.save('awht.npy', atomic_whts)

    if os.path.isfile('sw.npy'):
        sw = np.load('sw.npy')
    else:
        WaveSuper   = unfold(M=M, wavecar='WAVECAR')
        sw = WaveSuper.spectral_weight(kpath)
        np.save('sw.npy', sw)

    EBS_plotting(kpath, cell, sw,
                atomic_whts,
                atomic_colors=['blue', "red", 'green'],
                nseg=num_kpoints, eref=2.0360,
                ylim=(-6, 3), 
                kpath_label = ['G', 'Mp', "X", "M/Xp", "G"],
                factor=20, show=False,
                save='ebs_s.png',
                legend=["dx2-y2", "dxz and dyz", "dxy and dz2"])
    
