#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --job-name=batch_ledalab_command_cluster


cd $SLURM_SUBMIT_DIR
cd /zwork/jingyi/EB/EBpsychopyz_NegNeu/scripts

export PATH=${PATH}:/sw/matlab_2018a/bin

matlab -nodisplay -nosplash -r "batch_ledalab_command_cluster"
