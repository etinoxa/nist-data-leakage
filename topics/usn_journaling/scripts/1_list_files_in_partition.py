import argparse
import pytsk3

def list_files_in_partition(image_path, offset):
    try:
        # Open the disk image
        img_info = pytsk3.Img_Info(image_path)

        # Open the file system at the specified partition offset
        fs_info = pytsk3.FS_Info(img_info, offset=offset * 512)

        # Get the root directory
        root_directory = fs_info.open_dir(path="/")

        # Initialize a list to store file names
        partition_files = []

        # Iterate over all files and directories
        for fs_object in root_directory:
            if fs_object.info.name:
                # Check if the file is unallocated (deleted)
                if pytsk3.TSK_FS_META_FLAG_ALLOC:
                    partition_files.append(fs_object.info.name.name.decode('utf-8'))

        # Print the list of deleted files
        if partition_files:
            print("Partition files:")
            for file_name in partition_files:
                print(file_name)
        else:
            print("No found.")
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="List deleted files on a partition.")
    parser.add_argument("image_path", help="Path to the disk image file.")
    parser.add_argument("offset", type=int, help="Partition offset in bytes.")

    # Parse the arguments
    args = parser.parse_args()

    # List deleted files
    list_files_in_partition(args.image_path, args.offset)
