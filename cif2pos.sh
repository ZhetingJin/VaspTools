#!/bin/sh
input=$1
format=$2
if test -z $2; then
format="ms"
fi

awk 'BEGIN{OFS="\t\t"}{if(NR==1) {print $0;print "1"}
if($1=="_cell_length_a") print $2,"0","0";
if($1=="_cell_length_b") print "0",$2,"0";
if($1=="_cell_length_c") print "0","0",$2;}' $input >POSCAR-cif

awk 'BEGIN{ORS=""}/_atom_site_occupancy/,/loop_/{
if($2~/^[A-Z]+/) {
if(a[i]!=$2) a[++i]=$2
++b[i]}
}END{
for(j=1;j<=i;j++) print a[j],"\t";
print "\n"
for(j=1;j<=i;j++) print b[j],"\t";
print "\n"
}' $input >>POSCAR-cif

echo "Direct" >>POSCAR-cif

awk -v format="$format" 'BEGIN{OFS="\t\t"}/_atom_site_fract_z/,/loop_/{
if($2~/^[A-Z]+/) {
if(format=="vtst") print $4,$5,$6
else if(format=="ms") print $3,$4,$5}
}' $input >>POSCAR-cif
