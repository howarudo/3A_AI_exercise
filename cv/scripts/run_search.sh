#!/bin/sh
#SBATCH -p v
#SBATCH --gres=gpu:1
export PATH=/home/app/cuda/bin:$PATH
export LD_LIBRARY_PATH=/home/app/cuda/lib64:$LD_LIBRARY_PATH
poetry run python3 search.py -i data/mini_cifar/test/airplane/airbus_s_001508.png