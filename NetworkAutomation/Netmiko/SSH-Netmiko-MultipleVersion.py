from netmiko import ConnectHandler

with open("DeviceList.txt") as f:
    deviceList = f.read().splitlines()

for ip in deviceList:
    ip = ip.strip()
    print("\n========== Connecting to device " + str(ip) + " =========")
    router = {
        "ip": ip,
        "username": "admin",
        "password": "admin",
        "device_type": "cisco_ios",
        "secret": "123",
    }
    try:
        connection = ConnectHandler(**router)
    except Exception as unknownError:
        print("Error: " + str(unknownError))
        continue
    connection.enable()
    
    versionList = ["I86BI_LINUX-ADVENTERPRISEK9-M",
                   "I86BI_LINUXL2-ADVENTERPRISEK9-M",
                   "VIOS-ADVENTERPRISEK9-M"]

    for version in versionList:
        print("Checking for " + version)
        outputVersion = connection.send_command("show version")
        versionFound = outputVersion.find(version)
        if (versionFound > 0):
            print("Version found: " + version)
            break
        else:
            print("Did not find " + version)

    if (version == "I86BI_LINUX-ADVENTERPRISEK9-M"):
        print("Running " + version + " command...")
        output = connection.send_config_from_file("RouterConfiguration.txt")
        print(output)
    elif (version == "I86BI_LINUXL2-ADVENTERPRISEK9-M"):
        print("Running " + version + " command...")
        output = connection.send_config_from_file("SwitchConfiguration.txt")
        print(output)
    else:
        print("Running " + version + " command...")
        output = connection.send_config_from_file("RouterConfiguration.txt")
        print(output)
