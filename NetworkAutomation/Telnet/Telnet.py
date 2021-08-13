import telnetlib
import getpass

HOST = "192.168.2.101"
telnetPassword = getpass.getpass(prompt = "Enter your telnet password: ")
enablePassword = getpass.getpass(prompt = "Enter your enable password: ")

tn = telnetlib.Telnet(HOST)

if telnetPassword != "":
	tn.read_until(b"Password: ")
	tn.write(telnetPassword.encode("ascii") + b"\n")

tn.write(b"enable\n")

if enablePassword != "":
	tn.read_until(b"Password: ")
	tn.write(enablePassword.encode("ascii") + b"\n")

tn.write(b"terminal length 0\n")
tn.write(b"show ip int br\n")
tn.write(b"show ip route\n")
#tn.write(b"show run\n")
tn.write(b"exit\n")

print(tn.read_all().decode("ascii"))


