
# kubectl minio-operator를 다운받습니다.
wget https://github.com/minio/operator/releases/download/v4.2.2/kubectl-minio_4.2.2_linux_amd64 -O kubectl-minio
chmod +x kubectl-minio

# bin 디렉토리로 옯겨줍니다.
sudo mv kubectl-minio /usr/local/bin/

# minio를 실행합니다.
#kubectl minio version
kubectl minio init
kubectl minio proxy -n minio-operator

