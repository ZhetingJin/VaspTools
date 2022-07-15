#!/bin/sh
# eliminate forces of fixed atoms
#lipai@mail.ustc.edu.cn
fix=$1
if test -z $1; then
fix=0
fi
# get data form OUTCAR
awk -v fix="$fix" '/POSITION/,/drift/{
if($1~/^[0-9.]+$/&&$3>=fix) print $1,$2,$3,sqrt($4*$4+$5*$5+$6*$6i);
else if($1=="total") print $0
}' OUTCAR >temp.f
awk '{
if($1=="total") {print ++i,a;a=0}
else {if(a<$4) a=$4}
}' temp.f >force.conv
sed -i '1,9d' force.conv
rm temp.f
awk '/entropy=/{if(i<9) i++;else print ++i,$7}' OUTCAR >energy.conv
# plot
gnuplot <<EOF
set grid
set term post
set output 'b.ps'
set xlabel 'Ion steps'
set title 'Energy & Max Force of each ion steps'
set key box reverse spacing 3.0
set ytics nomirror
set y2tics
set ylabel 'Energy(eV)'
set y2label 'Max Force(eV/Angstrom)'
plot 'energy.conv' u 1:2 w l lw 3 lc rgb "red" axes x1y1 t "Energy ",'force.conv' u 1:2 w l lw 2 lc 3 axes x1y2 t "Max Force "
EOF
gs -sDEVICE=jpeg -r300 -sPAPERSIZE=a4 -dBATCH -dNOPAUSE -sOutputFile=conv.jpg b.ps
convert -rotate 90 conv.jpg conv.jpg
mogrify -trim conv.jpg
gnuplot <<EOF
set term dumb
plot 'energy.conv' w l t " Energy "
plot 'force.conv' w l t " Force "
EOF
rm b.ps # force.conv energy.conv
