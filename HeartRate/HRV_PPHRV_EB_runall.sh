#!/bin/bash

subjects=('006' '007' '008')
runs="1 2 3 4 5 6"

for i in "${subjects[@]}";
do
for j in $runs
do

	sed "s/replaceSUB/${id}/g;s/replacerun/${j}/g" <HRV_PPHRV_EB_template.m >${i}_{j}_HRV_PPHRV_EB_runwise_cluster.m
	sed "s/replaceSUB/${id}/g;s/replacerun/${j}/g" <HRV_PPHRV_EB_template.slurm >${i}_{j}_HRV_PPHRV_EB_runwise_cluster.slurm
#     sbatch ${i}_{j}_HRV_PPHRV_EB_runwise_cluster.slurm
done
done
