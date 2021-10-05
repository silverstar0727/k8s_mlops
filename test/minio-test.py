from minio import Minio

endpoint = "104.197.17.36"
access_key = "minioadmin"
secret_key = "minioadmin"

client = Minio(
    endpoint,
    access_key=access_key,
    secret_key=secret_key,
    secure=False,
)

client.make_bucket("abc")