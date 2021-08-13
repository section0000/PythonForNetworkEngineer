from netmiko import ConnectHandler
from getpass import getpass
from netmiko.ssh_exception import NetmikoTimeoutException

username = input("Enter username: ")
password = getpass(prompt = "Enter ssh password: ")
enablePassword = getpass(prompt = "Enter enable password: ")

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

    # Approach 1: Use a variable to store configuration getting from file
    with open("RouterCommand.txt") as commandSet:
        configuration = commandSet.read().splitlines()
    output = connection.send_config_set(configuration)
    print(output)

    # Approach 2: Use configuration from file directly
    #output = connection.send_config_from_file(config_file="RouterCommand.txt")
    #print(output)

    print("Saving the configuration...")
    output = connection.save_config()
    print(output)

    output = connection.send_command_timing("show ip int br")
    print(output)

routerList.close()

switchList = open("SwitchList.txt")
for ip in switchList:
    ip = ip.strip()
    switch = {
            "username": username,
            "password": password,
            "ip": ip,
            "device_type": "cisco_ios",
            "secret": enablePassword,
    }

    print("\t==== Connecting to switch " + ip  + " ====\n")
    try:
        connection = ConnectHandler(**switch)
    except NetmikoTimeoutException:
        print("Can't connect to switch " + ip + ". Timed out\n")
        continue
    
    connection.enable()

    output = connection.send_config_from_file(config_file="SwitchCommand.txt")
    print(output)

    print("Saving the configuration...")
    output = connection.save_config()
    print(output)

    output = connection.send_command_timing("show ip route")
    print(output)

switchList.close
