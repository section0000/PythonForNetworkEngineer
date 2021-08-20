import telnetlib
from getpass import getpass

username = input("Enter username: ")
password = getpass(prompt="Enter remote password: ")
enablePassword = getpass(prompt="Enable enable password: ")

host = "192.168.2.101"
tn = telnetlib.Telnet(host)

tn.read_until(b"Username: ")
tn.write(username.encode("ascii") + b"\n")

if (password != ""):
    tn.read_until(b"Password: ")
    tn.write(password.encode("ascii") + b"\n")

tn.write(b"enable\n")

if (enablePassword != ""):
    tn.read_until(b"Password: ")
    tn.write(enablePassword.encode("ascii") + b"\n")

tn.write(b"terminal length 0\n")
tn.write(b"show version\n")
tn.write(b"exit\n")

output = tn.read_all().decode("ascii")
versionIndex = output.find("Version")
print(output[versionIndex: versionIndex + 18])


