from csv import reader
from pprint import pprint
import paramiko
import time

configDict = {}
with open("CSVConfigInRow.csv", "r") as csvFile:
    csvContent = reader(csvFile)
    # Each result is a list
#    ['192.168.2.101', 'enable', '123', 'terminal len 0', 'conf t', 'int lo0', 'no shut', 'exit', 'exit', 'show ip \
#    int brief', 'show run int e0/1', '', '', '']

    for device in csvContent:
        if not device[0]: #  If the IP of this device is empty (Ex:<No IP here>,enable,123), it's not going to be added 
            continue
        if device[0] not in configDict.keys():
            configDict[device[0]] = []
        # Result:
#        {'192.168.2.101': []}

        n = len(device) # When reading a CSV file, the highest length will be chosen
        # Result:
#        14 (Although the real length of this is 12)
#        14
        for config in range(1, n):
            if not device[config]: # Ignore the blank field. Ex: 192.168.2.101,config t,    ,terminal len 0
                continue
            configDict[device[0]].append(device[config]) # Add config to the device having that ip address

pprint(configDict)

session = paramiko.SSHClient()
session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for ip in configDict.keys():
    try:
        print("="*25 + " Connecting to device " + ip  + " " + "="*25)
        session.connect(hostname=ip,
                        username="admin",
                        password="admin"
                       )

        deviceAccess = session.invoke_shell()
        print("\nExcecuting commands are: " + str(configDict[ip]))
        #print(f"\nExecuting Commands are\n{'~'*22}\n{configDict[ip]}")
        for config in configDict[ip]:
            deviceAccess.send(config + "\n")
            time.sleep(0.5)
            output = deviceAccess.recv(65000)
            print(output.decode("ascii"), end="")
            time.sleep(0.5)
        session.close()
    except Exception as ex:
        #print("Error: " + str(ex))
        traceback.print_exc()
