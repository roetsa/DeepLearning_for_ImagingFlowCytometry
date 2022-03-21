import functions.train
import tensorflow as tf
from joblib import Parallel, delayed
from pathlib import Path
import main
import model
import time
import preprocessing
import numpy as np

def run(args):
    main.prerun(args, run_dir=False, exp=False)

    with tf.device("/cpu:0"): 
        data = preprocessing.load_hdf5_to_memory(args, None)
        ds, ds_len = preprocessing.load_dataset(data, None, None, args, type="pred")

    m = model.load_model(args)
    
    preds = m.predict(
        ds,
        steps = int(np.ceil(ds_len / args["batch_size"])),
    )

    path=args["run_dir"]+"predictions.npy"
    np.save(path, preds)
