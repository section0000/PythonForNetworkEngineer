import paramiko
import getpass
import time
import datetime

username = input("Enter username: ")
password = getpass.getpass(prompt = "Enter ssh password: ")
enablePassword = getpass.getpass(prompt = "Enter enable password: ")

currentDateTime = datetime.datetime.now().replace(microsecond = 0) 

ipList = open("IPList.txt")
for ip in ipList:
    ip = ip.strip()
    print("\t==== Connecting to device " + ip + " ====\n")
    
    SSHClient = paramiko.SSHClient()
    SSHClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    SSHClient.connect(ip, username = username, password = password)

    connection = SSHClient.invoke_shell()
    connection.send(b"enable\n")
    connection.send(enablePassword.encode("ascii") + b"\n")
    connection.send(b"terminal length 0\n")
    connection.send(b"show run\n")
    time.sleep(2)

    output = connection.recv(65000)
    
    print(output.decode("ascii"))

    saveFile = open("./Configuration/Router " + ip + " configuration at " + str(currentDateTime), "a") # a: append
    saveFile.write(output.decode("ascii"))
    saveFile.close
    
    connection.close
