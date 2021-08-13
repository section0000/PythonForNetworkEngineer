import paramiko
import getpass
import time
import datetime
import schedule

currentDateTime = datetime.datetime.now().replace(microsecond = 0) 

def backup():
    ipList = open("IPList.txt")
    for ip in ipList:
        ip = ip.strip()
        print("\t==== Connecting to device " + ip + " ====\n")
        
        SSHClient = paramiko.SSHClient()
        SSHClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        SSHClient.connect(ip, username="admin", password="admin")

        connection = SSHClient.invoke_shell()
        connection.send(b"enable\n")
        connection.send(b"123\n")
        connection.send(b"terminal length 0\n")
        connection.send(b"show run\n")
        time.sleep(2)

        output = connection.recv(65000)		
        print(output.decode("ascii"))

        print(str(currentDateTime) + "- Saving the configuration...\n")

        saveFile = open("./Configuration/Router " + ip + " configuration at " + str(currentDateTime), "a") # a: append
        saveFile.write(output.decode("ascii"))
        saveFile.close

        time.sleep(1)
        print("Saved\n")
        
        connection.close

    ipList.close

schedule.every(1).minute.at(":00").do(backup)
while True:
    schedule.run_pending()
    time.sleep(1)
