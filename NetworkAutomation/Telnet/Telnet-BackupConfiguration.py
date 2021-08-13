import telnetlib
from getpass import getpass

host = "192.168.2.101"
username = input("Enter username: ")
password = getpass(prompt="Enter password: ")
enablePassword = getpass(prompt="Enter enable password: ")

tn = telnetlib.Telnet(host)

if (password != ""):
    tn.read_until(b"Password: ")
    tn.write(password.encode("ascii") + b"\n")

tn.write(b"enable\n")

if (enablePassword != ""):
    tn.read_until(b"Password: ")
    tn.write(enablePassword.encode("ascii") + b"\n")

tn.write(b"terminal length 0\n")
tn.write(b"show run\n")
tn.write(b"exit\n")

output = tn.read_all().decode("ascii")
print(output)

backup = open("Router" + host, "w")
backup.write(output)
backup.close()


