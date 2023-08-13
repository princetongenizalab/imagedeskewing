#!/bin/bash
#SBATCH --job=compress
#SBATCH --output=compress%j.out
#SBATCH --error=compress%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=300M
#SBATCH --time=01:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=eh0560@princeton.edu

module purge
module load anaconda3/2023.3
conda activate torch_env

python /scratch/gpfs/RUSTOW/jts_images/create_compressed_images.py

