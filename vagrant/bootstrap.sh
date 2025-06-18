#!/bin/bash

# Enable ssh password authentication
echo "Enable ssh password authentication"
sed -i 's/.*PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config
sed -i 's/.*PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/.*PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config
# Enable powershell remote session
sed -i '$ a Subsystem powershell /usr/bin/pwsh -sshs -NoLogo' /etc/ssh/sshd_config

# Remove another sshd_config
rm -rf /etc/ssh/sshd_config.d/*

# Restart sshd
systemctl reload sshd
# systemctl restart sshd

# Verify SSH Config
sudo sshd -T | grep -Ei 'passwordauthentication|pubkeyauthentication|permitrootlogin'

# Set Root password
echo "Set root password"
echo -e "admin\nadmin" | passwd root >/dev/null 2>&1
