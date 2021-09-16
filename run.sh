#!/bin/bash
#SBATCH --job-name=3D-Postprocessing
#SBATCH --account=lyons-lab
#SBATCH --partition=standard
#SBATCH --ntasks=28
#SBATCH --ntasks-per-node=28
#SBATCH --nodes=1
#SBATCH --mem=192GB
#SBATCH --gres=gpu:0
#SBATCH --time=00:01:00
###SBATCH --array 101-102
#SBATCH -o /xdisk/ericlyons/data/ariyanzarei/3d_geocorrection/logs/%x_%A_%a.out

image=/xdisk/kobus/ariyanzarei/singularity_images/full_geocorrection.simg
code=/home/u7/ariyanzarei/projects/3d_postprocessing/main.py
input=/xdisk/ericlyons/data/ariyanzarei/3d_geocorrection/align_result/scanner3DTop-2021-07-15__18-59-42-459_sorghum/full
output=/xdisk/ericlyons/data/ariyanzarei/3d_geocorrection/geo_result/scanner3DTop-2021-07-15__18-59-42-459_sorghum
plants=/xdisk/ericlyons/data/ariyanzarei/3d_geocorrection/2021-07-15__09-45-31-924_sorghum_detection.csv

cd $input
# folders=($(ls -d */))
# dir_name=${folders[${SLURM_ARRAY_TASK_ID}]}

for dir_name in *
do
    echo $dir_name
    singularity exec $image python3 $code -i $input/$dir_name -o $output -p $plants
done


# singularity exec /xdisk/kobus/ariyanzarei/singularity_images/full_geocorrection.simg python3 main.py -i /xdisk/ericlyons/data/ariyanzarei/3d_geocorrection/align_result/scanner3DTop-2021-07-15__18-59-42-459_sorghum/full/2021-07-15__19-01-49-007 -o /xdisk/ericlyons/data/ariyanzarei/3d_geocorrection/geo_result/scanner3DTop-2021-07-15__18-59-42-459_sorghum -p /xdisk/ericlyons/data/ariyanzarei/3d_geocorrection/2021-07-15__09-45-31-924_sorghum_detection.csv