import socket

socket.setdefaulttimeout(0.5)

def checkTCPPortRangeStatus(ip, startPort, endPort):
    endPort = endPort + 1
    print("\n" + "#"*25 + " Checking on " + str(ip) + " " + "#"*25)
    try:
        for port in range(startPort, endPort):
            deviceSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            resultOfChecking = deviceSocket.connect_ex((ip, port))

            if (resultOfChecking == 0):
                print(str(ip) + " is listening on port " + str(port))
                deviceSocket.close()
            else:
                print(str(ip) + " is not listening on port " + str(port))
                deviceSocket.close()
    except:
        print("IP is not valid")

checkTCPPortRangeStatus("192.168.2.10abc", 130, 135)
checkTCPPortRangeStatus("192.168.2.10", 130, 135)
checkTCPPortRangeStatus("192.168.2.12", 80, 90)
