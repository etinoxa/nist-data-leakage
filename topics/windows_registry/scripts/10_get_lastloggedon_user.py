from regipy import RegistryHive
import argparse

# hive_path = "../working_files/registry/SOFTWARE"
# Execution = python .\topics\10_get_lastloggedon_user.py .\working_files\registry\SOFTWARE
def get_last_logged_on_user(hive_path):
    key_path = r"\Microsoft\Windows\CurrentVersion\Authentication\LogonUI"

    # Load the hive
    registry_hive = RegistryHive(hive_path)

    key = registry_hive.get_key(key_path)
    try:
        last_logged_on_user = key.get_value('LastLoggedOnUser')
        last_logged_on_sam_user = key.get_value('LastLoggedOnSAMUser')

        print(f"LastLoggedOnUser = {last_logged_on_user}")
        print(f"LastLoggedOnSAMUser = {last_logged_on_sam_user}")

    except FileNotFoundError:
        print("Key or value not found in the registry")
    except PermissionError:
        print("Permission denied. Please run the script with elevated privileges.")



if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="List last user to logon into PC.")
    parser.add_argument("hive_path", help="Path to the registry file.")

    # Parse the arguments
    args = parser.parse_args()

    # Print Windows version
    get_last_logged_on_user(args.hive_path)
