import json
from napalm import get_network_driver

cisco = ["192.168.2.101"]
arista = ["192.168.2.121"]

for ciscoIP in cisco:
	print("\n\t==== Connecting to device " + str(ciscoIP) + " ====")
	driver = get_network_driver("ios")
	device = driver(
		hostname=ciscoIP,
		username="admin",
		password="admin",
		optional_args={"secret": "123"},
	)
	device.open()

	facts = device.get_facts()
	#print(json.dumps(facts, sort_keys=True, indent=4))
	print(json.dumps(facts["os_version"], sort_keys=True, indent=4))	

	device.close()

for aristaIP in arista:
	print("\n\t==== Connecting to device " + str(aristaIP) + " ====")
	driver = get_network_driver("eos")
	device = driver(
		hostname=aristaIP,
		username="admin",
		password="admin",
		#optional_args={"secret": "123"},
	)
	device.open()

	facts = device.get_facts()
	#print(json.dumps(facts, sort_keys=True, indent=4))
	print(json.dumps(facts["interface_list"], sort_keys=True, indent=4))	

	device.close()


