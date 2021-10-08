FROM apache/airflow:2.1.0

COPY requirements.txt ./
COPY ./dags/ \${AIRFLOW_HOME}/dags/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# image name
## silverstar456/k8s_mlops:airflow-custom