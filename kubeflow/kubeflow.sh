# 설치 폴더 이름 정하기
export KF_NAME=my-kubeflow
# 기본 디렉토리 설정
export BASE_DIR=~/Desktop
# 설치 디렉토리 설정
export KF_DIR=${BASE_DIR}/${KF_NAME}
# 폴더 생성후 이동
mkdir -p ${KF_DIR}
cd ${KF_DIR}

# kfctl 다운로드
wget https://github.com/kubeflow/kfctl/releases/download/v1.2.0/kfctl_v1.2.0-0-gbc038f9_darwin.tar.gz
# kfctl 압축 해제
tar -xvf kfctl_v1.2.0-0-gbc038f9_darwin.tar.gz

# 파일 삭제
rm -rf kfctl_v1.2.0-0-gbc038f9_darwin.tar.gz

# url의 yaml파일 지정
export CONFIG_URI="https://raw.githubusercontent.com/kubeflow/manifests/v1.2-branch/kfdef/kfctl_k8s_istio.v1.2.0.yaml"

# 설치 진행
kfctl apply -V -f ${CONFIG_URI}

# 모두 running 될때까지 기다리기
kubectl get all -n kubeflow

# port-forwarding으로 8080포트로 띄우기
kubectl port-forward svc/istio-ingressgateway -n istio-system 8080:80
