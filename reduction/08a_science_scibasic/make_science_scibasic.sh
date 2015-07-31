export OMP_NUM_THREADS=6
echo "Setting max number of usable threads to" $OMP_NUM_THREADS 
esorex --log-file=science_scibasic.log muse_scibasic --nifu=-1 --merge science_scibasic.sof
