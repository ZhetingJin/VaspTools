from pymatgen.ext.matproj import MPRester
with MPRester("qxqEJ3whMC5s9RYzqpcvLaMX0p3GjKCM") as mpr:
    struct = mpr.get_structure_by_material_id("mp-22862")
    struct.to(fmt='poscar', filename='POSCAR')
