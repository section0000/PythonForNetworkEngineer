from ncclient import manager
import xml.etree.ElementTree as ET

routerManager = manager.connect(
        host="sandbox-iosxe-latest-1.cisco.com",
        port=830,
        username="developer",
        password="C1sco12345",
        hostkey_verify=False,
        device_params={"name": "csr"}
)

#filter = """
#<filter>
#    <native
#        xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
#        <hostname></hostname>
#    </native>
#</filter> """

# CSR1000v 17.3 and above
filter = """
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native
        xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface></interface>
    </native>
</filter> """

output = routerManager.get_config("running", filter)

root = ET.fromstring(str(output))

n = int(input("Enter interface number: "))

interfaceNumber = list(root)[0][0][0][n-1][0].text
interfaceIP = list(root)[0][0][0][n-1][2][0][0][0].text

print("GigabitEthernet " + interfaceNumber + " - IP: " + interfaceIP)

routerManager.close_session()
