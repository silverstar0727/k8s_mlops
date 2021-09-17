## prometheus 레포 추가
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# 네임스페이스 생성
kubectl create namespace monitoring

# 설치
helm install -n monitoring monitor prometheus-community/kube-prometheus-stack

# prometheus, grafana port-forwarding
kubectl -n monitoring port-forward svc/monitor-kube-prometheus-st-prometheus 9000:9090
kubectl -n monitoring port-forward svc/monitor-grafana 9000:80
