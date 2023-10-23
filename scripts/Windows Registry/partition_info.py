import struct
import sys

# Execution: python3 partition_info.py ../cfreds_2015_data_leakage_pc.dd 206848

def read_sector(image_file, offset, sector_size):
    image_file.seek(offset * sector_size)
    return image_file.read(sector_size)

def parse_boot_sector(sector_data):
    # Extract file system information
    file_system_type = sector_data[3:11].decode("utf-8", errors="ignore")
    oem_name = sector_data[71:82].decode("utf-8", errors="ignore")
    version = sector_data[82:90].decode("utf-8", errors="ignore")

    # Extract metadata information
    first_cluster_of_mft, first_cluster_of_mft_mirror = struct.unpack("<QQ", sector_data[48:64])
    size_of_mft_entries, size_of_index_records = struct.unpack("<II", sector_data[64:72])
    mft_range = "0 - " + str(first_cluster_of_mft * size_of_mft_entries)
    root_directory = struct.unpack("<I", sector_data[96:100])[0]

    # Extract content information
    sector_size, cluster_size = struct.unpack("<HH", sector_data[11:15])
    total_cluster_range = "0 - " + str(int(((root_directory * cluster_size) / sector_size) - 1))
    total_sector_range = "0 - " + str(int((root_directory * cluster_size) - 1))

    return {
        "\nFILE SYSTEM INFORMATION": {
            "file_system_type": file_system_type,
            "oem_name": oem_name,
            "version": version,
        },
        "\nMETADATA INFORMATION": {
            "first_cluster_of_mft": first_cluster_of_mft,
            "first_cluster_of_mft_mirror": first_cluster_of_mft_mirror,
            "size_of_mft_entries": size_of_mft_entries,
            "size_of_index_records": size_of_index_records,
            "mft_range": mft_range,
            "root_directory": root_directory,
        },
        "\nCONTENT INFORMATION": {
            "sector_size": sector_size,
            "cluster_size": cluster_size,
            "total_cluster_range": total_cluster_range,
            "total_sector_range": total_sector_range,
        },
    }

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python partition_details.py <image_file> <offset>")
        sys.exit(1)

    image_file_path = sys.argv[1]
    offset = int(sys.argv[2])
    sector_size = 512

    try:
        with open(image_file_path, "rb") as image_file:
            sector_data = read_sector(image_file, offset, sector_size)
            partition_details = parse_boot_sector(sector_data)

            # Display partition details
            for section, details in partition_details.items():
                print(section)
                for key, value in details.items():
                    print(f"{key}: {value}")

    except FileNotFoundError:
        print("Image file not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
