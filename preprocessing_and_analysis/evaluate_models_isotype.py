import argparse
import os
from pathlib import Path

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(description='calculates accuracy for models')

parser.add_argument("--run_dir", help="run_dir")
parser.add_argument("--data_dir", help="data_dir")
parser.add_argument("--type", help="wbc or pbmc")
parser.add_argument("--cellnames_file", help="filepath to list")
args = parser.parse_args()


def calculate_metrics(run_dir, data_dir, cell_name):
    predictions = np.load(run_dir + cell_name + '/predictions.npy')
    split = data_dir + 'Split_isotype/' + cell_name
    pred_indices = np.loadtxt(Path(split, "test.txt"), dtype=int)
    y_pred = np.rint(predictions.squeeze()).astype(int)
    meta = pd.read_csv(data_dir + cell_name + '_meta.csv')
    labels = meta["label"].values
    y_true = labels[pred_indices]
    prop_true = y_true.mean()
    prop_pred = y_pred.mean()
    print(prop_true, prop_pred)
    return prop_true, prop_pred


def evaluation(run_dir, data_dir, type_cell, cellnames_file):
    df = pd.DataFrame(columns=['Name', 'Accuracy'])
    # todo loop over list of isotypes instead of hardcoding the name
    result_path = run_dir + 'results_isotype_Plate1_A06_' + type_cell + '.csv'
    df_cell = pd.read_csv(cellnames_file, header=None).squeeze()
    for _, cellname in df_cell.items():
        if os.path.exists(run_dir + cellname + '/predictions.npy'):
            prop_true, prop_pred = calculate_metrics(run_dir, data_dir, cellname)
            dict = {'Name': cellname, 'Percentage y_true': prop_true, 'Percentage y_pred': prop_pred}
            df = df.append(dict, ignore_index=True)
        else:
            print('no results for', cellname)
    df.to_csv(result_path, index=False)
    print('written to', result_path)


evaluation(args.run_dir, args.data_dir, args.type, args.cellnames_file)
