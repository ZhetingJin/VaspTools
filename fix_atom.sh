#!/bin/sh
# usage: fix_atom.sh 0.3 It fixs atoms with z coordinate lower than 0.3
awk '{
      if ( NR > 9 )
      {
            if ( $3 > -25 )
                  printf("%10.7f %10.7f %10.7f %s %s %s\n",$1,$2,$3,"F","F","F")
            else
                  printf("%10.7f %10.7f %10.7f %s %s %s\n",$1,$2,$3,"T","T","T")
      }
      else
      print $0
}' POSCAR > POSCAR-new
