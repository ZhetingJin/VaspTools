from pymatgen.io.vasp import Vasprun, BSVasprun
from pymatgen.electronic_structure.plotter import BSPlotter

v = BSVasprun("band/vasprun.xml")
bs = v.get_band_structure(kpoints_filename="band/KPOINTS",line_mode=True)
plt = BSPlotter(bs)
result = plt.get_plot(vbm_cbm_marker=True,ylim=(-5,9))
result.savefig('band.png')
