import paramiko
import time

n = 1
while True:
    showCommand = input("Enter show command: ")
    if (showCommand == "" or showCommand == "exit"):
        print("Exiting...")
        break

    session = paramiko.SSHClient()
    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #print("="*25 + " Connecting to device " + ip  + " " + "="*25)
    session.connect(hostname="192.168.2.101",
                    username="admin",
                    password="admin"
                   )

    deviceAccess = session.invoke_shell()
    deviceAccess.send(b"enable\n")
    deviceAccess.send(b"123\n")
    deviceAccess.send(b"terminal length 0\n")
    deviceAccess.send(showCommand + "\n")
    time.sleep(0.5)
    output = deviceAccess.recv(65000)
    print(output.decode("ascii"))
    time.sleep(0.5)
    session.close()

    with open(f"{n:02d}_{showCommand.replace(' ', '_')}_output.txt", "w") as fileOut:
        fileOut.write(output.decode("ascii"))
    n = n + 1 
