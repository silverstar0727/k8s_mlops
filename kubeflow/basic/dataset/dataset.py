import tensorflow as tf
from minio import Minio
import sys

def download_mnist(endpoint, access_key, secret_key):
    client = Minio(
        endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=False,
    )

    if client.bucket_exists("dataset") == False:
        client.make_bucket("dataset")

    tf.keras.datasets.mnist.load_data("./mnist.npz")

    client.fput_object("dataset", "./mnist/mnist.npz", "./mnist.npz")

if __name__ == "__main__":
    endpoint = sys.argv[1]
    access_key = sys.argv[2]
    secret_key = sys.argv[3]
    download_mnist(endpoint, access_key, secret_key)