f="1.txt"  # The file name of siesta output struct
sed -i "1i Sr32Ca16Cu32Bi32O132\n   1.0000000000000000" $f
sed -i "6d" $f
sed -i "6i    Sr   Ca   Cu   Bi   O\n    32    16    32    32   132\nDirect" $f
sed -i "s/  1    38/ /g" $f
sed -i "s/  2    20/ /g" $f
sed -i "s/  3    29/ /g" $f
sed -i "s/  4    83/ /g" $f
sed -i "s/  5     8/ /g" $f

