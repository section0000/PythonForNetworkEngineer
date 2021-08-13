from ncclient import manager

routerManager = manager.connect(
        host="sandbox-iosxe-latest-1.cisco.com",
        port=830,
        username="developer",
        password="C1sco12345",
        hostkey_verify=False,
        device_params={"name": "csr"}
)

configuration = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">    
    <native
        xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <username operation = "delete">
	    <name>netconf_test</name>
	    <privilege>15</privilege>
	    <secret>
	        <encryption>0</encryption>
	        <secret>
                    abc123!
                </secret>
	    </secret>
	</username>
    </native>
</config> """

data = routerManager.edit_config(configuration, target="running")

routerManager.close_session()
