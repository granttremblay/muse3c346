export OMP_NUM_THREADS=4
echo "Setting max number of usable threads to" $OMP_NUM_THREADS 
esorex --log-file=dark.log muse_dark --nifu=-1 --merge dark.sof
