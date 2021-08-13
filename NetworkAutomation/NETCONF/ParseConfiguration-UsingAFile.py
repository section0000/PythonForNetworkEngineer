import xml.etree.ElementTree as ET
tree = ET.parse('Interface.xml')
root = tree.getroot()

#print(root[0][0][0][0][0].tag)
#print(root[0][0][0][0][0].text)
#print(root[0][0][0][0][0].attrib)

n = int(input("Enter interface number: "))

interfaceNumber = list(root)[0][0][0][n-1][0].text
interfaceIP = list(root)[0][0][0][n-1][2][0][0][0].text

print("GigabitEthernet " + interfaceNumber + " - IP: " + interfaceIP)



