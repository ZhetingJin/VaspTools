#!/bin/sh
# prepare input files for bandstructure, density of states, fermi surface
for i in band dos fs
do mkdir $i
cp * $i/
cp CONTCAR $i/POSCAR
sed -i "s/# ICHARG = 11/ICHARG = 11/g" $i/INCAR
sed -i "s/IBRION = 2/IBRION = -1/g" $i/INCAR
sed -i "s/NSW = 99/NSW = 0/g" $i/INCAR
sed -i "s/LWAVE = False/LWAVE = True/g" $i/INCAR
done

