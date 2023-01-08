#!/bin/bash
#PBS -l walltime=10:00:00
#PBS -N generate_config_files_isotype

meta_file='$VSC_HOME/Metadata.csv'
percent_minimum=5
generated_config_dir='$VSC_HOME/DeepLearning_for_ImagingFlowCytometry/configs/generated/isotype/'
model_dir='$VSC_DATA_VO_USER/Run/isotype/'

module load pandas

python $VSC_HOME/DeepLearning_for_ImagingFlowCytometry/preprocessing_and_analysis/generate_config_files_isotype.py --model_dir $VSC_DATA_VO_USER/Run/  --generated_config_dir $VSC_HOME/DeepLearning_for_ImagingFlowCytometry/configs/generated/isotype/ --meta_file $VSC_HOME/Metadata.csv --percent_minimum 5
