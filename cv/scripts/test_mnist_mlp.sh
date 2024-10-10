#!/bin/sh
#SBATCH -p v
#SBATCH --gres=gpu:1
export PATH=/home/app/cuda/bin:$PATH
export LD_LIBRARY_PATH=/home/app/cuda/lib64:$LD_LIBRARY_PATH
poetry run python3 test_mnist_mlp.py -g 0 -i data/mnist_zero.png -m result/model_20
