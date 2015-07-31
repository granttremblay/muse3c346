export OMP_NUM_THREADS=6
echo "Setting max number of usable threads to" $OMP_NUM_THREADS 
esorex --log-file=wavecal.log muse_wavecal --nifu=-1 --resample --residuals --merge wavecal.sof
