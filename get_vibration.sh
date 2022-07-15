#!/bin/sh
# This bash script extract vibration info from OUTCAR, which can be further used by jmol/ovito for visualization.

a1=`awk '{if(NR==3) print $1}' POSCAR`
a2=`awk '{if(NR==3) print $2}' POSCAR`
a3=`awk '{if(NR==3) print $3}' POSCAR`
b1=`awk '{if(NR==4) print $1}' POSCAR`
b2=`awk '{if(NR==4) print $2}' POSCAR`
b3=`awk '{if(NR==4) print $3}' POSCAR`
c1=`awk '{if(NR==5) print $1}' POSCAR`
c2=`awk '{if(NR==5) print $2}' POSCAR`
c3=`awk '{if(NR==5) print $3}' POSCAR`

pos2xyz.pl POSCAR

num_atom=`awk 'NR==1{print $1}' POSCAR.xyz`
n=`grep PiTHz OUTCAR |wc -l`
awk '/PiTHz/,/POTIM/{print $4"   "$5"   "$6}' OUTCAR> tmp
awk 'BEGIN{RS="\n      \n"}{a++}{print >"tmp_"a}' tmp
grep PiTHz OUTCAR |awk '{print $1,$2,$3,$4,$5}' >tmp2
awk 'BEGIN{RS="\n"}{a++}{print >"tmp2_"a}' tmp2

if [ -f "all_vib.xyz" ] ;  then
   rm all_vib.xyz
fi

for i in `seq 1 $n`
do
        freq=`cat tmp2_$i`
        sed -i "1,2s/.*/ /" tmp_$i
        paste -d "   " POSCAR.xyz tmp_$i >vib_$i.xyz

        awk   -v a1=$a1 -v a2=$a2 -v a3=$a3 -v b1=$b1 -v b2=$b2 -v b3=$b3 -v c1=$c1 -v c2=$c2 -v c3=$c3 -v name="$freq"  '{
        if(NR==2)
        printf("Lattice=\"%f %f %f %f %f %f %f %f %f\" Properties=species:S:1:pos:R:3:forces:R:3 pbc=\"T T T\" # %s \n",a1,a2,a3,b1,b2,b3,c1,c2,c3,name);
        else print}' vib_$i.xyz >temp
        mv temp vib_$i.xyz
        cat vib_$i.xyz >> all_vib.xyz
done
rm tmp*
mkdir vib_i
mv vib_*.xyz vib_i
