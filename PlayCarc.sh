#!/bin/sh
#SBATCH -p ProdQ
#SBATCH -N 1
#SBATCH -t 1:00:00
#SBATCH -A nuim01

python PlayCarcassonne.py
