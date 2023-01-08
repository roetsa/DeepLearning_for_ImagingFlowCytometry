# Deep Learning for Imaging Flow Cytometry

This repository contains the code used to generate results for the master thesis:

**_Stain-free cell marker identification with neural networks_**

The code was taken from this [repository](https://github.com/saeyslab/DeepLearning_for_ImagingFlowCytometry) and contains the adaptations for the specific problem setting.

## Research objectives

- Identify which surface proteins can be identified by stain-free information
- Compare the data set of white blood cells to the peripheral blood mononuclear cells
data set to see if this helps the performance for detecting specific surface proteins
linked to rare cell types.

## Problem setting

For the identification of the stain-free cell marker, 2 datasets where available
- First dataset of samples of white blood cells (WBC) 
- Second dataset of  peripheral blood mono nuclear cells (PBMC)

In each data set, samples per stain-free cell marker where available.
As there is 3-5% noise, a [script](https://github.com/roetsa/DeepLearning_for_ImagingFlowCytometry/blob/master/preprocessing_and_analysis/generate_config_files.py) filters out only the samples where the values lie between 5% and 90%.

This leads to [164](https://github.com/roetsa/DeepLearning_for_ImagingFlowCytometry/blob/master/selected_cells/pbmc_cellnames.txt) binary classifiers to train for the PBMC dataset and [172](https://github.com/roetsa/DeepLearning_for_ImagingFlowCytometry/blob/master/selected_cells/wbc_cellnames.txt) to train for the WBC dataset.
Because of the amount of classifiers, a train-validation-test set was used instead of cross validation.

Furthermore, the original model (Deepflow) was trained for a multi-classification problem,
the code was adapted for binary classification.

### Prerequisites
This installation requires Python (tested on version 3.6 and 3.7) and git.

The requirements for the packages can be found [here](). 

The [HPC infrastructure](https://www.ugent.be/hpc/en) of Ghent University was used to obtain the results.

### Framework installation
Clone this repository:
```
https://github.com/roetsa/DeepLearning_for_ImagingFlowCytometry
```
Use the package manager pip to install all dependencies:
```
pip install -r requirements_hpc.txt
```
## Usage
### Data
#### Images
Images should be fed to the network in the form of HDF5 files containing images and accompanying masks.

The HDF5-file is required to have the following structure:
- channel_1 (HDF5 Group)
  - images (HDF5 Dataset, uint16 2D-arrays)
  - masks (HDF5 Dataset, boolean 2D-arrays)
- channel_9
  - images
  - masks
- ...

The datasets in all the groups need to have a corresponding order. This means that `data["channel_1/images"][0]` and `data["channel_9/images"][0]` are both images of the same cell. Also `data["channel_1/masks"][0]` is the mask for `data["channel_1/images"][0]`.

In case your data is acquired on an Amnis-platform a [tool](https://github.com/saeyslab) is available to convert CIF-files (as exported from IDEAS software) to the required HDF5-files.
#### Labels
For training, a textfile needs to be provided containing the class labels for each input image. The labels are assumed to be in the same order as the HDF5-file. 
For this problem, the hdf5 files for one sample where split over 2 files depending on their label.
A script creating 1 hdf5 file and the corresponding file with label information can be found [here](https://github.com/roetsa/DeepLearning_for_ImagingFlowCytometry/blob/master/pbs_scripts/preprocessing_hdf5.pbs)
#### Train-validation-test
Contrary to the original problem, no cross validation was done because of computing costs.
Instead the files where split into 3 sets and oversampling was done on the training set to account for class imbalance.
The script can be found [here](https://github.com/roetsa/DeepLearning_for_ImagingFlowCytometry/blob/master/pbs_scripts/preprocessing_split.pbs)

Adirectory structure containing train-validation-test splits needs to be provided. The structure is as follows:
- 0
  - train.txt
  - val.txt
  - test.txt
- 1
  - train.txt
  - val.txt
  - test.txt
- ...

The txt-files contain `int`s separated by newlines. Each int refers to a cell in the HDF5 file.

### Deep learning
The framework contains 5 functionalities but only 2 were used in this thesis
- training (`train`),
- predicting (`predict`),

The basic command to run any of the functionalities is
```
python main.py function_name json_config run_dir data_root 
```
with `python main.py` fixed,
- `function_name` any of the names in brackets above,
- `json_config` a json-file containing all options,
- `run_dir` path to a dir where output can be stored,
- and `data_root` path to root dir containing data.

#### Functionalities overview

##### Training (`train`)
In order to perform training you need to provide the HDF5-file with images and masks and the labels as explained under [Data](###Data).

The framework will store several items in `run_dir`:
- best model,
- file with all metrics
##### Prediction (`predict`)
In order to perform training you need to provide the HDF5-file with images and masks and the labels as explained under [Data](###Data).

The framework will store several items in `run_dir`:
- file with all metrics

After predicting the labels on the test set, a script can be run to get the evaluation metrics of the cells in one file.

#### JSON-config
All parameters required to use a functionality are read from a JSON-config file. Some [example configs](./configs/) are available in this repository.

For this problem setting, the configs are not uploaded on github. The script to generate the config per classifier can be found [here](https://github.com/roetsa/DeepLearning_for_ImagingFlowCytometry/blob/master/preprocessing_and_analysis/generate_config_files.py)

#### Data root
This is the path the first common parent directory of the results directory, HDF5-file and labels-file. In the config file, make sure to specify all directories and files relative to the data root.

This setup makes it easy to re-use JSON-configs accross machines, as long as the directory tree starting from the data root is the same for every machine.

#### Special case: isotype

Ten samples in each dataset are labeled as isotypes, the specific identifiers are listed [here](https://github.com/roetsa/DeepLearning_for_ImagingFlowCytometry/blob/master/selected_cells/isotype_cellnames.txt)
Isotypes can be used to check for spectral overlap. Some of it is removed by the IDEAS
software with spectral compensation, but not all. With spectral overlap, some fluorescent emission might have spilled over on the brightfield or darkfield images. The model
should not use this information to predict the class. To test that it is not using this information, isotypes do not contain any antibodies which will bind with proteins and stain for
the specific surface protein of the classifier and there can be no spectral overlap. However,
this also means that there is no ground truth available, since the staining is used for the
labelling. If the assumption is made that the cell distribution is the same across the wells,
they should predict the same proportion of positive labels for a specific surface protein
as for the well where the stain was added. If the model got information through spectral
overlap to identify the surface-protein, the proportions will be different. 

=> scripts specific for isotype checking are listed with _isotype.

#### Lessons learned

The original repository already had everything implemented for the cross validation (including the evaluation of the metrics). 
Switching to the train-validation-set required extra scripting. On the HPC clusters, the training did not take as long as expected.
For a subset where the results of the classification are good, it makes sense to try the cross validation approach.
