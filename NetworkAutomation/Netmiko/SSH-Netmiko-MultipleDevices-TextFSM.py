from netmiko import ConnectHandler
from getpass import getpass
from netmiko.ssh_exception import NetmikoTimeoutException
from operator import itemgetter

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

#	output = connection.send_config_from_file(config_file="RouterCommand.txt")
#	print(output)

	output = connection.send_command_timing("show ip int br", use_textfsm=True)
	#print(output)

	# Get specific information
	#    Method 1: a[index][key]
	interfaceName = output[1]["intf"]
	interfaceStatus = output[1]["status"]
	print("Interface " + interfaceName + ", status: " + interfaceStatus)

	#    Method 2: use "itemgetter" from "operator". Example:
	interface0 = output[1]
	getIntf = itemgetter("intf")
	getStatus = itemgetter("status")
	name = getIntf(interface0)
	status = getStatus(interface0)
	print("(Itemgetter) Interface " + name + ", status: " + status) 
	
	totalNumber = len(output)
	print("Total number of interfaces of router " + ip + " is " + str(totalNumber) + "\n")

	for i in range(0, totalNumber):
		if (output[i]["status"] == "up"):
			print("Interface " + output[i]["intf"] + " is up\n")
		else:
			print("Interface " + output[i]["intf"] + " is down\n")
			if ((output[i]["intf"] == "Serial1/0") and (output[i]["status"] == "administratively down")):
				configSet = [   "int se1/1",
						"no shut"]	
				command = connection.send_config_set(configSet)
				print(command)

routerList.close

