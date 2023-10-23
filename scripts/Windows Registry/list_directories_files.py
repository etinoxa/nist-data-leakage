import argparse
import pytsk3

# Specify the disk image path and offset


 # Execution = python3 1_list_partitions.py path/to/your/image.dd 206848
def list_partition_details(image_path, offset=None):
    # Open the disk image
    # Create an Img_Info object with the specified offset
    img_info = pytsk3.Img_Info(image_path)
    offset_in_bytes = offset * 512

    # Open the file system
    fs_info = pytsk3.FS_Info(img_info, offset_in_bytes)

    # List the root directory
    root_directory = fs_info.open_dir(path="/")
    for entry in root_directory:
        print(entry.info.name.name)




if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="List disk partitions and their directories.")
    parser.add_argument("image_path", help="Path to the disk image file.")
    parser.add_argument("offset", type=int, help="Partition offset in bytes.", nargs='?')

    # Parse the arguments
    args = parser.parse_args()

    # List partition details
    list_partition_details(args.image_path, args.offset)
