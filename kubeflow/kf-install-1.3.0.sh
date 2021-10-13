# create working directory
mkdir ~/Desktop/kubeflow-1.3.0
cd ~/Desktop/kubeflow-1.3.0

# download kustomize version 3.2.0
# don't use kustomize version 4.4.x
# https://github.com/kubeflow/manifests#prerequisites
wget https://github.com/kubernetes-sigs/kustomize/releases/download/v3.2.0/kustomize_3.2.0_darwin_amd64

# chmod and move directory
chmod u+x kustomize_3.2.0_darwin_amd64
sudo mv kustomize_3.2.0_darwin_amd64 /usr/local/bin/kustomize

# git clone manifests
# can cutomize components or install individual components
# https://github.com/kubeflow/manifests#Kubeflow-20components-20versions
git clone https://github.com/kubeflow/manifests.git
cd manifests

# install all components
while ! kustomize build example | kubectl apply -f -; do echo "Retrying to apply resources"; sleep 10; done

# port forwarding
kubectl port-forward svc/istio-ingressgateway -n istio-system 8080:80

#kubectl expose deploy istio-ingressgateway --type=LoadBalancer --name=web-lb -n istio-system

## ===== default id and passwords
# id: user@example.com
# pwd: 12341234