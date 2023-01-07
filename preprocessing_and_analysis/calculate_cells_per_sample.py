import argparse

import pandas as pd

parser = argparse.ArgumentParser(description='Calculates cell per well')
parser.add_argument("--data_dir", help="data_dir")
parser.add_argument("--cellnames_file", help="File containing cellnames to train")
args = parser.parse_args()


def count_cells(cellnames_file, run_dir):
    """
    This function calculates the number of cells,
     the output is written to the Split directory in the run folder.
    """
    df_cell = pd.read_csv(cellnames_file, header=None).squeeze()
    dict_length = {}
    dict_perc = {}
    for _, cellname in df_cell.items():
        filename = cellname + "_meta.csv"
        df = pd.read_csv(run_dir + filename)
        df.reset_index(inplace=True)
        dict_length[cellname] = len(df['label'].to_numpy())
        dict_perc[cellname] = df['label'].mean()
        folder = run_dir + "Split/"

    with open(folder + 'count_cells.csv', 'w') as f:
        for key in dict_length.keys():
            f.write("%s, %s\n" % (key, dict_length[key]))
    with open(folder + 'perc_cells.csv', 'w') as f:
        for key in dict_perc.keys():
            f.write("%s, %s\n" % (key, dict_perc[key]))


count_cells(args.cellnames_file, args.data_dir)
