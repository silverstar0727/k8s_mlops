helm repo add minio https://helm.min.io/
helm repo update
helm install --set accessKey=myaccesskey,secretKey=mysecretkey --namespace default --generate-name minio/minio
helm delete my-release