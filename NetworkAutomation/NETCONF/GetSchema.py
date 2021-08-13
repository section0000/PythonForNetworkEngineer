from ncclient import manager

routerManager = manager.connect(
        host="sandbox-iosxe-latest-1.cisco.com",
        port=830,
        username="developer",
        password="C1sco12345",
        hostkey_verify=False,
        device_params={"name": "csr"}
)

schema = routerManager.get_schema("Cisco-IOS-XE-aaa")
print(schema)

#for capability in routerManager.server_capabilities:
#    print(capability)

routerManager.close_session()
