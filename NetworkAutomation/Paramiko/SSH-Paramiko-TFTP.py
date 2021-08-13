import paramiko
import getpass
import time
import datetime

username = input("Enter username: ")
password = getpass.getpass(prompt = "Enter ssh password: ")
enablePassword = getpass.getpass(prompt = "Enter enable password: ")
TFTPServer = input("Enter IP address of the server: ")

currentTime = datetime.datetime.now().replace(microsecond = 0)
formattedTime = "%.2i-%.2i-%i_%.2i-%.2i-%.2i" % (currentTime.day, currentTime.month, currentTime.year, currentTime.hour,
                                                 currentTime.minute, currentTime.second)

ipList = open("IPList.txt")
for ip in ipList:
    ip = ip.strip()
    print("\t==== Connecting to device " + ip + " ====\n")	

    SSHClient = paramiko.SSHClient()
    SSHClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    SSHClient.connect(ip, username = username, password = password)

    connection = SSHClient.invoke_shell()
    connection.send("enable\n")
    connection.send(enablePassword.encode("ascii") + b"\n")
    connection.send("copy startup-config tftp:\n")
    connection.send(TFTPServer + "\n")
    connection.send("Router-" + ip + "-" + str(formattedTime) + "\n")
    time.sleep(2)
    print("Copy successfully!\n")
#   connection.send("terminal length 0\n")
#   connection.send("show run\n")
#   time.sleep(2)

#   output = connection.recv(65000)
#   print(output.decode("ascii"))
    
    connection.close

ipList.close
