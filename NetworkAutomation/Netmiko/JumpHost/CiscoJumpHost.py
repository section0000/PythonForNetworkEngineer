from netmiko import Netmiko, redispatch, ssh_exception # Reference: https://ktbyers.github.io/netmiko/docs/netmiko/linux/index.html
import time
import traceback

ciscoJumpHostIP = "192.168.2.102"
ciscoJumpHostUser = "admin"
ciscoJumpHostPassword = "admin"

routerIP = "192.168.2.101"
routerUser = "admin"
routerPassword = "admin"
try:
    print("\n===== Connecting to the Jump Host... =====")
    connection = Netmiko(device_type="cisco_ios",
                         host=ciscoJumpHostIP,
                         username=ciscoJumpHostUser,
                         password=ciscoJumpHostPassword
                        )

    print(connection.find_prompt()) # "Finds the current network device prompt, last line only"
                                         # Result: [php22800@section0000 ~]$
    print("\n** Connected **")
    connection.write_channel("enable\n")
    time.sleep(2)
    connection.write_channel("123\n")
    print("\n===== Connecting to the destination device... =====") 
    connection.write_channel(f"ssh -l {routerUser} {routerIP}\n") # Execute command
    time.sleep(2)
    output = connection.read_channel() # Read the output
    print(output)
    if "Password" in output:
        print("Received password prompt!")
        connection.write_channel(f"{routerPassword}\n")
        time.sleep(2)
        print("\n** Destination device prompt **")
        print(connection.find_prompt())
        connection.write_channel("enable\n")
        time.sleep(2)
        connection.write_channel("123\n")
        print(connection.find_prompt())

        commandList = ["terminal length 0", "show ip int br", "show ip route", "show users"]
        #redispatch(connection, device_type="cisco_ios") # "Dynamically change Netmiko object's class to proper class"
                                                        # You may not use this function and it still works. But it's better to use it
        for command in commandList:
            print(f"Executing command: {command}")
            # You can use either send_command() or write_channel()
            output = connection.send_command(command)
            print(output)

    #        connection.write_channel(f"{command}\n")
    #        time.sleep(1)
    #        output = connection.read_channel()
    #        print(output)
    else:
        print("Unable to get the output from the desitnation device!")
except ssh_exception.NetmikoTimeoutException:
    traceback.print_exc()
except ssh_exception.NetmikoAuthenticationException:
    #traceback.print_exc()
    print("Authentication failed!")
