# get values.yaml
helm show values apache-airflow/airflow > values.yaml
# update chart
helm upgrade --install airflow apache-airflow/airflow -n airflow -f values.yaml --debug 
# load docker image
kind load docker-image silverstar456/k8s_mlops:airflow-custom


# second sol
helm upgrade -n airflow \
  --install airflow apache-airflow/airflow \
  --set images.airflow.repository=silverstar456/k8s_mlops \
  --set images.airflow.tag=airflow-custom \
  --set images.airflow.pullPolicy=Always \
  --debug