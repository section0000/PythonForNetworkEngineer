from csv import reader
from pprint import pprint
import paramiko
import time

configDict = {}
with open("CSVConfigInColumn.csv", "r") as csvFile:
    csvContent = reader(csvFile)
    # Result:
#   ['192.168.2.101', '192.168.2.102', '']
#   ['enable', 'enable', 'enable']
#   ['123', '123', '123']
#   ['terminal len 0', 'terminal len 0', 'terminal len 0']
#   ['conf t', 'conf t', 'conf t']
#   ['int lo0', 'int lo10', 'int e0/2']
#   ['no shut', 'ip address 10.0.0.1 255.255.255.0', 'no shut']
#   ['exit', '', '']
#   ['exit', '', '']
#   ['show ip int brief', 'int lo11', '']
#   ['show run int e0/1', 'ip addres 11.0.0.1 255.255.255.0', '']
#   ['', '', '']
#   ['', 'do show run int lo10', '']
#   ['', 'do show run int lo11', '']

    ips = next(csvContent) # next(): "Return the next row of the reader’s iterable object". In other words, it helps to 
                           #    move to the next row. So in this case, it's used to store the fist row, which is the row
                           #    containing ip address
                           #    For testing:
                           #        next(csvContent)
                           #        for config in csvContent:
                           #            print(config)
                           #    
                           #    ['enable', 'enable', 'enable']
                           #    ['123', '123', '123']
                           #    ['terminal len 0', 'terminal len 0', 'terminal len 0']
                           #    ['conf t', 'conf t', 'conf t']
                           #    ['int lo0', 'int lo10', 'int e0/2']
                           #    ['no shut', 'ip address 10.0.0.1 255.255.255.0', 'no shut']
                           #    ['exit', '', '']
                           #    ['exit', '', '']
                           #    ['show ip int brief', 'int lo11', '']
                           #    ['show run int e0/1', 'ip addres 11.0.0.1 255.255.255.0', '']
                           #    ['', '', '']
                           #    ['', 'do show run int lo10', '']
                           #    ['', 'do show run int lo11', '']

    for config in csvContent:
        for ip in ips:
            if not ip:
                continue
            if ip not in configDict.keys():
                configDict[ip] = []
            n = ips.index(ip)
            if not config[n]:
                continue
            configDict[ip].append(config[n])

#pprint(configDict)

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

