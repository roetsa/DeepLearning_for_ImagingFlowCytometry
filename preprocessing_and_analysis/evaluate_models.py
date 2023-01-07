import argparse
import os
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, roc_auc_score, balanced_accuracy_score, f1_score, precision_score, \
    recall_score

parser = argparse.ArgumentParser(description='calculates accuracy for models')

parser.add_argument("--run_dir", help="run_dir")
parser.add_argument("--data_dir", help="data_dir")
parser.add_argument("--type", help="wbc or pbmc")
parser.add_argument("--cellnames_file", help="filepath to list")
args = parser.parse_args()


def calculate_metrics(run_dir, data_dir, cell_name):
    """
    This functions evaluates the predictions of a cell. A set of metrics is used

    Input :

    run_dir: run directory containing the predictions made by the model
    data_dir: data directory containing the true label of the cell name
    cell_name: reference to cell

    Output:

    True Positives, True negatives, False negatives, True positives,
    AUC, Accuracy, Balanced Accuracy, F1-score, Precision, Recall

    """
    predictions = np.load(run_dir + cell_name + '/predictions.npy')
    split = data_dir + 'Split/' + cell_name
    pred_indices = np.loadtxt(Path(split, "test.txt"), dtype=int)
    y_pred = np.rint(predictions.squeeze()).astype(int)
    meta = pd.read_csv(data_dir + cell_name + '_meta.csv')
    labels = meta["label"].values
    y_true = labels[pred_indices]
    TP = np.sum(np.logical_and(y_pred == 1, y_true == 1))
    TN = np.sum(np.logical_and(y_pred == 0, y_true == 0))
    FP = np.sum(np.logical_and(y_pred == 1, y_true == 0))
    FN = np.sum(np.logical_and(y_pred == 0, y_true == 1))
    acc = accuracy_score(y_true, y_pred)
    auc = roc_auc_score(y_true, predictions.squeeze())
    bacc = balanced_accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    return TN, FP, FN, TP, auc, acc, bacc, f1, precision, recall


def evaluation(run_dir, data_dir, type_cell, cellnames_file):
    """
    This functions evaluates the predicted values of the model on a set of cells.
    The results are written to the file results_{type_cell}.csv in the run directory
    Input :

    run_dir: run directory containing the predictions made by the model
    data_dir: data directory containing the true label of the cell name
    type_cell: pbmc or  wbc
    cellnames_file: File containing cell names


    """

    df = pd.DataFrame(columns=['Name', 'Accuracy'])
    result_path = run_dir + 'results_' + type_cell + '.csv'
    df_cell = pd.read_csv(cellnames_file, header=None).squeeze()
    for _, cellname in df_cell.items():
        if os.path.exists(run_dir + cellname + '/predictions.npy'):
            TN, FP, FN, TP, auc, acc, bacc, f1, precision, recall = calculate_metrics(run_dir, data_dir, cellname)
            dict = {'Name': cellname, 'Accuracy': acc, 'TN': TN, 'FP': FP, 'FN': FN, 'TP': TP, 'AUC': auc,
                    'Balanced accuracy': bacc, 'F1-score': f1, 'Precision': precision, 'Recall': recall}
            df = df.append(dict, ignore_index=True)
        else:
            print('no predictions for ', cellname)
    df.to_csv(result_path, index=False)
    print('written to', result_path)

evaluation(args.run_dir, args.data_dir, args.type, args.cellnames_file)
