#!/bin/sh
#SBATCH -p ProdQ
#SBATCH -N 1
#SBATCH -t 24:00:00
# Charge job to my account 
#SBATCH -A nuim01
# Write stdout+stderr to file
#SBATCH -o output.txt

module load taskfarm
taskfarm MCTasks
