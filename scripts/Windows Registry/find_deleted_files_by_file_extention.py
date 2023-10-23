import argparse
import pytsk3

def search_docx_files(image_path, offset, directory_name, file_type):
    try:
        # Open the disk image
        img_info = pytsk3.Img_Info(image_path)

        # Open the file system at the specified partition offset
        fs_info = pytsk3.FS_Info(img_info, offset=offset * 512)

        # Construct the file search path
        search_path = f"/{directory_name}"

        # Initialize a list to store found file paths
        found_files = []

        # Recursively search for files with the specified extension
        for directory in fs_info.open_dir(path=search_path):
            for fs_object in directory:
                if fs_object.info and fs_object.info.name:
                    file_name = fs_object.info.name.name.decode('utf-8')
                    if file_name.endswith(f".{file_type}"):
                        found_files.append(file_name)

        # Print the found file paths
        if found_files:
            print("Found .{} files in '{}' directory:".format(file_type, directory_name))
            for file_path in found_files:
                print(file_path)
        else:
            print(f"No .{file_type} files found in '{directory_name}' directory.")
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Search for files in a disk image.")
    parser.add_argument("image_path", help="Path to the disk image file.")
    parser.add_argument("offset", type=int, help="Partition offset in sectors.")
    parser.add_argument("directory_name", help="Name of the directory to search within.")
    parser.add_argument("file_type", help="File type to search for (e.g., 'docx').")

    # Parse the arguments
    args = parser.parse_args()

    # Call the search function
    search_docx_files(args.image_path, args.offset, args.directory_name, args.file_type)
