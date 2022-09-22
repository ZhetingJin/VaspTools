echo -e "403\nall\n1\n0 0 0.5" |vaspkit
python3 ~/project/vasp/VaspTools/POSCAR_direct2cartesian.py POSCAR_REV > POSCAR_cart
sed -i "s/Direct/Selective \nCart/g" POSCAR_cart
cp POSCAR_cart POSCAR
~/project/vasp/VaspTools/fix_atom.sh

