import pytsk3
import argparse

# Define the image and the file pattern to search for
# image_path = '../cfreds_2015_data_leakage_pc.dd'
# search_pattern = 'gmreadme.txt'
def get_entry(image_path, search_pattern, return_fs = False):
    # Open the disk image
    img = pytsk3.Img_Info(image_path)

    # File system offset (assumed to be provided as in your command)
    fs_offset = 206848

    # Open the file system
    fs = pytsk3.FS_Info(img, offset=fs_offset*512)
    entries = []

    # Define a recursive function to list files
    def list_files(directory, path='/'):

        for entry in directory:
            # Skip ".", ".." or directory entries without a name
            if not entry.info.name or entry.info.name.name in [b".", b".."]:
                continue
            # Skip entries without metadata
            if entry.info.meta is None:
                continue
            # try:
            file_name = entry.info.name.name.decode('utf-8')
            # print(file_name)
            file_path = f"{path}{file_name}"
            current_path = f"{path}{entry.info.name.name.decode('utf-8')}"

            if entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                # print(entry.info.name.name.decode('utf-8'))
                # print(current_path)
                sub_directory = pytsk3.Directory(fs, inode=entry.info.meta.addr)
                list_files(sub_directory, path=f"{current_path}/")
            else:
                if search_pattern in file_name:
                    print(f"Found: {entry.info.meta.addr} | {file_path} | {entry.info.meta.size}")
                    entries.append((entry, file_path))
            # except Exception:
            #     continue



    # Start listing from the root directory
    root_dir = fs.open_dir(path="/")
    list_files(root_dir)
    if return_fs:
        return fs, entries
    else:
        return entries

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Finds file in image.")
    parser.add_argument("image_path", help="Path to the image file.")
    parser.add_argument("search_pattern", help="Search query.")

    # Parse the arguments
    args = parser.parse_args()

    # Print result
    get_entry(args.image_path, args.search_pattern)
