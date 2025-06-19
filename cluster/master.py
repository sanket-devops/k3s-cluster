import time
import settings
import os
os.system("")
from cluster.modules.ssh import ssh_conn
from cluster.modules.sftp import sftp_conn

def Setup_Cluster(servers):
    print(settings.COLOR["GREEN"], "Step 2:\n##################################################{ Cluster Setup Started On Master Node }##################################################\n", settings.COLOR["ENDC"])
    for server in servers:
        id = server["id"]
        host = server["host"]
        username = server["username"]
        password = server["password"]
        sshKey = server["keyFilePath"]
        hostname = server["hostname"]
        role = server["role"]
        master = server["master"]
        if master:
            print(settings.COLOR["YELLOW"], "========================================>[ {} = {} ]<========================================".format(hostname, host), settings.COLOR["ENDC"])

            def K3s_Cluster():
                print(settings.COLOR["BLUE"], "\n++++++++++++++++++++( Initialize K3s Cluster )++++++++++++++++++++\n", settings.COLOR["ENDC"])
                commandsArr = ['curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION={} INSTALL_K3S_EXEC="--node-ip={} {}" sh -s - server'.format(settings.k3s_version, host, settings.k3s_arg), "echo 'KUBECONFIG=/etc/rancher/k3s/k3s.yaml' >> /etc/environment"]
                res = ssh_conn(host, username, password, sshKey, commandsArr)
                # for commands in res:
                #     for output in commands:
                #         print(output)
                time.sleep(30)
                print("\nK3s Cluster Initialization Completed...")
            K3s_Cluster()

            def Node_Join_Command():
                print(settings.COLOR["BLUE"], "\n++++++++++++++++++++( Generate Node Join Command )++++++++++++++++++++\n", settings.COLOR["ENDC"])
                commandsArr = ["cat /var/lib/rancher/k3s/server/node-token"]
                res = ssh_conn(host, username, password, sshKey, commandsArr)
                for commands in res:
                    for output in commands:
                        settings.Node_Join = "curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION={} K3S_URL=https://{}:6443 K3S_TOKEN={}".format(settings.k3s_version, host, output)
                        # print(output)
                print("\nNode Join Command Generated...")
            Node_Join_Command()

            def Local_Registry():
                print(settings.COLOR["BLUE"], "\n>>>>>>>>>>>>>>>>>>>>( Configure K3s Registry )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<\n".format(hostname, host), settings.COLOR["ENDC"])
                commandsArr = ["mkdir -p /etc/rancher/k3s",
                    "echo '{}' > /etc/rancher/k3s/registries.yaml".format(settings.K3s_Registry.replace("localhost", server["local-registry"])),
                    "systemctl restart k3s",
                    ]
                res = ssh_conn(host, username, password, sshKey, commandsArr)
                print("K3s Registry Configured...")
            Local_Registry()

            def Install_CNI():
                print(settings.COLOR["BLUE"], "\n++++++++++++++++++++( Initialize CNI )++++++++++++++++++++\n", settings.COLOR["ENDC"])
                # Flannel network plugin
                # commandsArr = ["kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml"]
                # res = ssh_conn(host, username, password, commandsArr)
                
                # Calico as a network plugin
                commandsArr1 = ["mkdir -p /etc/kubernetes/network/calico"]
                res = ssh_conn(host, username, password, sshKey, commandsArr1)

                # Upload tigera-operator.yaml file to remote server
                # sftp_conn(host, username, password, sshKey, settings.tigera_operator_local_path, settings.tigera_operator_remote_path, "upload")

                commandsArr2 = [
                    "echo '{}' > /etc/kubernetes/network/calico/custom-resources.yaml".format(settings.custom_resources.replace("192.168.0.0/16", settings.network_cidr)),
                    "kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml create -f https://raw.githubusercontent.com/projectcalico/calico/{}/manifests/operator-crds.yaml".format(settings.calico_version),
                    "kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml create -f https://raw.githubusercontent.com/projectcalico/calico/{}/manifests/tigera-operator.yaml".format(settings.calico_version),
                    "kubectl --kubeconfig /etc/rancher/k3s/k3s.yaml create -f /etc/kubernetes/network/calico/custom-resources.yaml"
                    ]
                res = ssh_conn(host, username, password, sshKey, commandsArr2)

                # for commands in res:
                #     for output in commands:
                #         print(output)
                time.sleep(60)
                print("\nCNI Installed...")
            Install_CNI()

    print(settings.COLOR["GREEN"], "\n##################################################{ Cluster Setup Finished On Master Node }##################################################\n", settings.COLOR["ENDC"])