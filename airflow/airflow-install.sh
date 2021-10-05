kubectl create namespace airflow
helm repo add apache-airflow https://airflow.apache.org
helm install airflow apache-airflow/airflow --namespace airflow
kubectl expose deployment airflow-webserver --type=LoadBalancer --name=web-lb -n airflow