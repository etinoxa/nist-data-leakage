import argparse
from regipy import RegistryHive
from regipy.exceptions import RegistryKeyNotFoundException
from datetime import datetime


# Replace this path with the actual path to your SOFTWARE hive file
# hive_path = '../working_files/registry/SYSTEM'

def get_time_zone(hive_path):
    # Load the hive
    registry_hive = RegistryHive(hive_path)

    try:
        timezone_key = registry_hive.get_key('\ControlSet001\Control\TimeZoneInformation')
        day_light_name = timezone_key.get_value('DaylightName')
        standard_name = timezone_key.get_value('StandardName')
        bias = timezone_key.get_value('Bias')
        active_time_bias = timezone_key.get_value('ActiveTimeBias')
        time_zone_key_name = timezone_key.get_value('TimeZoneKeyName').decode('Windows-1252', errors='replace')

        print('DaylightName:', day_light_name)
        print('StandardName:', standard_name)
        print('Bias:', bias, f'({round(bias/60)} hours)')
        print('ActiveTimeBias:', active_time_bias, f'({round(active_time_bias/60)} hours)')
        print('TimeZoneKeyName:', time_zone_key_name)
    except RegistryKeyNotFoundException:
        print('Timezone key not found')

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Prints Time Zone Setting.")
    parser.add_argument("hive_path", help="Path to the SYSTEM hive file.")

    # Parse the arguments
    args = parser.parse_args()

    # Print Windows version
    get_time_zone(args.hive_path)
