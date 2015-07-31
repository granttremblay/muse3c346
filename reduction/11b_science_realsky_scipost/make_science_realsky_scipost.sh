export OMP_NUM_THREADS=3
echo "Setting max number of usable threads to" $OMP_NUM_THREADS 
esorex --log-file=science_modelsky_scipost.log muse_scipost --filter=white,Johnson_V,Cousins_R,Cousins_I science_modelsky_scipost.sof
