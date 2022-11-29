import tensorflow as tf
import tensorflow_hub as hub
from minio import Minio

import os
import tarfile
import math
import timeit
import random
import sys

random_seed = 44
batch_size = 128
datasets_bucket = 'datasets'
preprocessed_data_folder = 'preprocessed-data'
tf_record_file_size = 500
# Set the random seed
tf.random.set_seed(random_seed)

def login(endpoint, access_key, secret_key):
    client = Minio(endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=False)

    return client


def unzip(client):
    client.fget_object(
        datasets_bucket, 
        'aclImdb/aclImdb_v1.tar.gz',
        '/tmp/dataset.tar.gz')

    extract_folder = f'/tmp/{datasets_bucket}/'

    with tarfile.open("/tmp/dataset.tar.gz", "r:gz") as tar:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, path=extract_folder)

    train = []
    test = []

    dirs_to_read = [
        'aclImdb/train/pos',
        'aclImdb/train/neg',
        'aclImdb/test/pos',
        'aclImdb/test/neg',
    ]

    for dir_name in dirs_to_read:
        parts = dir_name.split("/")
        dataset = parts[1]
        label = parts[2]
        for filename in os.listdir(os.path.join(extract_folder,dir_name)):
            with open(os.path.join(extract_folder,dir_name,filename),'r') as f:
                content = f.read()
                if dataset == "train":
                    train.append({
                        "text":content,
                        "label":label
                    })
                elif dataset == "test":
                    test.append({
                        "text":content,
                        "label":label
                    })

    random.Random(random_seed).shuffle(train)
    random.Random(random_seed).shuffle(test)

    return train, test


def preprocess(client, train, test):
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-large/5")

    def _embedded_sentence_feature(value):
        return tf.train.Feature(float_list=tf.train.FloatList(value=value))
    def _label_feature(value):
        return tf.train.Feature(int64_list=tf.train.Int64List(value=value))
    def encode_label(label):
        if label == "pos":
            return tf.constant([1,0])
        elif label == "neg":
            return tf.constant([0,1])

    # This will take the label and the embedded sentence and encode it as a tf.TFRecord
    def serialize_example(label, sentence_tensor):
        feature = {
        'sentence': _embedded_sentence_feature(sentence_tensor[0]),
        'label': _label_feature(label),
        }
        example_proto = tf.train.Example(features=tf.train.Features(feature=feature))
        return example_proto
        
    def process_examples(records,prefix=""):
        starttime = timeit.default_timer()
        total_training = len(records)
        print(f"Total of {total_training} elements")
        total_batches = math.floor(total_training / tf_record_file_size)
        if total_training % tf_record_file_size != 0:
            total_batches += 1 
        print(f"Total of {total_batches} files of {tf_record_file_size} records")

        counter = 0
        file_counter = 0
        buffer = []
        file_list = []
        for i in range(len(records)):
            counter += 1

            sentence_embedding = embed([records[i]['text']])
            label_encoded = encode_label(records[i]['label'])
            record = serialize_example(label_encoded, sentence_embedding) 
            buffer.append(record)

            if counter >= tf_record_file_size:
                print(f"Records in buffer {len(buffer)}")
                # save this buffer of examples as a file to MinIO
                counter = 0
                file_counter+=1
                file_name = f"{prefix}_file{file_counter}.tfrecord"
                with open(file_name,'w+') as f:
                    with tf.io.TFRecordWriter(f.name,options="GZIP") as writer:
                        for example in buffer:
                            writer.write(example.SerializeToString())
                client.fput_object(datasets_bucket, f"{preprocessed_data_folder}/{file_name}", file_name)
                file_list.append(file_name)
                os.remove(file_name)
                buffer=[]
                print(f"Done with chunk {file_counter}/{total_batches} - {timeit.default_timer() - starttime}")
        if len(buffer) > 0:
            file_counter+=1
            file_name = f"file{file_counter}.tfrecord"
            with open(file_name,'w+') as f:
                with tf.io.TFRecordWriter(f.name) as writer:
                    for example in buffer:
                        writer.write(example.SerializeToString())
            client.fput_object(datasets_bucket, f"{preprocessed_data_folder}/{file_name}", file_name)
            file_list.append(file_name)
            os.remove(file_name)
            buffer=[]
        print("Total time preprocessing is :", timeit.default_timer() - starttime)
        return file_list
        
    process_examples(train,prefix="train")
    process_examples(test,prefix="test")
    print("Done Preprocessing data!")


if __name__ == "__main__":
    endpoint = sys.argv[1]
    access_key = sys.argv[2]
    secret_key = sys.argv[3]
    
    client = login(endpoint, access_key, secret_key)
    train, test = unzip(client)
    preprocess(client, train, test)