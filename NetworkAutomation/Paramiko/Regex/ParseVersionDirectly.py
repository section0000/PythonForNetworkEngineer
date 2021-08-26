import paramiko
import time
import re
import traceback

versionPattern = re.compile(r"Version (\S+)")
modelPattern = re.compile(r"Linux (\S+).+")
serialNumberPattern = re.compile(r"Processor board ID (\S+)")
uptimePattern = re.compile(r"(.+) uptime is (.+)")

def parse_cisco_version(hostname, username, password):
    try:
        print("="*25 + " Connecting to device " + hostname  + " " + "="*25)
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        session.connect(hostname=hostname,
                        username=username,
                        password=password
                       )

        deviceAccess = session.invoke_shell()
        deviceAccess.send(b"enable\n")
        time.sleep(0.5)
        deviceAccess.send(b"123\n")
        time.sleep(0.5)
        deviceAccess.send(b"terminal length 0\n")
        time.sleep(0.5)
        deviceAccess.send(b"show version\n")
        time.sleep(1)
        output = deviceAccess.recv(65000).decode("ascii")
        #print(output)

        versionMatched = versionPattern.search(output)
        print("IOS version".ljust(18) + ": " + versionMatched.group(1))

        modelMatched = modelPattern.search(output)
        print("Model".ljust(18) + ": " + modelMatched.group(1))

        serialNumberMatched = serialNumberPattern.search(output)
        print("Serial number".ljust(18) + ": " + serialNumberMatched.group(1))

        uptimeMatched = uptimePattern.search(output)
        print("Hostname".ljust(18) + ": " + uptimeMatched.group(1))
        print("Uptime".ljust(18) + ": " + uptimeMatched.group(2))

        session.close()
    except paramiko.ssh_exception.AuthenticationException:
        traceback.print_exc()
    except AttributeError:
        traceback.print_exc()
    except:
        traceback.print_exc()


parse_cisco_version("192.168.2.101", "admin", "admin")

