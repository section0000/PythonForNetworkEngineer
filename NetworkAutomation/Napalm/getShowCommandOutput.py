import json
from napalm import get_network_driver

driver = get_network_driver("ios")
device = driver(
	hostname="192.168.2.101", 
	username="admin", 
	password="admin",
	optional_args = {"secret": "123"},	
)
device.open()

print("\tGET FACTS\n")
facts = device.get_facts()
print(json.dumps(facts, sort_keys=True, indent=4))

print("\nPING TEST\n")
pingTest = device.ping("192.168.2.1")
print(json.dumps(pingTest, sort_keys=True, indent=4))

device.close()
