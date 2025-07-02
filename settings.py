global servers
servers = [
    {
        "id": 1,
        "host": "10.0.2.101",
        "username": "root",
        "password": "admin",
        "keyFilePaths": [
            "C:/Users/sanket/.ssh/id_rsa",
            "~/.ssh/id_rsa"
        ],
        "hostname": "master",
        "local-registry": "10.0.2.101",
        "role": "master",
        "master": True
    },
    {
        "id": 2,
        "host": "10.0.2.102",
        "username": "root",
        "password": "admin",
        "keyFilePaths": [
            "C:/Users/sanket/.ssh/id_rsa",
            "~/.ssh/id_rsa"
        ],
        "hostname": "node1",
        "local-registry": "10.0.2.101",
        "role": "worker",
        "master": False
    },
    {
        "id": 3,
        "host": "10.0.2.103",
        "username": "root",
        "password": "admin",
        "keyFilePaths": [
            "C:/Users/sanket/.ssh/id_rsa",
            "~/.ssh/id_rsa"
        ],
        "hostname": "node2",
        "local-registry": "10.0.2.101",
        "role": "worker",
        "master": False
    }
]

# K8S Network Configuration
global network_cidr
# Flannel network cidr
# network_cidr = "10.244.0.0/16"
# Calico network cidr 
network_cidr = "192.168.0.0/16"
# Cilium network cidr
# network_cidr = "10.0.0.0/16"

global K3s_Registry
K3s_Registry = open("./rancher/k3s/registries.yaml").read()
global kubernetes
k3s_version = "v1.32.5+k3s1"
global k3s_arg
k3s_arg = "--flannel-backend=none --cluster-cidr={} --disable-network-policy --disable=traefik --write-kubeconfig-mode=644".format(network_cidr)
global Node_Join

# Cilium
# https://docs.cilium.io/en/stable/gettingstarted/k8s-install-default/
cilium_version = "1.17.5"


global COLOR
COLOR = {
    "HEADER": "\033[95m",
    "BLUE": "\033[1;34m",
    "GREEN": "\033[1;32m",
    "RED": "\033[1;31m",
    "YELLOW": "\033[1;33m",
    "CYAN": "\033[1;36m",
    "ENDC": "\033[0m",
}
