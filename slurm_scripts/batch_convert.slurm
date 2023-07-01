#!/bin/bash
#SBATCH --job=batch_image_conversion
#SBATCH --output=batch_image_conversion_%j.out
#SBATCH --error=batch_image_conversion_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=00:10:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=eh0560@princeton.edu

module purge
module load anaconda3/2023.3
conda activate torch_env

python /scratch/gpfs/eh0560/imagedeskewing/imagedeskewing/utils/batch_convert.py --input_dir /scratch/gpfs/RUSTOW/htr_deskewing_image_dataset --input_format tif --output_format jpg --quality 90 --recursive
