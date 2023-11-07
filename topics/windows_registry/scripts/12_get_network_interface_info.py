from regipy import RegistryHive
import argparse

#hive_path = "../working_files/registry/SYSTEM"
# Execution = python .\topics\12_get_network_interface_info.py .\working_files\registry\SYSTEM

def get_network_interface_info(hive_path):
    registry = RegistryHive(hive_path)
    tcpip_interfaces_key = r"\ControlSet001\Services\Tcpip\Parameters\Interfaces"

    interfaces = registry.get_key(tcpip_interfaces_key)

    for i in interfaces.iter_subkeys():
        print(f"Adapter: {i.name}")

        for j in i.iter_values(as_json=True):
            print(f"\t{j.name}: {j.value}")
        print("\n")


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="List information of network interface(s) with an IP address assigned by DHCP")
    parser.add_argument("hive_path", help="Path to the registry file.")

    # Parse the arguments
    args = parser.parse_args()

    # Print Windows version
    get_network_interface_info(args.hive_path)