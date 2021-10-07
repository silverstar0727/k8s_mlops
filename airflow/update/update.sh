# get values.yaml
helm show values apache-airflow/airflow > values.yaml
# update chart
helm upgrade --install airflow apache-airflow/airflow -n airflow -f values.yaml --debug 
# load docker image
kind load docker-image silverstar456/k8s_mlops:airflow-custom