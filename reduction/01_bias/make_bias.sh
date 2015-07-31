export OMP_NUM_THREADS=4
echo "Setting max number of usable threads to" $OMP_NUM_THREADS 
esorex --log-file=bias.log muse_bias --nifu=-1 --merge bias.sof
