#!/usr/bin/env bash
###########################################################################
# job.slurm                                             (June, 2021 Zheting)
#
# Script for submitting jobs to the cluster (slurm)
#
# Submit the script with "sbatch job.slurm".
# List your queued and running jobs "squeue --me".
# Cancel a queued or running job, e.g. a job with ID 12345 "scancel 12345"
# Check status of a job, "sacct -j 12345"
# Check how efficiently a job ran, "seff 12345"
###########################################################################
# Lines that begin with #PBS are PBS directives (not comments).
# True comments begin with "# " (# followed by a space).
###########################################################################

#SBATCH --job-name=BSCCO
#SBATCH --out="log.-%j"
#SBATCH --partition scavenge --time=1-00:00:00
#SBATCH --requeue 
#SBATCH --nodes=20 --ntasks-per-node=8
#SBATCH --mem=20G
#SBATCH --export=ALL

cd ${SLURM_SUBMIT_DIR}
echo '-------------------------------'
echo Working directory is 
pwd
echo Running on host $(hostname)
echo Time is $(date)
echo SLURM_NODES are $(echo ${SLURM_NODELIST})
echo '-------------------------------'
echo -e '\n\n'
rm finish
touch running

if test -f "CONTCAR"; then
    echo "CONTCAR exists, cp CONTCAR POSCAR"
    cp POSCAR POSCAR_${SLURM_JOBID}
    cp CONTCAR POSCAR
fi

module load VASP/5.4.1-iomkl-2018b

srun -n 160 vasp_std

rm running
touch finish
