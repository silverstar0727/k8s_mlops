import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
import os 

mlflow.set_tracking_uri('http://34.133.252.129:5000/')

# Setting the requried environment variables
os.environ['MLFLOW_S3_ENDPOINT_URL'] = "http://34.71.39.91:9000/" 
os.environ['AWS_ACCESS_KEY_ID'] = 'minio'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'minio123' 

# dataset
iris = datasets.load_iris()
iris_train = pd.DataFrame(iris.data, columns=iris.feature_names)

# model
clf = RandomForestClassifier(max_depth=7, random_state=0)
clf.fit(iris_train, iris.target)

# mlflow model
signature = infer_signature(iris_train, clf.predict(iris_train))
mlflow.sklearn.log_model(clf, "iris_rf", signature=signature)