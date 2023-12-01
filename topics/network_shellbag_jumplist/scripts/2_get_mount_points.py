import argparse
from regipy import RegistryHive

def read_registry_key(hive_path):
    try:
        key_path = r'\Software\Microsoft\Windows\CurrentVersion\Explorer\MountPoints2'
        registry_hive = RegistryHive(hive_path)
        key = registry_hive.get_key(key_path)
        for subkey in key.iter_subkeys():
            print(subkey.name)
    except FileNotFoundError:
        print(f"The file at {hive_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Read a specific registry key from a Windows Registry hive file.')
    parser.add_argument('hive_path', help='Path to the Registry hive file')

    args = parser.parse_args()

    read_registry_key(args.hive_path)

if __name__ == '__main__':
    main()
