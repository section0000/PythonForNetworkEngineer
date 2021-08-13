from nornir import InitNornir
from nornir_utils.plugins.functions import print_result, print_title
from nornir_netmiko import netmiko_send_command, netmiko_send_config

nr = InitNornir(
    config_file="config.yaml", dry_run=True
)

def configure(loopbackTask):
	loopbackTask.run(task=netmiko_send_config, config_commands = ["int lo200", "int lo201"])
	loopbackTask.run(task=netmiko_send_command, command_string = "show ip int br")

print_title("Netmiko send ")

results = nr.run(task=configure)
print_result(results)

