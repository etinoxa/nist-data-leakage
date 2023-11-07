from regipy import RegistryHive
import datetime
import argparse


# hive_path = "../working_files/registry/SYSTEM"
# Execution = python .\topics\11_get_shutdown_time.py .\working_files\registry\SYSTEM
def get_shutdown_time(hive_path):
    key_path = r"\ControlSet001\Control\Windows"
    # hive_path = "../working_files/registry/SYSTEM"
    # Load the hive
    registry_hive = RegistryHive(hive_path)

    key = registry_hive.get_key(key_path)
    try:
        shutdowntime = key.get_value('ShutdownTime')

        # Convert bytes to an integer
        filetime_int = int.from_bytes(shutdowntime, byteorder='little')

        # Define the FILETIME epoch
        filetime_epoch = datetime.datetime(1601, 1, 1)

        # Convert the integer to a datetime object
        shutdowntime = filetime_epoch + datetime.timedelta(microseconds=filetime_int / 10)

        print(f"ShutdownTime: {shutdowntime}")

    except FileNotFoundError:
        return "Key or value not found in the registry"
    except PermissionError:
        return "Permission denied. Please run the script with elevated privileges."


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="List last recorded shutdown date/time.")
    parser.add_argument("hive_path", help="Path to the registry file.")

    # Parse the arguments
    args = parser.parse_args()

    # Print Windows version
    get_shutdown_time(args.hive_path)