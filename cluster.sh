# us-central1-a 를 기본 리전으로 선택합니다.
gcloud config set compute/zone us-central1-a

# k8s를 클러스터 이름으로 지정합니다.
CLUSTER_NAME=k8s-ml

# 클러스터를 만들때 
gcloud container clusters create $CLUSTER_NAME \
    --num-nodes=4 \
    --node-labels=role=default \
    --machine-type=n1-standard-2 \
    --node-locations=us-central1-a
