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
        <hostname></hostname>
        <interface>
	    <GigabitEthernet>
    	        <name>3</name>
		<description>Configured via Python</description>
		<ip>
		    <address>
		        <primary>
			    <address>1.1.1.1</address>
			    <mask>255.255.255.0</mask>
			</primary>
		    </address>
		</ip>
		<logging>
		    <event>
			<link-status/>
		    </event>
		</logging>
		<mop>
		    <enabled>false</enabled>
		    <sysid>false</sysid>
		</mop>
		<negotiation
		    xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ethernet">
		    <auto>true</auto>
		</negotiation>
	    </GigabitEthernet>
        </interface>
    </native>
</config> """

data = routerManager.edit_config(configuration, target="running")

routerManager.close_session()
