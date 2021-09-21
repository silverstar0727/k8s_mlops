FROM tensorflow/tensorflow

WORKDIR /app
COPY . .

RUN pip install minio

ENTRYPOINT [ "python", "preprocess.py" ]