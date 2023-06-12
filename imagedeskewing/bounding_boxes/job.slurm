#!/bin/bash
#SBATCH --job=bounding_box_test
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --gres=gpu:1
#SBATCH --time=00:05:00
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-type=fail
#SBATCH --mail-user=eh0560@princeton.edu

module purge
module load anaconda3/2023.3
module load cudnn/cuda-11.x/8.2.0
module load cudatoolkit/11.7
conda activate torch-env
