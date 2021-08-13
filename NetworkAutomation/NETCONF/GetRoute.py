from ncclient import manager

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
        <ip>
            <route></route>
        </ip>
    </native>
</filter> """

print(routerManager.get_config("running", filter))

routerManager.close_session()
