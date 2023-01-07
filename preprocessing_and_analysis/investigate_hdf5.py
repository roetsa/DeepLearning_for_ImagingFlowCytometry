import h5py
import pandas as pd


def print_objs(name):
    print(name)


path_pos = "/data/gent/vo/000/gvo00070/Newcastle_IFC/LabelFreeCDs/HDF5/WBC/PePos/Plate2/C01.h5"
path_neg = "/data/gent/vo/000/gvo00070/Newcastle_IFC/LabelFreeCDs/HDF5/WBC/PeNeg/Plate2/C01.h5"
path_end = "/data/gent/vo/000/gvo00070/vsc44507/HDF5/WBC/Plate2_C01_90x90.h5"
meta = "/data/gent/vo/000/gvo00070/vsc44507/HDF5/WBC/Plate2_C01_meta.csv"
with h5py.File(path_pos, 'r') as f:
    print('positive')
    f.visit(print_objs)
with h5py.File(path_neg, 'r') as f:
    print('negative')
    f.visit(print_objs)
with h5py.File(path_end, 'r') as f:
    print('end result')
    f.visit(print_objs)

meta = pd.read_csv(prefix + "_meta.csv")
print(meta.shape())
