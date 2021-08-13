from nornir import InitNornir
from nornir_utils.plugins.functions import print_result, print_title
from nornir_napalm.plugins.tasks import napalm_get

nr = InitNornir(
    config_file="config.yaml", dry_run=True
)

results = nr.run(
    task=napalm_get, getters=["facts", "interfaces"]
)

print_title("Napalm get")
#print_result(results)
print(nr.inventory.hosts)

host = nr.inventory.hosts["vIOS-R1"]
print(host.keys())
print(host["site"])
