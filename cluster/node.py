import json
import time
import settings
import os
os.system("")
from cluster.modules.ssh import ssh_conn

def Join_Nodes(servers):
    print(settings.COLOR["GREEN"], "Step 3:\n##################################################{ Join Worker Nodes With The Cluster }##################################################\n", settings.COLOR["ENDC"])
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
        if not master :
            print(settings.COLOR["YELLOW"], "========================================>[ {} = {} ]<========================================".format(hostname, host), settings.COLOR["ENDC"])

            def Join_Node():
                print(settings.COLOR["BLUE"], "\n>>>>>>>>>>>>>>>>>>>>( Join This Node To The Cluster )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<\n".format(hostname, host), settings.COLOR["ENDC"])
                commandsArr = ['{} INSTALL_K3S_EXEC="--node-ip={}" sh -'.format(settings.Node_Join, host)]
                res = ssh_conn(host, username, password, sshKey, commandsArr)
                # for commands in res:
                #     for output in commands:
                #         print(output)
                time.sleep(30)
                print("\nNode Join Proccess Completed...\n")
            Join_Node()

            def Local_Registry():
                print(settings.COLOR["BLUE"], "\n>>>>>>>>>>>>>>>>>>>>( Configure K3s Registry )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<\n".format(hostname, host), settings.COLOR["ENDC"])
                commandsArr = ["mkdir -p /etc/rancher/k3s",
                    "echo '{}' > /etc/rancher/k3s/registries.yaml".format(settings.K3s_Registry.replace("localhost", server["local-registry"])),
                    "systemctl restart k3s-agent",
                    ]
                res = ssh_conn(host, username, password, sshKey, commandsArr)
                print("K3s Registry Configured...")
            Local_Registry()