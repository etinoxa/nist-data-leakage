import argparse
import pytsk3

# Define the image and the file pattern to search for
# image_path = '../cfreds_2015_data_leakage_pc.dd'
# search_pattern = 'gmreadme.txt'
def get_entry(image_path, search_pattern, return_fs=False):
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


def get_data_streams(image_path, query):
    """
    Retrieves data streams from a file within a disk image.

    Args:
    image_path (str): Path to the disk image.
    query (str): Query to search for the file.

    Returns:
    list: A list of data streams in the file.
    """
    try:
        fs, result = get_entry(image_path, query, return_fs=True)
    except Exception as e:
        print(f"Error accessing the file system: {e}")
        return []

    if not result:
        print("No file found for the given query.")
        return []

    file = result[0][0]
    file_path = result[0][1]
    inode_number = file.info.meta.addr

    return read_stream(file, inode_number, file_path)


def read_stream(file, inode_number, file_path):
    """
    Reads the data streams of a file.

    Args:
    file (File object): The file to read from.
    inode_number (int): The inode number of the file.
    file_path (str): The path of the file.

    Returns:
    list: Data streams from the file.
    """
    streams = []
    for attr in file:
        if attr.info.name:
            stream_name = attr.info.name.decode()
            print(f"{inode_number}-{attr.info.type}: {file_path}:{stream_name}")
            streams.append((stream_name, attr))
    return streams


def main():
    """
    Main function to parse arguments and retrieve data streams.
    """
    parser = argparse.ArgumentParser(description="Finds data streams in a disk image.")
    parser.add_argument("image_path", help="Path to the disk image.")
    parser.add_argument("query", help="Search query for the file.")

    args = parser.parse_args()

    streams = get_data_streams(args.image_path, args.query)
    if streams:
        print("Data streams retrieved successfully.")
    else:
        print("No data streams found.")

if __name__ == "__main__":
    main()
