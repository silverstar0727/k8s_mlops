FROM tensorflow/tensorflow

WORKDIR /app
COPY . .

RUN pip install minio

RUN apt-get update
RUN apt-get install wget

RUN wget https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz
RUN tar -xvf aclImdb_v1.tar.gz

ENTRYPOINT ["python", "dataset.py"]