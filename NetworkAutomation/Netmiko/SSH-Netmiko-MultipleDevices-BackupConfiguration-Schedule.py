from netmiko import ConnectHandler
from getpass import getpass
from netmiko.ssh_exception import NetmikoTimeoutException
import datetime
import time
import schedule

currentTime = datetime.datetime.now().replace(microsecond=0)

def backup():	
    routerList = open("RouterList.txt")
    for ip in routerList:
        ip = ip.strip()
        router = {
                "username": "admin",
                "password": "admin",
                "ip": ip,
                "device_type": "cisco_ios",
                "secret": "123",
        }

        print("\t==== Connecting to router " + ip  + " ====\n")
        try:
                connection = ConnectHandler(**router)
        except NetmikoTimeoutException:
                print("Can't connect to router " + ip + ". Timed out\n")
                continue
        
        connection.enable()

        print(str(currentTime) + "- Saving the configuration to a file...\n")
        
        output = connection.send_command("show run")
        savingFile = open("./Configuration/Router-" + ip + "-" + str(currentTime), "w")
        savingFile.write(output)
        savingFile.close

        print("Saved")

    routerList.close

schedule.every(1).minute.at(":00").do(backup)
while True:
    schedule.run_pending()
    time.sleep(1)
