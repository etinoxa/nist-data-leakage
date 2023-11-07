from regipy import RegistryHive
import argparse

# hive_path = "../working_files/registry/SOFTWARE"
# Execution = python .\topics\9_get_installed_apps.py .\working_files\registry\SOFTWARE


def get_installed_apps(hive_path):
    registry = RegistryHive(hive_path)
    tcpip_interfaces_key = r"\Microsoft\Windows\CurrentVersion\Installer\UserData"

    # Iterate over all network interfaces
    interfaces = registry.get_key(tcpip_interfaces_key)
    for i in interfaces.iter_subkeys():
        print(i.name)
        products = i.get_subkey("Products")
        for j in products.iter_subkeys():
            properties = j.get_subkey("InstallProperties")
            print(f'{properties.get_value("DisplayName")} {properties.get_value("DisplayVersion")} ({properties.get_value("Publisher")})')


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="List installed applications")
    parser.add_argument("hive_path", help="Path to the registry file.")

    # Parse the arguments
    args = parser.parse_args()

    # Print Windows version
    get_installed_apps(args.hive_path)