import paramiko
import time
from getpass import getpass

host = "172.16.1.2"
username = input("Enter username (root): ") or "root"
#password = getpass(prompt = "Enter password: ")

session = paramiko.SSHClient()
#session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
session.load_system_host_keys() # You don't need to specify a file containing the host key
#session.load_host_keys("/root/.ssh/known_hosts") # You need to specify a file containing the host key
#session.set_missing_host_key_policy(paramiko.RejectPolicy()) # Deny connection if host key is not found in known_hosts
#session.set_missing_host_key_policy(paramiko.WarningPolicy()) # Connect to host and raise a warning if host key is not 
                                                              #   found in known_hosts


keyPass = getpass("Enter private key password: ")
#keyFile = paramiko.RSAKey.from_private_key_file("/root/.ssh/php22800_id_rsa")
keyFile = paramiko.RSAKey.from_private_key_file("/root/.ssh/php22800_passphrase_id_rsa", keyPass)
session.connect(hostname=host,
                username=username,
                #password=password,
                pkey=keyFile, # Use pkey when you want to manually specify your key. Otherwise, you can let your system 
                              #automatically search your key in ~/.ssh/(it's done by default with look_for_keys parameter)
               )

commands = ["ls", "hostname", "netstat -nltp", "abbcacwa"]

for command in commands:
    print("="*25 + " Executing command: " + command + " " + "="*25)
    stdin, stdout, stderr = session.exec_command(command)
    time.sleep(.5)
    print(stdout.read().decode())
    error = stderr.read().decode()
    if error:
        print(error)

session.close()
