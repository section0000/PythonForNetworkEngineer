import paramiko
import time
from getpass import getpass

ip = input("Enter IP: ")
username = input("Enter username: ")
password = input("Enter password: ")

session = paramiko.SSHClient() # Create an SSH client

# Ignore server's certificate. In other words, allow the Python script to SSH to a remote server with unknown SSH keys.
# Not recommended to use in reality
session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

session.connect(ip,
                port=22,
                username=username,
                password=password,
                look_for_keys=False
               )

access = session.invoke_shell() # Send shell commands to the device
access.send(b"enable\n")
time.sleep(1)
access.send(b"123\n")
time.sleep(1)
access.send(b"terminal length 0\n")
access.send(b"show run\n")
time.sleep(3)
output = access.recv(65000) # Define how many words in the output that this session can receive
print(output.decode("ascii"))

session.close
