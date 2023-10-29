import argparse
from regipy import RegistryHive

# Replace this path with the actual path to your SOFTWARE hive file
# hive_path = '../working_files/registry/SOFTWARE'
# Get the Windows version information
def get_windows_version(hive_path):
    key_path = r'\Microsoft\Windows NT\CurrentVersion'

    # Load the hive
    registry_hive = RegistryHive(hive_path)

    # registry_hive.get_key()
    key = registry_hive.get_key(key_path)

    # Get the values
    product_name = key.get_value('ProductName')
    current_build = key.get_value('CurrentBuild')
    current_version = key.get_value('CurrentVersion')
    build_lab_ex = key.get_value('BuildLabEx')

    # Print the Windows version information
    print(f'Product Name: {product_name}')
    print(f'Current Build: {current_build}')
    print(f'Current Version: {current_version}')
    print(f'Build Lab Ex: {build_lab_ex}')


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Prints Windows version.")
    parser.add_argument("hive_path", help="Path to the SOFTWARE hive file.")

    # Parse the arguments
    args = parser.parse_args()

    # Print Windows version
    get_windows_version(args.hive_path)

