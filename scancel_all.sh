squeue --me |grep 200 |awk '{print $1}' |xargs scancel
