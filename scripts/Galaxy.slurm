#This is the SLURM job used for generating 10 million binaries in a single galaxy. 
#This was used to run the code on Northwestern's Quest Cluster for HPC.
#The code starts from '#!/bin/bash' and is not a comment.
#----------------------------------------------------------------------------
#!/bin/bash
#SBATCH --account='accname' # Your allocation/account name
#SBATCH --partition=ciera-std # Partition name
#SBATCH --job-name=binary_batch_test         # Job name
#SBATCH --array=0-i                          # Run i jobs: batch 0 to i-1
#SBATCH --ntasks=1                           # Only 1 task per job
#SBATCH --cpus-per-task=8                    # Use 4 CPUs per job
#SBATCH --mem=20G                            # Memory per job
#SBATCH --time=01:00:00                      # Max time per job
#SBATCH --output=logs/outputfilename%A_%a.out        # Standard output
#SBATCH --error=logs/output%A_%a.err         # Error log output

# --- Run Python script with batch index ---
# Force Python to use conda binary explicitly
"/User/path" generation.py --batch-index ${SLURM_ARRAY_TASK_ID}
