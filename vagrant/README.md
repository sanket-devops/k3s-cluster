# Create Vagrant VM
### Virtual-Box should be installed (Version 6.1.50).
**vagrant 2.4.6 = Virtualbox 6.1.50** 

## Generate SSH key pair
### Option 1: Recommended (Standard SSH Key Pair)
```shell
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
```
* This generates:
    * Private key: ~/.ssh/id_rsa
    * Public key: ~/.ssh/id_rsa.pub

### Option 2: Using OpenSSL (Not standard for SSH)
**Step 1: Generate Private Key**
```shell
openssl genpkey -algorithm RSA -out C:\Users\sanket\.ssh\id_rsa -pkeyopt rsa_keygen_bits:4096
```

**Step 2: Extract Public Key (in PEM format)**
```shell
openssl rsa -in C:\Users\sanket\.ssh\id_rsa -pubout -out C:\Users\sanket\.ssh\id_rsa_pub.pem
```
⚠️ Note: This will not be in the OpenSSH format (id_rsa.pub). To convert it:

**Step 3: Convert to OpenSSH Format**
```shell
ssh-keygen -i -m PKCS8 -f C:\Users\sanket\.ssh\id_rsa_pub.pem > C:\Users\sanket\.ssh\id_rsa.pub
```



**1. Remove the broken box:**
```shell
vagrant box remove ubuntu/jammy64
```
**2. You can specify --provider virtualbox if needed:**
```shell
vagrant box add ubuntu/jammy64 --provider virtualbox
```
**3. Try vagrant up again::**
```shell
# Up Vagrant VM's 
vagrant up --provider=virtualbox
# vagrant up --provider=libvirt

# Destroy Vagrant VM's
vagrant destroy
```
