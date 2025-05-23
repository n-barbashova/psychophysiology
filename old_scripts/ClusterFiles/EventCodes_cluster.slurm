#!/bin/bash -l
#SBATCH --nodes=1 --ntasks-per-node=1
#SBATCH --mem=1G
cd $SLURM_SUBMIT_DIR

date
hostname
source ~/anaconda3/etc/profile.d/conda.sh
conda activate python3.8

python /zwork/jingyi/EB/EBpsychopyz_NegNeu/scripts/EventCodes_cluster.py

date
hostname