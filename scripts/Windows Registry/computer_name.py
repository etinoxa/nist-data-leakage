import dfwinreg

# Open the registry
registry = dfwinreg.OpenRegistry("HKEY_CURRENT_USER")

# Get the name of the PC
name = registry.Get("Software\Microsoft\Windows NT\CurrentVersion\Winlogon", "ComputerName")

# Print the name of the PC
print(name)
