#!/bin/sh
#SBATCH -p v
#SBATCH --gres=gpu:1
export PATH=/home/app/cuda/bin:$PATH
export LD_LIBRARY_PATH=/home/app/cuda/lib64:$LD_LIBRARY_PATH
poetry run python3 src/make_acoustic_features.py