from simplecrypt import encrypt, decrypt
from pprint import pprint
import csv
import json

# Input
filename = input("Input CSV filename (DeviceCredentials.csv): ") or "DeviceCredentials.csv"
key = input("Encryption key (cisco): ") or "cisco"

# Read data from that file
with open(filename) as f:
    deviceCredentialsReader = csv.reader(f)
    deviceCredentialsList = [device for device in deviceCredentialsReader]

print("\n===== Device Credentials =====")
pprint(deviceCredentialsList)

encryptedDeviceCredentialsFilename = input("Output encrypted filename (EncryptedDeviceCredentials.csv): ")\
        or "EncryptedDeviceCredentials.csv"

with open(encryptedDeviceCredentialsFilename, "wb") as f:
    f.write(encrypt(key, json.dumps(deviceCredentialsList)))

print("\nEncrypt successfully!")

print("\nGeting credentials...")
with open(encryptedDeviceCredentialsFilename, "rb") as f:
    deviceCredentialsJSON = decrypt(key, f.read())

deviceCredentialsList = json.loads(deviceCredentialsJSON.decode("utf-8"))
pprint(deviceCredentialsList)

print("\n===== Confirmation: Device Credentials =====")
deviceCredentials = {device[0]:device for device in deviceCredentialsList}
pprint(deviceCredentials)

