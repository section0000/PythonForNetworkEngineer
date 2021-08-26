import re
from pprint import pprint

hostnamePattern = re.compile(r"hostname (\S+)")
domainNamePattern = re.compile(r"ip domain name (\S+)")
netconfPattern = re.compile(r"netconf-yang\n")
usernamePattern = re.compile(r"username (\S+) privilege (\d{1,2})")
interfacePattern = re.compile(r"interface (\S+)\n.+?\n\s?ip address ([\d\.]+) ([\d\.]+)")
# Instead of letting groups be numbered automatically, you assign names for them
interfacePropertyPattern = re.compile(r"interface (?P<name>\S+)\n.+?\n\s?ip address (?P<ip>[\d\.]+) (?P<netmask>[\d\.]+)")
#defaultRoutePattern = re.compile(r"ip route 0.0.0.0 0.0.0.0.+? ([\d\.]+)")
defaultRoutePattern = re.compile(r"ip route 0.0.0.0 0.0.0.0 ([\d\.]+)")
staticRoutePattern = re.compile(r"ip route (?P<dst_subnet>[^0][\d\.]+) (?P<netmask>[\d\.]+) (?P<next_hop>[\d\.]+)")


with open("02_show_run_output.txt", "r") as f:
    output = f.read()
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

    # In this case, you have 2 matches. Therefore, it's necessary to use finditer() instead of search() because search()
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
