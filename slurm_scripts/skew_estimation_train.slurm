#!/bin/bash
#SBATCH --job=skew_estimation_train
#SBATCH --output=logs/skew_estimation_train%j.out
#SBATCH --error=logs/skew_estimation_train%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6
#SBATCH --mem-per-cpu=8
#SBATCH --time=01:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=eh0560@princeton.edu
#SBATCH --gres=gpu:1

module purge
module load anaconda3/2023.3
conda activate tensorflow_env
source $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh

python /scratch/gpfs/eh0560/imagedeskewing/imagedeskewing/skew_estimation_train.py

