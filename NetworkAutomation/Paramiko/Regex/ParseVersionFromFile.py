import re

versionPattern = re.compile(r"Version (\S+)")
modelPattern = re.compile(r"Linux (\S+).+")
serialNumberPattern = re.compile(r"Processor board ID (\S+)")
uptimePattern = re.compile(r"(.+) uptime is (.+)")

with open("01_show_version_output.txt", "r") as f:
    output = f.read()
    #print(output)

    versionMatched = versionPattern.search(output)
    print("IOS version".ljust(18) + ": " + versionMatched.group(1))

    modelMatched = modelPattern.search(output)
    print("Model".ljust(18) + ": " + modelMatched.group(1))

    serialNumberMatched = serialNumberPattern.search(output)
    print("Serial number".ljust(18) + ": " + serialNumberMatched.group(1))

    uptimeMatched = uptimePattern.search(output)
    print("Hostname".ljust(18) + ": " + uptimeMatched.group(1))
    print("Up time".ljust(18) + ": " + uptimeMatched.group(2))
