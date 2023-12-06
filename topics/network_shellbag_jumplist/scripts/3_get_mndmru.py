from regipy import RegistryHive, exceptions
import argparse
from datetime import datetime, timedelta

# Prints content of Map Network Drive MRU.

def filetime_to_dt(filetime):
    """
    Convert Windows FILETIME to datetime.
    Windows FILETIME is the number of 100-nanosecond intervals since January 1, 1601 (UTC).
    """
    # FILETIME epoch in Unix timestamp
    filetime_epoch = datetime(1601, 1, 1)

    # Convert the FILETIME value to a timedelta and add it to the FILETIME epoch
    return filetime_epoch + timedelta(microseconds=filetime // 10)


# hive_path = "../../topics/windows_registry/files/registry/NTUSER_Informant.DAT"
def get_runmru(hive_path):
    # Initialize the Registry Hive object
    registry_hive = RegistryHive(hive_path)

    # The RunMRU key path within the NTUSER.DAT hive
    key_path = r'\Software\Microsoft\Windows\CurrentVersion\Explorer\Map Network Drive MRU'

    try:
        # Attempt to get the RunMRU key from the hive
        key = registry_hive.get_key(key_path)

        # Convert the last write time to a datetime object
        last_write_time = filetime_to_dt(key.header.last_modified)
        print(f"Last Write Time: {last_write_time}")

        # Iterate over all values within the RunMRU key and print them
        for value in key.iter_values():
            # Each value is a named tuple, so you can access its name and data properties
            print(f"Name: {value.name}, Data: {value.value}")

    except exceptions.RegistryKeyNotFoundException:
        # Handle the case where the RunMRU key does not exist
        print(f"The key path {key_path} was not found in the registry hive.")
    except Exception as e:
        # Handle any other unexpected exceptions
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Prints content of Map Network Drive MRU.")
    parser.add_argument("hive_path", help="Path to the NTUSER.DAT file.")

    # Parse the arguments
    args = parser.parse_args()

    # Print content of RunMRU
    get_runmru(args.hive_path)