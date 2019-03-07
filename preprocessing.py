import tensorflow as tf
import time
from pathlib import Path
import numpy as np


def preprocess_image(image, args):
    image = tf.image.decode_png(image, channels=1, dtype=tf.uint16)
    image = tf.image.resize_images(image, [args["image_width"], args["image_height"]])
    image = tf.squeeze(image, axis=[2])
    image = tf.cast(image, tf.float32)
    image /= 2**16

    return image

def load_and_preprocess_image(path, args):
    image = tf.read_file(path)
    return preprocess_image(image, args)


def load_and_preprocess_images(paths, args):
    return tf.map_fn(
        lambda j: load_and_preprocess_image(j, args),
        paths,
        dtype=tf.float32
    )

def load_dataset(indices_file, cache_file, meta, args, type="train", augment_func = None):

    if indices_file is not None:
        indices = np.loadtxt(indices_file, dtype=int)
        meta = meta.iloc[indices]

    image_columns = ["image_%s" % str(c) for c in args["channels"]]

    all_image_paths = meta[image_columns].applymap(lambda path: str(Path(args["image_base"], path)))
    all_image_labels = meta["label"]
    
    if type=="train":
        X = []
        for i in range(args["noc"]):
            indices = all_image_labels.index[all_image_labels == i]
            X.append(
                tf.data.Dataset.from_tensor_slices((
                    all_image_paths.loc[indices].values, 
                    all_image_labels.loc[indices].values
                ))
                .shuffle(buffer_size=len(indices))
                .map(lambda i, l: (load_and_preprocess_images(i, args), l), num_parallel_calls=8)
                .cache()
                .repeat()
            )
        ds = tf.data.experimental.sample_from_datasets(X, weights=args["sample_weights"]).repeat()

        if augment_func is not None:
            ds = ds.map(lambda i, l: (augment_func(i), l))

        ds = ds.batch(args["batch_size"]).prefetch(buffer_size=256)
    elif type=="val":
        ds = tf.data.Dataset.from_tensor_slices((
            all_image_paths.values, 
            all_image_labels.values
        ))
        ds = ds.map(lambda i, l: (load_and_preprocess_images(i, args), l), num_parallel_calls=8).cache(filename=cache_file)
        ds = ds.batch(args["batch_size"]).prefetch(buffer_size=256)
    else:
        raise RuntimeError("Wrong argument value (%s)" % type)

    return ds, meta.shape[0] 


def load_datasets(train_indices, val_indices, train_cache, val_cache, meta, args, augment_func):
    train_ds, train_steps = load_dataset(train_indices, train_cache, meta, args, "train", augment_func)
    val_ds, val_steps = load_dataset(val_indices, val_cache, meta, args, "val")

    return train_ds, val_ds, train_steps, val_steps


def apply_augmentation(image):
    image = tf.transpose(image, [1, 2, 0])

    angle = tf.random_uniform([], -3.14, 3.14, tf.float32, None, "angle")
    dx = tf.random_uniform([], -6, 6, tf.float32)
    dy = tf.random_uniform([], -6, 6, tf.float32)

    # Randomly flip the image horizontally.
    distorted_image = tf.image.random_flip_left_right(image)
    # Randomly flip the image vertically.
    distorted_image = tf.image.random_flip_up_down(distorted_image)
    # Randomly rotate the image
    distorted_image = tf.contrib.image.rotate(distorted_image, angle)

    distorted_image = tf.contrib.image.translate(distorted_image, [dx, dy])

    distorted_image = tf.transpose(distorted_image, [2, 0, 1])
    return distorted_image


if __name__ == "__main__":
    tf.enable_eager_execution()

    from collections import Counter
    import arguments
    from pathlib import Path
    import pandas as pd
    from matplotlib import pyplot as plt

    args = arguments.get_args()
    meta = pd.read_csv(args["meta"])
    train_indices = Path(args["split_dir"], "val.txt")
    train_cache = str(Path("caches", "test"))

    ds, _ = load_dataset(train_indices, train_cache, meta, args, "train", augment_func=apply_augmentation)

    overall_start = time.time()
    # Fetch a single batch to prime the pipeline (fill the shuffle buffer),
    # before starting the timer
    batches = 30
    it = iter(ds)
    next(it)

    count = Counter({})
    times = []

    start = time.time()
    for i,(images,labels) in enumerate(it):
        a = time.time()
        times.append(a-start)
        start = a

        if i == 30: 
            break

    plt.plot(times)
    plt.savefig("tmp.png")




 