#!/bin/bash
#SBATCH --job=high_priority_deskewing
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
#SBATCH --gres=gpu:1
#SBATCH --time=10:00:00
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --mail-type=fail
#SBATCH --mail-user=eh0560@princeton.edu

module purge
module load anaconda3/2023.3
conda activate torch_env

python high_priority_deskewing.py