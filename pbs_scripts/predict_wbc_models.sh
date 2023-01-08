#!/bin/bash
#PBS -l walltime=30:0:0
#PBS -l nodes=1:ppn=quarter,gpus=1
#PBS -N predict_wbc_models
#PBS -m abe
#PBS -t 1-172

module load TensorFlow/2.4.1-fosscuda-2020b
pip install --user -r DeepLearning_for_ImagingFlowCytometry/requirements_hpc.txt

datapath="$VSC_DATA_VO_USER/HDF5/WBC"
runpath="$VSC_DATA_VO_USER/Run/wbc"
configpath="$VSC_HOME/DeepLearning_for_ImagingFlowCytometry/configs/generated/wbc"
scripthpath="$VSC_HOME/DeepLearning_for_ImagingFlowCytometry/main.py"

FILENAME="$VSC_HOME/DeepLearning_for_ImagingFlowCytometry/selected_cells/wbc_cellnames.txt"

CELL_ID=$((PBS_ARRAYID - 1))
LINES=$(cat $FILENAME)
readarray -t arr <$FILENAME
LINE=${arr[${CELL_ID}]}

echo "Start predicting $LINE"
mkdir -p $runpath/$LINE
python $scripthpath predict $configpath/pred-2-deepflow_hpc_$LINE.json  -r $runpath/$LINE/ $datapath/
