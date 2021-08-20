import socket

socket.setdefaulttimeout(0.5)

#destination = ("192.168.2.10", 135)
#deviceSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET: used for IPv4, SOCK_STREAM: used for TCP      connection
##resultOfChecking = deviceSocket.connect(destination)
#resultOfChecking = deviceSocket.connect_ex(destination) # Connect with try catch(except) statment. If result is 0, device is listening on that port. If result is  a different number, device is not listening on that port
#
##print(resultOfChecking)
#
#if (resultOfChecking == 0):
#    print("Listening")
#    deviceSocket.close()
#else:
#    print("Not listening")
#    deviceSocket.close()

print("\n" + "#"*25 + " Started to check port status " + "#"*25) 

def checkTCPPortStatus(ip, port):
    deviceSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    resultOfChecking = deviceSocket.connect_ex((ip, port))

    if (resultOfChecking == 0):
        print(str(ip) + " is listening on port " + str(port))
        deviceSocket.close()
    else:
        print(str(ip) + " is not listening on port " + str(port))
        deviceSocket.close()

checkTCPPortStatus("192.168.2.10", 44)
checkTCPPortStatus("192.168.2.10", 135)
checkTCPPortStatus("192.168.2.12", 80)
checkTCPPortStatus("192.168.2.12", 135)
