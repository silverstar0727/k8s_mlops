# https://www.youtube.com/watch?v=39k2Sz9jZ2c
# https://airflow.apache.org/docs/helm-chart/stable/airflow-configuration.html
kubectl create namespace airflow
helm repo add apache-airflow https://airflow.apache.org
helm install airflow apache-airflow/airflow --namespace airflow
kubectl expose deployment airflow-webserver --type=LoadBalancer --name=web-lb -n airflow