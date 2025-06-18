# K8S Cluster Setup

Setup Kubernetes Kubeadm Cluster On Remote Server

## Python3.10 and pip require

> https://www.python.org/downloads/

### Install dependency using Pipfile

```shell
python --version
python -m pip --version

python -m pip install -r ./requirements.txt

# OR

python -m pip install pipenv
pipenv shell

# Install Pipfile dependency
pipenv install
# pipenv install --ignore-pipfile     # Install dependency from Pipfile.lock
```

## Setup root access

### 1. Set root password on all linux servers
```shell script
sudo passwd root
```
### 2. Install Ubuntu OpenSSH Server on all linux servers.
```shell script
sudo apt install -y openssh-client openssh-server
```
### 3. Edit the sshd_config file at location /etc/ssh on all linux servers.
```shell script
sudo nano /etc/ssh/sshd_config
```
> Change below changes
```shell script
PasswordAuthentication yes
PermitRootLogin yes
PubkeyAuthentication yes
```
### 4. Restart the ssh service after change the configuration of all linux servers.
```shell script
sudo systemctl restart sshd.service / sudo systemctl restart ssh
```

## Start Cluster Setup

```shell
python main.py
```
