from csv import DictReader
from pprint import pprint
import paramiko
import time

configDict = {}
with open("CSVConfigInColumn.csv", "r") as csvFile:
    csvContent = DictReader(csvFile)
    # Result:
#    OrderedDict([('192.168.2.101', 'enable'), ('192.168.2.102', 'enable'), ('', 'enable')])
#    OrderedDict([('192.168.2.101', '123'), ('192.168.2.102', '123'), ('', '123')])
#    OrderedDict([('192.168.2.101', 'terminal len 0'), ('192.168.2.102', 'terminal len 0'), ('', 'terminal len 0')])
#    OrderedDict([('192.168.2.101', 'conf t'), ('192.168.2.102', 'conf t'), ('', 'conf t')])
#    OrderedDict([('192.168.2.101', 'int lo0'), ('192.168.2.102', 'int lo10'), ('', 'int e0/2')])
#    OrderedDict([('192.168.2.101', 'no shut'), ('192.168.2.102', 'ip address 10.0.0.1 255.255.255.0'), ('', 'no shut')])
#    OrderedDict([('192.168.2.101', 'exit'), ('192.168.2.102', ''), ('', '')])
#    OrderedDict([('192.168.2.101', 'exit'), ('192.168.2.102', ''), ('', '')])
#    OrderedDict([('192.168.2.101', 'show ip int brief'), ('192.168.2.102', 'int lo11'), ('', '')])
#    OrderedDict([('192.168.2.101', 'show run int e0/1'), ('192.168.2.102', 'ip addres 11.0.0.1 255.255.255.0'), ('', '')])
#    OrderedDict([('192.168.2.101', ''), ('192.168.2.102', ''), ('', '')])
#    OrderedDict([('192.168.2.101', ''), ('192.168.2.102', 'do show run int lo10'), ('', '')])
#    OrderedDict([('192.168.2.101', ''), ('192.168.2.102', 'do show run int lo11'), ('', '')])


    columnNames = csvContent.fieldnames # "If not passed as a parameter when creating the object, this attribute is 
                                #    initialized  upon first access or when the first record is read from the file."
                                # Result:
                                # ['192.168.2.101', '192.168.2.102', '']
    #print(ips)
    for row in csvContent:
        for columnName in columnNames:
            if not columnName: # Ignore the blank column name
                continue
            if not row[columnName]: # Ignore the blank configuration. Ex: ('192.168.2.101', '')
                continue
            if columnName not in configDict.keys():
                configDict[columnName] = []
            configDict[columnName].append(row[columnName])

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
