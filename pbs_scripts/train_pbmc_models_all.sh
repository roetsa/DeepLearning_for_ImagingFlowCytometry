#!/bin/bash
#PBS -l walltime=30:0:0
#PBS -l nodes=1:ppn=quarter,gpus=1  
#PBS -N train_pbmc_models_all
#PBS -m abe

module load TensorFlow/2.4.1-fosscuda-2020b
pip install --user -r DeepLearning_for_ImagingFlowCytometry/requirements_hpc.txt

datapath="$VSC_DATA_VO_USER/HDF5/PBMC"
runpath="$VSC_DATA_VO_USER/Run/pbmc"
configpath="$VSC_HOME/DeepLearning_for_ImagingFlowCytometry/configs/generated/pbmc"
scripthpath="$VSC_HOME/DeepLearning_for_ImagingFlowCytometry/main.py"

FILENAME="$VSC_HOME/DeepLearning_for_ImagingFlowCytometry/selected_cells/pbmc_cellnames.txt"

LINES=$(cat $FILENAME)

train=0

for LINE in $LINES
do
	echo "Start training $LINE"
	mkdir -p $runpath/$LINE/
	rm -f $runpath/$LINE/initial_model_weights.h5
        cp  $VSC_HOME/DeepLearning_for_ImagingFlowCytometry/weights/deepflow-wbc-bfdf.h5 $runpath/$LINE/initial_model_weights.h5
	python $scripthpath train $configpath/train-2-deepflow_hpc_$LINE.json  -r $runpath/$LINE/ $datapath/
	break
done
