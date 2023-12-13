import pytsk3
from datetime import datetime, timezone, timedelta
import pytz
import argparse

# Usage: python3 USNJournaling_scripts/2_master_file_table_entry.py cfreds_2015_data_leakage_pc.dd 206848
def get_meta(image_path, offset):
    image = pytsk3.Img_Info(image_path)
    partition_offset = offset * 512
    fs = pytsk3.FS_Info(image, offset=partition_offset)

    def to_edt(utc, nano):
        utc_datetime = datetime.utcfromtimestamp(utc)
        edt_timezone = pytz.timezone('America/New_York')
        edt_datetime = utc_datetime.replace(tzinfo=timezone.utc).astimezone(edt_timezone)
        return edt_datetime.strftime(f"%Y-%m-%d %H:%M:%S.{nano} (%Z)")

    def list_inodes(fs, inode_number=None):
        for file in fs:
            if not file.info.meta or file.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                continue  # Skip directories and non-files
            print_metadata(file)

    def print_metadata(file):
        print("\nFile Metadata:")
        print(f"Name: {file.info.name.name.decode()}")
        print(f"Size: {file.info.meta.size}")
        print(f"Entry: {file.info.meta.addr}")
        print(f"Link: {file.info.meta.nlink}")
        print(f"Sequence: {file.info.meta.seq}")
        print(f"Type: {file.info.meta.type}")
        print(f"Flags: {file.info.meta.flags}")
        print(f"File Modified: {to_edt(file.info.meta.mtime, file.info.meta.mtime_nano)}")
        print(f"Accessed: {to_edt(file.info.meta.atime, file.info.meta.atime_nano)}")
        print(f"MTF Modified: {to_edt(file.info.meta.ctime, file.info.meta.ctime_nano)}")
        print(f"Created: {to_edt(file.info.meta.crtime, file.info.meta.crtime_nano)}")

    # Start listing inodes from the root directory
    root_dir = pytsk3.Directory(fs, inode=fs.info.root_inum)
    list_inodes(root_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get metadata from file inode")
    parser.add_argument("image_path", help="Path to the image file.")
    parser.add_argument("offset", type=int, help="File system offset")
    args = parser.parse_args()
    get_meta(args.image_path, args.offset)
