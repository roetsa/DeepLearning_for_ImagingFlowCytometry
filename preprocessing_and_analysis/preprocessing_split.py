import argparse
import os
import random

import numpy as np
import pandas as pd
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import train_test_split

random.seed(1234)

parser = argparse.ArgumentParser(
    description='Split model in a train validation set based on 60-20-20 and oversample minority class')
parser.add_argument("--data_dir", help="data_dir")
parser.add_argument("--cellnames_file", help="File containing cellnames to train")
args = parser.parse_args()


def sample_and_split(cellnames_file, run_dir):
    df_cell = pd.read_csv(cellnames_file, header=None).squeeze()
    for _, cellname in df_cell.items():
        split_train_validation_test(cellname, run_dir)


def split_train_validation_test(plate, run_dir):
    filename = plate + "_meta.csv"
    df = pd.read_csv(run_dir + filename)
    df.reset_index(inplace=True)
    X = df['index'].to_numpy().reshape(-1, 1)
    y = df['label'].to_numpy()

    X_train, X_rem, y_train, y_rem = train_test_split(X, y, train_size=0.6, random_state=1234, stratify=y)
    X_valid, X_test, y_valid, y_test = train_test_split(X_rem, y_rem, test_size=0.5, stratify=y_rem)
    oversample = RandomOverSampler(sampling_strategy='minority')
    X_train, y_train = oversample.fit_resample(X_train, y_train)
    folder = run_dir + "Split/" + plate

    if not os.path.exists(folder):
        os.makedirs(folder)
        print("The new directory is created!")

    np.savetxt(folder + "/train.txt", X_train, fmt='%d')
    np.savetxt(folder + "/val.txt", X_valid, fmt='%d')
    np.savetxt(folder + "/test.txt", X_test, fmt='%d')  # Script to split data into train, validation and test set


sample_and_split(args.cellnames_file, args.data_dir)
