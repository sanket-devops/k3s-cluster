import paramiko
import sys
import settings
import os
os.system("")

def ssh_conn(host, username, password, sshKey, commandsArr):
    try:
        hostName = host
        hostUser = username
        hostPass = password
        key_path = os.path.expanduser(sshKey)
        commands = commandsArr
        results = []
        if os.name == "nt":
            os.system("ssh-keygen -R {} > NUL 2>&1".format(hostName))
        elif os.name == "posix":
            os.system("ssh-keygen -R {} > /dev/null 2>&1".format(hostName))
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # client.connect(hostName, username=hostUser, password=hostPass)
        try:
            # First attempt: try with SSH key
            # print("Trying to connect with SSH key...")
            client.connect(hostName, username=hostUser, key_filename=key_path)
        except (paramiko.AuthenticationException, paramiko.SSHException) as e:
            print(f"Key-based authentication failed: {e}")
            # print("Falling back to password authentication...")
            try:
                client.connect(hostName, username=hostUser, password=hostPass)
            except Exception as e:
                print(f"Password authentication failed: {e}")
                exit(1)

        for command in commands:
            print(settings.COLOR["CYAN"], "🚀 " + command, settings.COLOR["ENDC"], "\n")
            temp = []
            ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(command)
            for line in ssh_stdout:
                print(line)
                nRemove = line.strip('\n')
                temp.append(nRemove)
            results.append(temp)
    except:
        print("SSH Connection Timeout...")
    # print("Host: ", hostName,"\nData: ", results)
    return results