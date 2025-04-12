#!/usr/bin/env python3
import os

"""
dpkg-status Parser Script

Description:
This Python3 script parses the /var/lib/dpkg/status file on Debian-based systems (e.g., Debian 12)
to extract packages explicitly installed by the user. It uses metadata from the dpkg status file 
to determine which packages were manually installed, excluding dependencies and auto-installed packages.

Usage:
- Ensure that the /var/lib/dpkg/status file exists and is accessible.
- Run the script on a Debian-based system to get a list of user-installed packages.

Requirements:
- Python3
- Read permissions for the /var/lib/dpkg/status file

Notes:
- This script targets Debian-based systems and may not work correctly on other distributions.
- Modify the detection logic to suit more complex scenarios if needed.

Author:
Jesse Finn
"""
def parse_dpkg_status(file_path):

    # Store found package in list for display
    explicitly_installed = []

    try:
        with open(file_path, 'r') as file:
            package = None
            manual_installed = False

            # Loop through the file to parse
            for line in file:
                # Extract package name
                if line.startswith("Package:"):
                    # Clean up the string
                    package = line.split(":")[1].strip()

                # Check if the package is explicitly installed
                elif line.startswith("Installed-Size:") and package:
                    # Example assumption for explicit installation
                    manual_installed = True

                # End of package entry
                elif line.strip() == "" and package:
                    if manual_installed:
                        # Add the found package to the explicitly installed list
                        explicitly_installed.append(package)
                    # Reset for next package
                    package = None
                    manual_installed = False

        return explicitly_installed

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found. Ensure you are on a Debian-based system.")
        return []

if __name__ == "__main__":
    # Target file(s) path
    dpkg_status_path = "/var/lib/dpkg/status"
    # TODO check other files for packages explicitly installed by the user.

    # Ensure the script is running on Debian-based systems
    if os.path.exists(dpkg_status_path):
        # Call the parse dpkg status method to obtain the list of packages explicitly installed by the user
        user_installed_packages = parse_dpkg_status(dpkg_status_path)
        print("Packages explicitly installed by the user:")
        # Loop of explicitly installed package list and display to console
        for pkg in user_installed_packages:
            print(f"- {pkg}")
    else:
        print(f"{dpkg_status_path} does not exist. This script targets Debian-based systems only.")
