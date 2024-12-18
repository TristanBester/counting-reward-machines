#!/bin/bash
mkdir -p ~/warehouse/slurm_logs/error
mkdir -p ~/warehouse/slurm_logs/out

# Setup environment 
cd ~/warehouse
uv sync --extra experiments

# Start training
cd ~/warehouse/scripts/train/debug

echo "CSAC..."
sbatch --exclude=mscluster[8,9,35,42,44,46,47,54,57,59,61,62,65,67,68,75,76] csac/serial.sbatch 0 
sleep 30s
sbatch --exclude=mscluster[8,9,35,42,44,46,47,54,57,59,61,62,65,67,68,75,76] csac/parallel.sbatch 0
sleep 30s

echo "SAC..."
sbatch --exclude=mscluster[8,9,35,42,44,46,47,54,57,59,61,62,65,67,68,75,76] sac/serial.sbatch 0 
sleep 30s
sbatch --exclude=mscluster[8,9,35,42,44,46,47,54,57,59,61,62,65,67,68,75,76] sac/parallel.sbatch 0
