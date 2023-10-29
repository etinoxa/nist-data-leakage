import hashlib
import sys


def calculate_md5(file_path):
    """
    Calculate the MD5 hash of a file.

    :param file_path: Path to the file.
    :return: MD5 hash as a hexadecimal string.
    """
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as file:
        while True:
            data = file.read(4096)  # Read the file in chunks of 4KB
            if not data:
                break
            md5_hash.update(data)
    return md5_hash.hexdigest()


def calculate_sha256(file_path):
    """
    Calculate the SHA-256 hash of a file.

    :param file_path: Path to the file.
    :return: SHA-256 hash as a hexadecimal string.
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        while True:
            data = file.read(4096)  # Read the file in chunks of 4KB
            if not data:
                break
            sha256_hash.update(data)
    return sha256_hash.hexdigest()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python 1_calculate_md5_sha.py <file_path>")
        sys.exit(1)

    file_path = "/home/etinoxa/PycharmProjects/forensic-lab/cfreds_2015_data_leakage_pc.dd"
    # file_path = sys.argv[1]

    try:
        md5_hash = calculate_md5(file_path)
        sha256_hash = calculate_sha256(file_path)

        print(f"MD5 Hash: {md5_hash}")
        print(f"SHA-256 Hash: {sha256_hash}")
    except FileNotFoundError:
        print("File not found.")
