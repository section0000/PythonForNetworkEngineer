from napalm import get_network_driver
from getpass import getpass
import urllib3

urllib3.disable_warnings()

username = input("Enter username: ")
password = getpass("Enter password: ")
#enablePassword = getpass("Enter enable password: ")

driver = get_network_driver("nxos")
device = driver(
	hostname = "192.168.2.131",
	username = username,
	password = password,
#	optional_args = {"secret": enablePassword},
)
device.open()

device.load_merge_candidate(filename="Configuration.txt")
print(device.compare_config())

changes = device.compare_config()
if len(changes) > 0: # If there is at lease a modification happened
	choice = input("\nWould you like to commit these changes? (y/n)")
	if (choice == "y"):
		print("Committing...")
		device.commit_config()
	else:
		print("Discared!")
		device.discard_config()
else:
	print("No changes have been made")

device.close()

