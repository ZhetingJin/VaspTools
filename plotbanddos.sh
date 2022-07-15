cd dos
echo -e "114\n63\n1 5-9\n2" |vaspkit
cp PDOS_* ../band/
cd ../band/
echo -e "214\n63\n2\n1 5-9" |vaspkit
for i in UP DW
do cp PBAND_PDOS_SUM_${i}.jpg Fe_${i}.jpg
done

cd ../dos
echo -e "114\n13-14 17-20\n5-9\n2" |vaspkit
cp PDOS_* ../band/
cd ../band/
echo -e "214\n13-14 17-20\n2\n5-9" |vaspkit
for i in UP DW
do cp PBAND_PDOS_SUM_${i}.jpg Cubulk_${i}.jpg
done

cd ../dos
echo -e "114\n15-16\n5-9\n2" |vaspkit
cp PDOS_* ../band/
cd ../band/
echo -e "214\n15-16\n2\n5-9" |vaspkit
for i in UP DW
do cp PBAND_PDOS_SUM_${i}.jpg Cusur_${i}.jpg
done

cd ../dos
echo -e "114\n13-14 17-20\n9\n2" |vaspkit
cp PDOS_* ../band/
cd ../band/
echo -e "214\n13-14 17-20\n2\n9" |vaspkit
for i in UP DW
do cp PBAND_PDOS_SUM_${i}.jpg Cubulk_x2y2_${i}.jpg
done

cd ../dos
echo -e "114\n15-16\n9\n2" |vaspkit
cp PDOS_* ../band/
cd ../band/
echo -e "214\n15-16\n2\n9" |vaspkit
for i in UP DW
do cp PBAND_PDOS_SUM_${i}.jpg Cusur_x2y2_${i}.jpg
done

sed -i "s/#x_limits/x_limits/g" PLOT.in

cd ../dos
echo -e "114\n21\n2-4\n2" |vaspkit
cp PDOS_* ../band/
cd ../band/
echo -e "214\n21\n2\n2-4" |vaspkit
for i in UP DW
do cp PBAND_PDOS_SUM_${i}.jpg Bireplaced_${i}.jpg
done

cd ../dos
echo -e "114\n22\n2-4\n2" |vaspkit
cp PDOS_* ../band/
cd ../band/
echo -e "214\n22\n2\n2-4" |vaspkit
for i in UP DW
do cp PBAND_PDOS_SUM_${i}.jpg Bisur_${i}.jpg
done

cd ../dos
echo -e "114\n35\n2-4\n2" |vaspkit
cp PDOS_* ../band/
cd ../band/
echo -e "214\n35\n2\n2-4" |vaspkit
for i in UP DW
do cp PBAND_PDOS_SUM_${i}.jpg O_bond_BiO_${i}.jpg
done

cd ../dos
echo -e "114\n36\n2-4\n2" |vaspkit
cp PDOS_* ../band/
cd ../band/
echo -e "214\n36\n2\n2-4" |vaspkit
for i in UP DW
do cp PBAND_PDOS_SUM_${i}.jpg O_unbond_BiO_${i}.jpg
done

cd ../dos
echo -e "114\n37\n2-4\n2" |vaspkit
cp PDOS_* ../band/
cd ../band/
echo -e "214\n37\n2\n2-4" |vaspkit
for i in UP DW
do cp PBAND_PDOS_SUM_${i}.jpg O_bond_SrO_${i}.jpg
done

cd ../dos
echo -e "114\n62\n2-4\n2" |vaspkit
cp PDOS_* ../band/
cd ../band/
echo -e "214\n62\n2\n2-4" |vaspkit
for i in UP DW
do cp PBAND_PDOS_SUM_${i}.jpg O_added_${i}.jpg
done
