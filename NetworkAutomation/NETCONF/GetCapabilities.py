from ncclient import manager

routerManager = manager.connect(
        host="sandbox-iosxe-latest-1.cisco.com",
        port=830,
        username="developer",
        password="C1sco12345",
        hostkey_verify=False,
        device_params={"name": "csr"}
)

for routerCapability in routerManager.server_capabilities:
    print(routerCapability)

routerManager.close_session()
