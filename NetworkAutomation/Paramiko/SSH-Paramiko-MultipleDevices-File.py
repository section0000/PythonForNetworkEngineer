import paramiko
import getpass
import time

username = input("Enter username: ")
password = getpass.getpass(prompt = "Enter ssh password: ")
enablePassword = getpass.getpass(prompt = "Enter enable password: ")

ipList = open("IPList.txt")
for ip in ipList:
    print("\t==== Connecting to device " + ip.strip() + " ====\n")
    
    SSHClient = paramiko.SSHClient()
    SSHClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    SSHClient.connect(ip.strip(), username = username, password = password)

    connection = SSHClient.invoke_shell()
    connection.send(b"enable\n")
    connection.send(enablePassword.encode("ascii") + b"\n")
    command = open("Command.txt")
    for commandLine in command:
            time.sleep(1)
            connection.send(str(commandLine))

    time.sleep(3)
    output = connection.recv(65000)

    print(output.decode("ascii"))

    connection.close
