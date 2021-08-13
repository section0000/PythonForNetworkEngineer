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
<config
	xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
	<native
	    xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
	    <ip>
		<route>
		    <ip-route-interface-forwarding-list>
			<prefix>1.1.1.0</prefix>
			<mask>255.255.255.0</mask>
			<fwd-list>
			    <fwd>192.168.12.26</fwd>
			</fwd-list>
		    </ip-route-interface-forwarding-list>
		</route>
	    </ip>
	</native>
</config> """

data = routerManager.edit_config(configuration, target="running")

routerManager.close_session()
