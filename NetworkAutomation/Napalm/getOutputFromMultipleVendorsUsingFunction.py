import json
from napalm import get_network_driver

cisco = ["192.168.2.101"]
arista = ["192.168.2.121"]

def getfacts(ipList, driver, vendor):
	for ip in ipList:
		print("\n\t==== Connecting to " + vendor + " device " + str(ip) + " ====")
		driver = get_network_driver(driver)
		device = driver(
			hostname=ip,
			username="admin",
			password="admin",
			optional_args={"secret": "123"},
		)
		device.open()

		facts = device.get_facts()
		print(json.dumps(facts, sort_keys=True, indent=4))
		#print(json.dumps(facts["os_version"], sort_keys=True, indent=4))	

		device.close()

getfacts(cisco, "ios", "Cisco")
getfacts(arista, "eos", "Arista")
