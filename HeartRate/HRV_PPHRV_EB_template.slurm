#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=15G
#SBATCH --job-name=replaceSUB_replaceRUN_HRV_PPHRV_EB_runwise_cluster


cd $SLURM_SUBMIT_DIR
cd /zwork/jingyi/EB/EBpsychopyz_NegNeu/HRV/HRV_PPHRV_EB

export PATH=${PATH}:/sw/matlab_2018a/bin

matlab -nodisplay -nosplash -r "replaceSUB_replaceRUN_HRV_PPHRV_EB_runwise_cluster"
