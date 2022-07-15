#!/bin/bash
# This bash script supervises distant changes of structures in VASP optimization.
touch p1 p2;
touch dist.conv
Num=`awk 'NR==7{for(i=1;i<=NF;i++) a=$i+a;}END{print a}' XDATCAR`
Lnum=`wc XDATCAR|awk '{print $1}'`
((n=(Lnum-7)/(Num+1)))
head -7 XDATCAR >p1
awk -v num="$Num" 'NR==9,NR==(num+1)+7{print $0}' XDATCAR >>p1
for((i=1;i<n;i++))
do
cat p1 >p2
head -7 XDATCAR >p1
((n1=9+(Num+1)*i))
((n2=(i+1)*(Num+1)+7))
sed -n ''$n1','$n2'p' XDATCAR >>p1
echo -e $i"\t"`dist.pl p1 p2 ` >>dist.conv
done
# plot
gnuplot <<EOF
set grid
set term post
set output 'b.ps'
set xlabel 'Ion steps'
set title 'Distance between each ion steps'
unset key
set ylabel 'dist(Angst)'
plot 'dist.conv' u 1:2 w l lw 2 lc rgb "blue"
EOF
gs -sDEVICE=jpeg -r300 -sPAPERSIZE=a4 -dBATCH -dNOPAUSE -sOutputFile=dist.jpg b.ps
convert -rotate 90 dist.jpg dist.jpg
mogrify -trim dist.jpg
gnuplot <<EOF
set term dumb
plot 'dist.conv' w l t "Dist "
EOF
rm b.ps p1 p2 dist.conv

