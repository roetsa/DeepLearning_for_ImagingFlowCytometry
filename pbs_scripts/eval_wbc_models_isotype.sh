#!/bin/bash
#PBS -l walltime=10:00:00
#PBS -N eval_wbc_models_isotype

 module load scikit-learn 

datapath="$VSC_DATA_VO_USER/HDF5/WBC/"
runpath="$VSC_DATA_VO_USER/Run/isotype/wbc/" 
FILENAME="$VSC_HOME/DeepLearning_for_ImagingFlowCytometry/selected_cells/wbc_cellnames.txt"

python $VSC_HOME/DeepLearning_for_ImagingFlowCytometry/preprocessing_and_analysis/evaluate_models_isotype.py --run_dir $runpath --data_dir $datapath --type 'wbc' --cellnames_file $FILENAME
