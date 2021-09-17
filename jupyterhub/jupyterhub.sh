helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm repo update

RELEASE=jupyterhub
NAMESPACE=jupyterhub

kubectl create ns $NAMESPACE

helm upgrade --install $RELEASE jupyterhub/jupyterhub \
  --namespace $NAMESPACE  \
  --version=1.1.3 \
  --values config.yaml

kubectl --namespace=jupyterhub get svc