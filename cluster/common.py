import time
import settings
import os
os.system("")
from cluster.modules.ssh import ssh_conn


def Setup_All_Nodes(servers):
    print(settings.COLOR["GREEN"], "Step 1:\n##################################################{ Common Setup Started On All Nodes }##################################################\n", settings.COLOR["ENDC"])
    for server in servers:
        id = server["id"]
        host = server["host"]
        username = server["username"]
        password = server["password"]
        sshKey = server["keyFilePath"]
        hostname = server["hostname"]
        role = server["role"]
        master = server["master"]
        print(settings.COLOR["YELLOW"], "========================================>[ {} = {} ]<========================================".format(hostname, host), settings.COLOR["ENDC"])
        
        def Set_Hostname():
            print(settings.COLOR["BLUE"], "\n>>>>>>>>>>>>>>>>>>>>( Set Hostname )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<\n".format(hostname, host), settings.COLOR["ENDC"])
            commandsArr = ["hostnamectl set-hostname {}".format(hostname),"cat /etc/hostname"]
            res = ssh_conn(host, username, password, sshKey, commandsArr)
            print("Hostname set...")
        Set_Hostname()

        def Set_Hosts():
            print(settings.COLOR["BLUE"], "\n>>>>>>>>>>>>>>>>>>>>>( Add Host Entry )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<\n".format(hostname, host), settings.COLOR["ENDC"])
            for node in servers:
                def set_hostEntry():
                    commandsArr = ["cat >>/etc/hosts<<EOF\n{}    {}\nEOF".format(node["host"], node["hostname"]),"cat /etc/hosts"]
                    res = ssh_conn(host, username, password, sshKey, commandsArr)
                    return res
                commands_check = ["cat /etc/hosts | grep '{}    {}'".format(node["host"], node["hostname"])]
                res = ssh_conn(host, username, password, sshKey, commands_check)
                for resData in res:
                    if len(resData) == 0:
                        set_hostEntry()
                        print("Host entery add...")
                    else:
                        print("Host entery already added...")
        Set_Hosts()

        def Firewall_Disable():
            print(settings.COLOR["BLUE"], "\n>>>>>>>>>>>>>>>>>>>>( Firewall Disable )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<\n".format(hostname, host), settings.COLOR["ENDC"])
            commandsArr = ["systemctl disable --now ufw"]
            res = ssh_conn(host, username, password, sshKey, commandsArr)
            print("Stop and Disable firewall")
        Firewall_Disable()

        def Install_Packages():
            print(settings.COLOR["BLUE"], "\n>>>>>>>>>>>>>>>>>>>>( Install Packages )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<\n".format(hostname, host), settings.COLOR["ENDC"])
            commandsArr = ["apt update", "apt-get install -y net-tools htop curl git apt-transport-https ca-certificates wget"]
            res = ssh_conn(host, username, password, sshKey, commandsArr)
            print("Require packages are installed...")
        Install_Packages()

        def Kernal_Modules():
            print(settings.COLOR["BLUE"], "\n>>>>>>>>>>>>>>>>>>>>( Load K8S Network Kernal Modules )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<\n".format(hostname, host), settings.COLOR["ENDC"])
            commandsArr = [
                "cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf\noverlay\nbr_netfilter\nEOF",
                "modprobe overlay", "modprobe br_netfilter", 
                "cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf\nnet.bridge.bridge-nf-call-iptables  = 1\nnet.bridge.bridge-nf-call-ip6tables = 1\nnet.ipv4.ip_forward                 = 1\nEOF", 
                "sysctl --system"
                ]
            res = ssh_conn(host, username, password, sshKey, commandsArr)
            print("Kernal modules Loaded...")
        Kernal_Modules()

        def Reboot_Server():
            print(settings.COLOR["BLUE"], "\n>>>>>>>>>>>>>>>>>>>>( Reboot Server )=>( {} = {} )<<<<<<<<<<<<<<<<<<<<\n".format(hostname, host), settings.COLOR["ENDC"])
            commandsArr = [
                "reboot"
                ]
            res = ssh_conn(host, username, password, sshKey, commandsArr)
            time.sleep(5)
            print("Server Rebooting...\n")
        Reboot_Server()

        def Check_Server_Back_Online():
            online  = False
            counter = 0
            while counter <= 30 :
                counter = counter + 1
                commandsArr = [
                    "hostnamectl hostname"
                    ]
                res = ssh_conn(host, username, password, sshKey, commandsArr)
                for commands in res:
                    for output in commands:
                        if output == hostname:
                            print("{} = {} > Server Back Online Connected...\n".format(hostname, host))
                            online = True
                            break
                if online:
                    break
                else:
                    print(counter, ".: Connecting...")
                    time.sleep(10)
        Check_Server_Back_Online()
    print(settings.COLOR["GREEN"], "\n##################################################{ Common Setup Finished On All Nodes }##################################################\n", settings.COLOR["ENDC"])