import argparse
import pytsk3


def list_unallocated_space(image_path):
    # Open the disk image
    img_info = pytsk3.Img_Info(image_path)

    # Open the volume system
    vol_info = pytsk3.Volume_Info(img_info)

    # Print partition table header
    print("Slot      Start        End          Length       Description")

    # Iterate through the partitions
    for part in vol_info:
        start = part.start
        end = start + part.len - 1
        length = part.len
        description = part.desc

        print(f"{part.addr:4}  {start:12}  {end:12}  {length:12}  {description}")


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="List unallocated space on a disk.")
    parser.add_argument("image_path", help="Path to the disk image file.")

    # Parse the arguments
    args = parser.parse_args()

    # List unallocated space
    list_unallocated_space(args.image_path)
