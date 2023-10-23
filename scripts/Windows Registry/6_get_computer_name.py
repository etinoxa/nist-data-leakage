import argparse
from regipy import RegistryHive
from regipy.exceptions import RegistryKeyNotFoundException
from datetime import datetime


# Replace this path with the actual path to your SYSTEM hive file
# hive_path = '../working_files/registry/SYSTEM'

def get_computer_name(hive_path):
    # Load the hive
    registry_hive = RegistryHive(hive_path)

    try:
        computer_key = registry_hive.get_key('\ControlSet001\Control\ComputerName\ComputerName')
        computer_name = computer_key.get_value('ComputerName')
        print('Computer Name:', computer_name)
    except RegistryKeyNotFoundException:
        print('Computer name key not found')

    try:
        network_key = registry_hive.get_key('\ControlSet001\\Services\\Tcpip\\Parameters')
        hostname = network_key.get_value('Hostname')
        print('Hostname:', hostname)
    except RegistryKeyNotFoundException:
        print('Hostname key not found')

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Prints Time Zone Setting.")
    parser.add_argument("hive_path", help="Path to the SYSTEM hive file.")

    # Parse the arguments
    args = parser.parse_args()

    # Print Windows version
    get_computer_name(args.hive_path)
