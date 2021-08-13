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

	print("\n\t==== Connecting to router " + ip  + " ====\n")
	try:
		connection = ConnectHandler(**router)
	except NetmikoTimeoutException:
		print("Can't connect to router " + ip + ". Timed out\n")
		continue
	
	connection.enable()

#	output = connection.send_config_from_file(config_file="RouterCommand.txt")
#	print(output)

	output = connection.send_command_timing("show ip int br", use_textfsm=True)
#	print(output)

	# Add the output to a list
	interfaces = []
	for i in output:
		if (i["status"] == "up"):
			interfaces.append(i["ipaddr"])
	print(interfaces)
	

	print("\nPrint the output by using for loop")
	for i in output:
		if (i["status"] == "up"):
			print(i)

	print("\nPrint the output by using list comprehension")
	listComprehension = [i["intf"] for i in output if i["status"] == "up"]
	print(listComprehension)
	#print([i["intf"] for i in output if i["status"] == "up"])

routerList.close

