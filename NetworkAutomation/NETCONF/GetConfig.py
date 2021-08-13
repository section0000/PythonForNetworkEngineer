from ncclient import manager

routerManager = manager.connect(
        host="sandbox-iosxe-latest-1.cisco.com",
        port=830,
        username="developer",
        password="C1sco12345",
        hostkey_verify=False,
        device_params={"name": "csr"}
)

configuration = routerManager.get_config("running")
print(configuration)

#for capability in routerManager.server_capabilities:
#    print(capability)

routerManager.close_session()
