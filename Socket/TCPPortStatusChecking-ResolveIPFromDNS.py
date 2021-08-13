import socket

socket.setdefaulttimeout(0.5)

print("\n" + "#"*25 + " Started to check port status from " + socket.gethostname() + " " + "#"*25) 

def checkTCPPortStatus(ip, port):
    print("\n" + "="*25)
    print("FQDN: " + socket.getfqdn(ip))
    try:
        print("IP: " + socket.gethostbyname(ip))
    except:
        print("Can't get IP address")

    try:
        deviceSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        resultOfChecking = deviceSocket.connect_ex((ip, port))

        if (resultOfChecking == 0):
            print(str(ip) + " is listening on port " + str(port))
            deviceSocket.close()
        else:
            print(str(ip) + " is not listening on port " + str(port))
            deviceSocket.close()
    except socket.gaierror:
        print("Can't check host " + str(ip))
    except:
        print("Exception occrured")

checkTCPPortStatus("192.168.2.10", 44)
checkTCPPortStatus("192.168.2.10", 135)
checkTCPPortStatus("cisco.com", 80)
checkTCPPortStatus("abc", 123)
checkTCPPortStatus("192.168.2.12", 80)
checkTCPPortStatus("192.168.2.12", 123)
