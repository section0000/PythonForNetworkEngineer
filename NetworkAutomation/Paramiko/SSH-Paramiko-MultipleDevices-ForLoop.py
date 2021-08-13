import paramiko
import getpass
import time

username = input("Enter username: ")
password = getpass.getpass(prompt = "Enter ssh password: ")
enablePassword = getpass.getpass(prompt = "Enter enable password: ")

for i in range (101,103):
    ip = "192.168.2." + str(i)
    print("Connecting to device " + ip)
    
    SSHClient = paramiko.SSHClient()
    SSHClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    SSHClient.connect(ip, username = username, password = password)

    connection = SSHClient.invoke_shell()
    connection.send(b"enable\n")
    connection.send(enablePassword.encode("ascii") + b"\n")
    connection.send(b"terminal length 0\n")
    #connection.send(b"show ip route\n")
    time.sleep(3)
    connection.send(b"conf t\n")
    for x in range (1,11):
            connection.send("int lo" + str(x) + "\n")
            connection.send("ip address 192.168.1." + str(x) + " 255.255.255.255\n")
    connection.send(b"end\n")
    connection.send(b"show ip int br\n")
    time.sleep(3)

    output = connection.recv(65000)

    print(output.decode("ascii"))
