#!/bin/bash
#PBS -l walltime=10:00:00
#PBS -N generate_config_files

meta_file='$VSC_HOME/Metadata.csv'
percent_minimum=5
ouput_dir='$VSC_HOME'
generated_config_dir='$VSC_HOME/DeepLearning_for_ImagingFlowCytometry/configs/generated'
model_dir='$VSC_DATA_VO_USER/Run'

module load pandas

python $VSC_HOME/DeepLearning_for_ImagingFlowCytometry/preprocessing_and_analysis/generate_config_files.py --output_dir $VSC_HOME/ --model_dir $VSC_DATA_VO_USER/Run/  --generated_config_dir $VSC_HOME/DeepLearning_for_ImagingFlowCytometry/configs/generated/ --meta_file $VSC_HOME/Metadata.csv --percent_minimum 5
