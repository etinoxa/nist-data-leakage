import pytsk3
import hexdump
import argparse

# Stream name = $J or $Max
def get_file_by_inode(image_path, inode, stream_name, offset_multiplier=206848):
    offset = offset_multiplier * 512
    try:
        # Open the disk image
        img = pytsk3.Img_Info(image_path)
        print(f"Opened image: {image_path}")

        # Open the file system
        fs = pytsk3.FS_Info(img, offset=offset)
        print("File system opened.")

        # Open the file by its inode
        f = fs.open_meta(inode=inode)
        print(f"Opened file with inode: {inode}")

        for attribute in f:
            if attribute.info.name and attribute.info.name.decode() == stream_name:
                print(f"Reading data stream: {stream_name}")
                print(attribute.info.name)
                print(attribute.info.size)

                # Read the content of the file
                offset = 0
                size = attribute.info.size
                print(f"File size: {size} bytes")
                while offset < size:
                    available_to_read = min(1024, size - offset)
                    file_data = f.read_random(offset, available_to_read)
                    if not file_data:
                        break
                    hexdump.hexdump(file_data)
                    offset += len(file_data)

    except IOError as e:
        print(f"IOError: {e}")
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Extract and display file content from a disk image based on inode.")
    parser.add_argument("image_path", help="Path to the disk image")
    parser.add_argument("inode", type=int, help="Inode number of the file")
    parser.add_argument("stream_name", type=str, help="Name of the data stream")
    return parser.parse_args()

def main():
    args = parse_arguments()
    get_file_by_inode(args.image_path, args.inode, args.stream_name)

if __name__ == "__main__":
    main()
