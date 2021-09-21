from minio import Minio
import os
import sys
import glob

def upload_data_zip(client, local_file, bucket_name, minio_file):
    print(local_file)
    client.fput_object(bucket_name=bucket_name, object_name=minio_file, file_path=local_file)

def upload_local_directory_to_minio(client, local_path, bucket_name, minio_path):
    assert os.path.isdir(local_path)

    for local_file in glob.glob(local_path + '/**'):
        local_file = local_file.replace(os.sep, "/") # Replace \ with / on Windows
        print(local_file)
        if not os.path.isfile(local_file):
            upload_local_directory_to_minio(
                client, local_file, bucket_name, minio_path + "/" + os.path.basename(local_file))
        else:
            remote_path = os.path.join(
                minio_path, local_file[1 + len(local_path):])
            remote_path = remote_path.replace(
                os.sep, "/")  # Replace \ with / on Windows
            client.fput_object(bucket_name, remote_path, local_file)

def dataset_upload_component(endpoint, access_key, secret_key, minio_path="aclImdb", local_path="./aclImdb"):
    client = Minio(
        endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=False,
    )

    if client.bucket_exists("dataset") == False:
        client.make_bucket("dataset")

    upload_data_zip(client=client, local_file="aclImdb_v1.tar.gz", bucket_name="dataset", minio_file="aclImb/aclImdb_v1.tar.gz")
    upload_local_directory_to_minio(client=client, local_path=local_path, bucket_name="dataset", minio_path=minio_path)

if __name__ == "__main__":
    endpoint = sys.argv[1]
    access_key = sys.argv[2]
    secret_key = sys.argv[3]
    dataset_upload_component(endpoint, access_key, secret_key)
