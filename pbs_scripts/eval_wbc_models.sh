#!/bin/bash
#PBS -l walltime=10:00:00
#PBS -N eval_wbc_models

 module load scikit-learn 

datapath="$VSC_DATA_VO_USER/HDF5/WBC/"
runpath="$VSC_DATA_VO_USER/Run/wbc/" 
FILENAME="$VSC_HOME/DeepLearning_for_ImagingFlowCytometry/selected_cells/wbc_cellnames.txt"

python $VSC_HOME/DeepLearning_for_ImagingFlowCytometry/preprocessing_and_analysis/evaluate_models.py --run_dir $runpath --data_dir $datapath --type 'wbc' --cellnames_file $FILENAME
