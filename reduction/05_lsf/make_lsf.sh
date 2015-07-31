export OMP_NUM_THREADS=6
echo "Setting max number of usable threads to" $OMP_NUM_THREADS 
esorex --log-file=lsf.log muse_lsf --nifu=-1 --merge lsf.sof
