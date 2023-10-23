import argparse

import pytsk3


# TODO Get volume serial number
# Execution = python3 1_list_partitions.py path/to/your/image.dd 206848
def list_partition_details(image_path, offset=None):
    # Open the disk image
    img_info = pytsk3.Img_Info(image_path)

    # Open the volume system
    vol_info = pytsk3.Volume_Info(img_info)
    offset_in_byte = offset * 512

    # Open the file system
    fs_info = pytsk3.FS_Info(img_info, offset_in_byte)

    # Iterate through the partitions
    for part in vol_info:
        start = part.start
        length = part.len
        description = part.desc
        part_offset = start * 512

        if offset is None or offset == part_offset / 512:
            print(
                f"Partition address: {part.addr}\n"
                f"start: {start}\n"
                f"length: {length}\n"
                f"description: {description}\n"
                f"offset: {part_offset}\n")


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="List disk partitions and their details.")
    parser.add_argument("image_path", help="Path to the disk image file.")
    parser.add_argument("offset", type=int, help="Partition offset in bytes.", nargs='?')

    # Parse the arguments
    args = parser.parse_args()

    # List partition details
    list_partition_details(args.image_path, args.offset)
