#!/bin/bash
#PBS -l walltime=10:00:00
#PBS -N eval_pbmc_models

module load scikit-learn

datapath="$VSC_DATA_VO_USER/HDF5/PBMC/"
runpath="$VSC_DATA_VO_USER/Run/pbmc/" 
FILENAME="$VSC_HOME/DeepLearning_for_ImagingFlowCytometry/selected_cells/pbmc_cellnames.txt"

python $VSC_HOME/DeepLearning_for_ImagingFlowCytometry/preprocessing_and_analysis/evaluate_models.py --run_dir $runpath --data_dir $datapath --type 'pbmc' --cellnames_file $FILENAME
