import paramiko
import time
import re
import traceback
from pprint import pprint

hostnamePattern = re.compile(r"hostname (\S+)")
domainNamePattern = re.compile(r"ip domain name (\S+)")
# Note: When you are connecting to device, unlike reading from file, to make regex effective, you need to add "\r" before 
#    any "\n"
netconfPattern = re.compile(r"netconf-yang\r\n")
usernamePattern = re.compile(r"username (\S+) privilege (\d{1,2})")
# This regex is still NOT GOOD because it only matches the interfaces configured with "description"
interfacePattern = re.compile(r"interface (\S+)\r\n.+?\r\n\s?ip address ([\d\.]+) ([\d\.]+)")
# Instead of letting groups be numbered automatically, you assign names for them
interfacePropertyPattern = re.compile(r"interface (?P<name>\S+)\r\n.+?\r\n\s?ip address (?P<ip>[\d\.]+) (?P<netmask>[\d\.]+)")
#defaultRoutePattern = re.compile(r"ip route 0.0.0.0 0.0.0.0.+? ([\d\.]+)")
defaultRoutePattern = re.compile(r"ip route 0.0.0.0 0.0.0.0 ([\d\.]+)")
staticRoutePattern = re.compile(r"ip route (?P<dst_subnet>[^0][\d\.]+) (?P<netmask>[\d\.]+) (?P<next_hop>[\d\.]+)")

def parse_cisco_running_config(hostname, username, password):
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
        deviceAccess.send(b"show run\n")
        time.sleep(1)
        output = deviceAccess.recv(65000).decode("ascii")
        #print(output)

        hostnameMatched = hostnamePattern.search(output)
        print("Hostname".ljust(18) + ": " + hostnameMatched.group(1))

        domainNameMatched = domainNamePattern.search(output)
        print("Domain name".ljust(18) + ": " + domainNameMatched.group(1))

        netconfMatched = netconfPattern.search(output)
        if netconfMatched:
            print("NETCONF enabled".ljust(18) + ": Yes")
        else:
            print("NETCONF enabled".ljust(18) + ": No")

        # In this case,you have 2 matches.Therefore, it's necessary to use finditer() instead of search() because search()
        #    only returns one match
        usernameMatched = usernamePattern.finditer(output)
        userList = []
        for username in usernameMatched:
           #print(username.group(1))
           userList.append(username.group(1))

        print("List of users".ljust(18) + ": " + str(userList))

        interfaceMatched = interfacePattern.finditer(output)
        interfaceList = []
        for interface in interfaceMatched:
            interfaceList.append(interface.group(1))
        print("Interface with IP".ljust(18) + ": " + str(interfaceList))

        # When you assign a name for a group, instead of using group(), you have to switch to groupdict()
        interfacePropertyMatched = interfacePropertyPattern.finditer(output)
        interfacePropertyList = []
        for interfaceConfig in interfacePropertyMatched:
            interfacePropertyList.append(interfaceConfig.groupdict())
        #print(interfacePropertyList)
        print("Interface configuration details".ljust(18) + ": ")
        pprint(interfacePropertyList, indent=10)

        defaultRouteMatched = defaultRoutePattern.search(output)
        if defaultRouteMatched:
            print("Default gateway".ljust(18) + ": " +  defaultRouteMatched.group(1))
        else:
            print("Default gateway".ljust(18) + ": Unknown")

        staticRouteMatched = staticRoutePattern.finditer(output)
        staticRouteList = []
        for staticRoute in staticRouteMatched:
            staticRouteList.append(staticRoute.groupdict())
        print("Static route".ljust(18) + ": ")
        pprint(staticRouteList)

        session.close()
    except paramiko.ssh_exception.AuthenticationException:
        traceback.print_exc()
    except AttributeError:
        traceback.print_exc()
    except:
        traceback.print_exc()


parse_cisco_running_config("192.168.2.101", "admin", "admin")

