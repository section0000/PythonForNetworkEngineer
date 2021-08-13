from netmiko import ConnectHandler
from getpass import getpass
from netmiko.ssh_exception import NetmikoTimeoutException
from paramiko.ssh_exception import SSHException

username = input("Enter username: ")
enablePassword = getpass(prompt = "Enter enable password: ")

routerListKeyPair = open("RouterList.txt")
for ip in routerListKeyPair:
    ip = ip.strip()
    router = {
            "username": username,
            "ip": ip,
            "device_type": "cisco_ios",
            "secret": enablePassword,
            "use_keys": True,
            "key_file": "/root/PythonForNetworkEngineer/NetworkAutomation/Netmiko/KeyPair/R1-admin",
    }

    print("\t==== Connecting to router " + ip  + " ====\n")
    try:
        connection = ConnectHandler(**router)
    except NetmikoTimeoutException as ex:
        print("Can't connect to router " + ip + ". Timed out\n")
        #print(str(ex))
        continue
    except SSHException:
        print("Authentication failed")
        continue

    connection.enable()

    output = connection.send_config_from_file(config_file="RouterCommand.txt")
    print(output)

    output = connection.send_command_timing("show ip int br")
    print(output)

routerListKeyPair.close
