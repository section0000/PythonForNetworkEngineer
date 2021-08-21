import paramiko
import time
from getpass import getpass

host = "192.168.2.101"
username = input("Enter username: ")
password = getpass("Enter password: ")
enablePassword = getpass("Enter enable password: ")

session = paramiko.SSHClient()
session.load_system_host_keys()

#keyPass = getpass("Enter private key password: ")
#keyFile = paramiko.RSAKey.from_private_key_file("/root/.ssh/php22800_id_rsa")
#keyFile = paramiko.RSAKey.from_private_key_file("/root/.ssh/php22800_passphrase_id_rsa", keyPass)
session.connect(hostname=host,
                username=username,
                password=password,
                #pkey=keyFile,
                look_for_keys=False
               )

access = session.invoke_shell()
access.send(b"enable\n")
time.sleep(0.5)
access.send(enablePassword.encode("ascii") + b"\n")
access.send(b"terminal length 0\n")
time.sleep(0.5)
access.send(b"show version\n")
time.sleep(0.5)
output = access.recv(65000)
print(output.decode("ascii"))

"""
# Not work. It arises an error:
#========================= Executing command: show version =========================
#Secsh channel 1 open FAILED: : Resource shortage
#Traceback (most recent call last):
#  File "SSH-Paramiko-HostKeyPolicy-Cisco.py", line 42, in <module>
#    stdin, stdout, stderr = session.exec_command(command)
#  File "/usr/local/lib/python3.6/site-packages/paramiko/client.py", line 508, in exec_command
#    chan = self._transport.open_session(timeout=timeout)
#  File "/usr/local/lib/python3.6/site-packages/paramiko/transport.py", line 879, in open_session
#    timeout=timeout,
#  File "/usr/local/lib/python3.6/site-packages/paramiko/transport.py", line 1017, in open_channel
#    raise e
#paramiko.ssh_exception.ChannelException: ChannelException(4, 'Resource shortage')

commands = ["show version"]

for command in commands:
    print("="*25 + " Executing command: " + command + " " + "="*25)
    stdin, stdout, stderr = session.exec_command(command)
    time.sleep(.5)
    print(stdout.read().decode())
    error = stderr.read().decode()
    if error:
        print(error)
"""

session.close()
