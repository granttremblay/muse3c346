export OMP_NUM_THREADS=6
echo "Setting max number of usable threads to" $OMP_NUM_THREADS 
esorex --log-file=twilight.log muse_twilight twilight.sof
