import pytsk3
from datetime import datetime, timezone, timedelta
import pytz
import argparse

# image_path = '../cfreds_2015_data_leakage_pc.dd'
# inode_number = 27331
def get_meta(image_path, offset, inode_number):
    # Open the disk image
    # image_path = '../cfreds_2015_data_leakage_pc.dd'  # Replace with your disk image path
    image = pytsk3.Img_Info(image_path)

    # Open the file system at a specific partition offset
    partition_offset = offset * 512  # Replace with the offset of your partition in bytes
    fs = pytsk3.FS_Info(image, offset=partition_offset)

    # Retrieve the metadata of the inode
    file_info = fs.open_meta(inode=inode_number)

    # Function to convert Unix timestamps to Eastern Daylight Time (EDT)
    def to_edt(utc, nano):
        # Convert Unix timestamp to UTC datetime
        utc_datetime = datetime.utcfromtimestamp(utc)

        # Convert UTC datetime to Eastern Daylight Time (EDT)
        edt_timezone = pytz.timezone('America/New_York')
        edt_datetime = utc_datetime.replace(tzinfo=timezone.utc).astimezone(edt_timezone)

        return edt_datetime.strftime(f"%Y-%m-%d %H:%M:%S.{nano} (%Z)")

    # Function to find hard links of a given inode number within a file system
    def find_hard_links(fs, directory, target_inode_number, sub_dir_inode=None):
        for entry in directory:
            # Skip entries without a name or if it's "." or ".."
            if not entry.info.name or entry.info.name.name in [b".", b".."]:
                continue
            # Skip entries without metadata
            if entry.info.meta is None:
                continue

            # Check if the current entry's inode number matches the target inode number
            if entry.info.meta.addr == target_inode_number:
                # Print details of the file from its metadata
                print("\n$FILE_NAME Attribute Values")
                print(f"Flags: {entry.info.meta.flags}")
                print(f"Hard link found: {entry.info.name.name.decode('utf-8')}")
                if sub_dir_inode is not None:
                    print(f"Parent MFT Entry: {sub_dir_inode}")
                print(f"Size: {entry.info.meta.size}")
                # Print timestamps in EDT
                print(f"File Modified: {to_edt(entry.info.meta.mtime, entry.info.meta.mtime_nano)}")
                print(f"Accessed: {to_edt(entry.info.meta.atime, entry.info.meta.atime_nano)}")
                print(f"MTF Modified: {to_edt(entry.info.meta.ctime, entry.info.meta.ctime_nano)}")
                print(f"Created: {to_edt(entry.info.meta.crtime, entry.info.meta.crtime_nano)}")

            # If the entry is a directory, recursively search it for hard links
            if entry.info.name.type == pytsk3.TSK_FS_NAME_TYPE_DIR:
                sub_directory = pytsk3.Directory(fs, inode=entry.info.meta.addr)
                subdirectory_inode = entry.info.meta.addr
                find_hard_links(fs, sub_directory, target_inode_number, subdirectory_inode)

    # Open the root directory of the file system
    root_dir = pytsk3.Directory(fs, inode=fs.info.root_inum)

    # Print metadata of the file specified by the inode number
    print("File Metadata:")
    print(f"Size: {file_info.info.meta.size}")
    print(f"Entry: {file_info.info.meta.addr}")
    print(f"Link: {file_info.info.meta.nlink}")
    print(f"Sequence: {file_info.info.meta.seq}")
    print(f"Type: {file_info.info.meta.type}")
    print(f"Flags: {file_info.info.meta.flags}")
    # Print timestamps in EDT
    print(f"File Modified: {to_edt(file_info.info.meta.mtime, file_info.info.meta.mtime_nano)}")
    print(f"Accessed: {to_edt(file_info.info.meta.atime, file_info.info.meta.atime_nano)}")
    print(f"MTF Modified: {to_edt(file_info.info.meta.ctime, file_info.info.meta.ctime_nano)}")
    print(f"Created: {to_edt(file_info.info.meta.crtime, file_info.info.meta.crtime_nano)}")

    # Start the hard link finding process from the root directory
    find_hard_links(fs, root_dir, inode_number)


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Get metadata from file inode")
    parser.add_argument("image_path", help="Path to the image file.")
    parser.add_argument("offset", type=int, help="File system offset")
    parser.add_argument("inode_number", type=int, help="Inode Number")

    # Parse the arguments
    args = parser.parse_args()

    # Print result
    get_meta(args.image_path, args.offset, args.inode_number)