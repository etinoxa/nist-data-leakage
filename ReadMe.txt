Disk Image
....
The disk image can be downloaded from the following link:
https://cfreds-archive.nist.gov/data_leakage_case/images/pc/cfreds_2015_data_leakage_pc.7z.001
https://cfreds-archive.nist.gov/data_leakage_case/images/pc/cfreds_2015_data_leakage_pc.7z.002
https://cfreds-archive.nist.gov/data_leakage_case/images/pc/cfreds_2015_data_leakage_pc.7z.003

Registries
....
The registries have been extracted from the disk image
and can be found in /topics/registry/ within the project folder.

Packages to install

```
Pytsk3: Python bindings for the SleuthKit -> pip install pytask3
regipy: Regipy is a python library for parsing offline registry hives -> pip install regipy
Hexdump: dump binary to hex and restore it back -> pip install hexdump


Parameters to run the script

```
dd_path: path to the disk image
dd_offset: offset of the disk image
system_registry_path: path to the system registry hive
software_registry_path: path to the software registry hive
ntuser_informant_registry: path to the ntuser registry hive

```

```