helm repo add minio https://helm.min.io/
helm repo update
helm install --set accessKey=myaccesskey, secretKey=mysecretkey, --namespace minio --generate-name minio/minio 
helm delete my-release


helm install minio-release minio/minio 