from netmiko import ConnectHandler
import getpass

username = input("Enter username: ")
password = getpass.getpass(prompt = "Enter ssh password: ")
enablePassword = getpass.getpass(prompt = "Enter enable password: ")

router = {
	"username": username,
	"password": password,
	"ip": "192.168.2.101",
	"device_type": "cisco_ios",
	"secret": enablePassword,
}

connection = ConnectHandler(**router)
connection.enable()
# Use to enter a specific level
#connection.enable(cmd="enable 14") 

commandSet = [ 	"int lo0",
	        "ip address 123.123.123.123 255.255.255.255",
	 	"no shut"]

output = connection.send_config_set(commandSet)
print(output)

#output = connection.send_command("show ip route")
#print(output)

