export OMP_NUM_THREADS=6
echo "Setting max number of usable threads to" $OMP_NUM_THREADS 
esorex --log-file=flat.log muse_flat --nifu=-1 --merge flat.sof
