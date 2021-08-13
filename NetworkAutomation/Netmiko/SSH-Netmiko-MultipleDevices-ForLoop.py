from netmiko import ConnectHandler
from getpass import getpass

username = input("Enter username: ")
password = getpass(prompt = "Enter ssh password: ")
enablePassword = getpass(prompt = "Enter enable password: ")

router101 = {
	"username": username,
	"password": password,
	"ip": "192.168.2.101",
	"device_type": "cisco_ios",
	"secret": enablePassword,
}

router102 = {
	"username": username,
	"password": password,
	"ip": "192.168.2.102",
	"device_type": "cisco_ios",
	"secret": enablePassword,
}

deviceList = [router101, router102]

for device in deviceList:
	print("\t==== Connecting to device " + device["ip"] + " ====\n")
	
	connection = ConnectHandler(**device)
	
	commandSet = [  "int lo77",
			"ip address 77.77.77.77 255.255.255.255",
			"no shut",
			"exit"]

	output = connection.send_config_set(commandSet)
	print(output)

	output = connection.send_command_timing("show ip int br")
	print(output)


