from netmiko import ConnectHandler
from getpass import getpass
from netmiko.ssh_exception import NetmikoTimeoutException
import datetime

username = input("Enter username: ")
password = getpass(prompt = "Enter ssh password: ")
enablePassword = getpass(prompt = "Enter enable password: ")

currentTime = datetime.datetime.now().replace(microsecond=0)

routerList = open("RouterList.txt")
for ip in routerList:
    ip = ip.strip()
    router = {
            "username": username,
            "password": password,
            "ip": ip,
            "device_type": "cisco_ios",
            "secret": enablePassword,
    }

    print("\t==== Connecting to router " + ip  + " ====\n")
    try:
        connection = ConnectHandler(**router)
    except NetmikoTimeoutException:
        print("Can't connect to router " + ip + ". Timed out\n")
        continue
    
    connection.enable()

    print("Saving the configuration to a file...\n")
    
    output = connection.send_command("show run")
    savingFile = open("./Configuration/Router-" + ip + "-" + str(currentTime), "w")
    savingFile.write(output)
    savingFile.close

    print("Saved")

routerList.close
