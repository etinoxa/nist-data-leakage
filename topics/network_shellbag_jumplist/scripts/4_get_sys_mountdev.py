import argparse
from regipy import RegistryHive, exceptions
import binascii
from datetime import datetime, timedelta

# Registry Hive MountedDevices Reader

def filetime_to_dt(filetime):
    """
    Convert Windows FILETIME to datetime.
    """
    filetime_epoch = datetime(1601, 1, 1)
    return filetime_epoch + timedelta(microseconds=filetime // 10)


# hive_path = topics/windows_registry/files/registry/SYSTEM
def get_sys_mountdev(hive_path):
    try:
        registry_hive = RegistryHive(hive_path)
        key_path = r'MountedDevices'
        key = registry_hive.get_key(key_path)
        print(f"Last Write time = {filetime_to_dt(key.header.last_modified)}")

        for value in key.iter_values(as_json=False):
            data_hex = binascii.unhexlify(value.value)[::-1]
            formatted_hex = ' '.join(f'{byte:02x}' for byte in data_hex)
            print(f"{value.name}: {formatted_hex}")

    except exceptions.RegistryKeyNotFoundException:
        print(f"The key path {key_path} was not found in the registry hive.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    parser = argparse.ArgumentParser(description="Registry Hive MountedDevices Reader")
    parser.add_argument("hive_path", help="Path to the registry hive file")
    args = parser.parse_args()

    get_sys_mountdev(args.hive_path)


if __name__ == "__main__":
    main()
