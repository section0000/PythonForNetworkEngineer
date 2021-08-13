from simplecrypt import encrypt, decrypt
from pprint import pprint
from netmiko import ConnectHandler
import json
from time import time
import threading

def getDevices(devicesFilename):
    devices = {}
    with open(devicesFilename) as f:
        for line in f: # Read all lines
            deviceInfo = line.strip().split(",")
            device = {"ipaddr": deviceInfo[0],
                      "type": deviceInfo[1],
                      "name": deviceInfo[2]}
            devices[device["ipaddr"]] = device # Add a device read from file to dictionary. Key is "ipaddr"

    print("\n===== Devices =====")
    pprint(devices)

    return devices

def getDevicesCredentials(devicesCredentialsFilename, key):
    print("\nGetting credentials...")
    with open(devicesCredentialsFilename, "rb") as f:
        devicesCredentialsJSON = decrypt(key, f.read())

    devicesCredentialsList = json.loads(devicesCredentialsJSON.decode("utf-8"))
    pprint(devicesCredentialsList)

    print("\n===== Devices Credentials =====")
    # Convert to dictionary by using dictionary comprehension
    devicesCredentials = {device[0]:device for device in devicesCredentialsList}
    pprint(devicesCredentials)

    return devicesCredentials

def configure(device, deviceCredentials):
    if (device["type"] == "junos-srx"):
        deviceType = "juniper"
    elif (device["type"] == "cisc_ios"):
        deviceType = "cisco_ios"
    elif (device["type"] == "cisco_xr"):
        deviceType = "cisco_xr"
    else:
        deviceType = "cisco_ios"

    print("\n===== Connecting to device {0}, username = {1}, password = {2} ===== ".format(device["ipaddr"],\
                                                                                           deviceCredentials[1],\
                                                                                           deviceCredentials[2]))
    connection = ConnectHandler(ip=device["ipaddr"],
                                username=deviceCredentials[1],
                                password=deviceCredentials[2],
                                device_type=deviceType,
                                secret=deviceCredentials[3])

    if (deviceType == "juniper"):
        # Use CLI command to get configuration data from device
        print("==== Getting configuration from device...")
        connection.send_command("configure terminal")
        configData = connection.send_command("show configuration")

    if (deviceType == "cisco_ios"):
        # Use CLI command to get configuration data from device
        print("==== Getting configuration from device...")
        configData = connection.send_command("show run")

    if (deviceType == "cisco_xr"):
        # Use CLI command to get configuration data from device
        print("==== Getting configuration from device...")
        configData = connection.send_command("show configuration running-config")

    # Write out configuration information to file
    configFilename = "Config-" + device["ipaddr"]  # Important - create unique configuration file name

    print("==== Writing configuration: ", configFilename)
    with open(configFilename, "w") as configOut:
        configOut.write(configData)

    connection.disconnect()

    return

# =========================== Main ====================================================
devices = getDevices("DeviceList.csv")
devicesCredentials = getDevicesCredentials("EncryptedDeviceCredentials.csv", "cisco")

startingTime = time() # To see how long it takes

threadsList = []
for ipaddr,device in devices.items():
    print("Creating thread for: ", device)
    threadsList.append(threading.Thread(target=configure, args=(device, devicesCredentials[ipaddr])))

print("\n===== Begin to get config threading ====\n")
for configThread in threadsList:
    configThread.start()

for configThread in threadsList:
    configThread.join()

print ("\n===== End of getting config sequentially, elapsed time = ", time() - startingTime)
