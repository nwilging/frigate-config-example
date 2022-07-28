#! /bin/sh

echo "Installing kubectl..."

sudo apt-get update -y && sudo apt-get install -y apt-transport-https ca-certificates curl
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update -y && sudo apt-get install -y kubectl

echo "Kubectl installed!"
echo "Installing Rancher CLI..."

wget -O rancher-cli.tar.gz https://github.com/rancher/cli/releases/download/v2.4.13/rancher-linux-amd64-v2.4.13.tar.gz
tar -xvf rancher-cli.tar.gz

mv rancher-*/rancher ./rancher
chmod +x ./rancher

echo "Rancher CLI installed!"

./rancher login $RANCHER_URL --token $RANCHER_TOKEN --context $RANCHER_CONTEXT
