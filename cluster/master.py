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
        sshKey = None
        for path in server["keyFilePaths"]:
            expanded = os.path.expanduser(path)
            if os.path.exists(expanded):
                sshKey = expanded
                break  # found the first usable key
        if not sshKey:
            raise FileNotFoundError(
                f"No valid SSH key found in {server['keyFilePaths']}"
            )
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

                cilium_script = f"""
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
CLI_ARCH=amd64
if [ "$(uname -m)" = "aarch64" ]; then CLI_ARCH=arm64; fi

curl -L --fail --remote-name-all https://github.com/cilium/cilium-cli/releases/download/${{CILIUM_CLI_VERSION}}/cilium-linux-${{CLI_ARCH}}.tar.gz{{,.sha256sum}}

sha256sum --check cilium-linux-${{CLI_ARCH}}.tar.gz.sha256sum

sudo tar xzvfC cilium-linux-${{CLI_ARCH}}.tar.gz /usr/local/bin

rm cilium-linux-${{CLI_ARCH}}.tar.gz{{,.sha256sum}}

cilium install --version {settings.cilium_version} --set ipam.operator.clusterPoolIPv4PodCIDRList="{{{settings.network_cidr}}}"
"""
                res = ssh_conn(host, username, password, sshKey, [cilium_script])

                # for commands in res:
                #     for output in commands:
                #         print(output)
                # time.sleep(60)
                print("\nCNI Installed...")
            Install_CNI()

    print(settings.COLOR["GREEN"], "\n##################################################{ Cluster Setup Finished On Master Node }##################################################\n", settings.COLOR["ENDC"])