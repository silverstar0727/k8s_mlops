# gcloud container clusters get-credentials k8s-ml --zone us-central1-a --project k8s-ml

# 모든 컴포넌트를 업데이트 합니다.
# gcloud components update

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

## kubectl minio 설치
wget https://github.com/minio/operator/releases/download/v4.2.2/kubectl-minio_4.2.2_linux_amd64 -O kubectl-minio
chmod +x kubectl-minio
sudo mv kubectl-minio /usr/local/bin/

# kubectl minio version
kubectl minio init
# kubectl minio proxy -n minio-operator





"""
gcloud container node-pools create train \
    --cluster $CLUSTER_NAME \
    --node-labels=role=train \
    --enable-autoscaling \
    --min-nodes=1 \
    --num-nodes=1 \
    --max-nodes=2 \
    --machine-type=n1-standard-2
"""


# 클러스터 확인
kubectl get node -L role

# RBAC setting - 해야하는지 잘 모르겟음 일단 스킵
cat <<EOF | kubectl create -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: default-admin
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: default
  namespace: kube-system
EOF

# Create Cloud FileStore
gcloud filestore instances create nfs-storage \
    --project=$DEVSHELL_PROJECT_ID \
    --file-share=name="vol",capacity=1TB \
    --zone=us-central1-a \
    --network=name="default",reserved-ip-range="10.0.0.0/29"

## filestore 삭제
# gcloud filestore instances delete create nfs-storage --zone=us-central1-a

# helm 
## argo workflow: Data pipeline & ML workflow를 실행 시켜줄 wf engine입니다.
## nfs-client-provisioner: NAS 서버(EFS)와 연결 시켜주는 Storage Provisioner입니다.
## minio: NAS 서버를 웹으로 통해 볼 수 있게 minio UI를 사용합니다.
## cluster-autoscaler: GCP 자체적으로 autoscale을 지원합니다. 단점은 세부적인 option 설정이 불가능합니다.
## metrics-server: GKE를 생성할때 metrics-server 설치 옵션을 넣으주면 자동으로 설치되어서 나옵니다.

helm repo add stable https://charts.helm.sh/stable
helm repo update

# nfs-server-provisioner
kubectl create namespace storage

helm install nfs stable/nfs-server-provisioner \
    --set persistence.enabled=true \
    --set persistence.size=10Gi \
    --version 1.1.1 \
    --namespace storage

# kubectl get pod -n storage
# kubectl get statefulset -n storage
# kubectl get svc -n storage
# kubectl get sc -n storage












"""
# helm minio operator 추가 operator -> blog로 수동 minio 설치
helm repo add minio https://operator.min.io/
helm repo update

# 설치
helm fetch --untar minio/minio-operator
# 수정 후 실행. 개수(storage class)
helm install --namespace minio-operator --create-namespace minio-op ./minio-operator

# 키 받기
kubectl get secret $(kubectl get serviceaccount console-sa --namespace minio-operator -o jsonpath="{.secrets[0].name}") \
  --namespace minio-operator -o jsonpath="{.data.token}" | base64 --decode
# 포트포워딩
kubectl --namespace minio-operator port-forward svc/console 9090:9090

##### custom 안하는 다른설치방법
helm install --namespace minio-operator --create-namespace --generate-name minio/minio-operator
##### 또다른 설치... https://blog.min.io/object_storage_as_a_service_on_minio/
##### or  https://min.io/download#/kubernetes



## minio 최신버전으로 한번 해보기
helm fetch --untar stable/minio --version 5.0.30


## ==== value를 수정한 뒤 실행해주세요.
helm install minio ./minio --namespace storage
kubectl get pod -n storage
kubectl get pv -n storage
kubectl get pvc -n storage

#export INGRESS_IP=$(kubectl get svc -n storage minio -ojsonpath="{.status.loadBalancer.ingress[0].ip}")
#echo $INGRESS_IP

export POD_NAME=$(kubectl get pods --namespace storage -l "release=minio" -o jsonpath="{.items[0].metadata.name}")
kubectl port-forward $POD_NAME 9000 --namespace storage

"""

"""
kubectl delete -f k8s_mlops/storage/minio/minio-standalone-storageclass.yaml
kubectl delete -f k8s_mlops/storage/minio/minio-standalone-pv.yaml
kubectl delete -f k8s_mlops/storage/minio/minio-standalone-pvc.yaml
kubectl delete -f k8s_mlops/storage/minio/minio-standalone-deployment.yaml
kubectl delete -f k8s_mlops/storage/minio/minio-standalone-service.yaml
"""
