import argparse
import os

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(description='All indices to text file for test isotype')
parser.add_argument("--data_dir", help="data_dir")
parser.add_argument("--cellnames_file", help="File containing cellnames to train")
args = parser.parse_args()


def sample_and_split(cellnames_file, run_dir):
    df_cell = pd.read_csv(cellnames_file, header=None).squeeze()
    for _, cellname in df_cell.items():
        write_indices(cellname, run_dir)


def write_indices(plate, run_dir):
    filename = plate + "_meta.csv"
    df = pd.read_csv(run_dir + filename)
    df.reset_index(inplace=True)
    X = df['index'].to_numpy().reshape(-1, 1)
    y = df['label'].to_numpy()

    folder = run_dir + "Split_isotype/" + plate

    if not os.path.exists(folder):
        os.makedirs(folder)
        print("The new directory is created!")

    np.savetxt(folder + "/test.txt", X, fmt='%d')


sample_and_split(args.cellnames_file, args.data_dir)
