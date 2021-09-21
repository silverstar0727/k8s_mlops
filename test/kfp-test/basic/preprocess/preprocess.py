import tensorflow as tf
import numpy as np
from minio import Minio

def login(endpoint, access_key, secret_key):
    client = Minio(endpoint, access_key, secret_key)
    client.fget_object("dataset", "mnist/mnist.npz", "./mnist.npz")

def preprocess():
    (x_train, y_train), (x_test, y_test) = np.load("./mnist.npz")

    # Scale images to the [0, 1] range
    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255
    # Make sure images have shape (28, 28, 1)
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)

    print("x_train shape:", x_train.shape)
    print(x_train.shape[0], "train samples")
    print(x_test.shape[0], "test samples")

    np.savez()