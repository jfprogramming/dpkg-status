#!/usr/bin/env python3
import os

"""
dpkg-status Parser Script

Description:
This Python3 script parses the /var/lib/dpkg/status file on Debian-based systems (e.g., Debian 12)
to extract packages explicitly installed by the user. It uses metadata from the dpkg status file 
and /var/lib/apt/extended_states to determine which packages were manually installed, excluding dependencies 
and auto-installed packages.

Usage:
- Ensure that the /var/lib/dpkg/status file and /var/lib/apt/extended_states file exist and are accessible.
- Run the script on a Debian-based system to get a list of user-installed packages.

Requirements:
- Python3
- Read permissions for the required files

Notes:
- This script targets Debian-based systems and may not work correctly on other distributions.
- Modify the detection logic to suit more complex scenarios if needed.

Author:
Jesse Finn
"""

def parse_manual_packages(extended_states_path):
    """
    Parses the extended_states file to build a set of packages explicitly installed by the user.
    :param extended_states_path: Path to /var/lib/apt/extended_states file.
    :return: Set of manually installed package names.
    """
    manual_packages_set = set()
    try:
        if os.path.exists(extended_states_path):
            with open(extended_states_path, 'r') as extended_file:
                package_name = None
                for line in extended_file:
                    if line.startswith("Package:"):
                        package_name = line.split(":")[1].strip()
                    elif line.startswith("Manual:") and "yes" in line and package_name:
                        manual_packages_set.add(package_name)
                    else:
                        print(f"parse_manual_packages package_name: {package_name}")
                        print(f"line: {line}")
        return manual_packages_set
    # Error handling
    except FileNotFoundError:
        print(f"Error: {extended_states_path} not found.")
        return set()

def parse_dpkg_status(dpkg_status_path, manual_packages):
    """
    Parses the dpkg status file to extract packages explicitly installed by the user and verified against manual_packages.
    :param dpkg_status_path: Path to /var/lib/dpkg/status file.
    :param manual_packages: Set of manually installed package names.
    :return: List of explicitly installed packages.
    """
    explicitly_installed = set()
    try:
        with open(dpkg_status_path, 'r') as dpkg_file:
            package_name = None
            package_installed = False

            for line in dpkg_file:
                if line.startswith("Package:"):
                    package_name = line.split(":")[1].strip()
                elif line.startswith("Status:") and "install ok installed" in line:
                    package_installed = True
                elif line.strip() == "" and package_name:
                    if package_installed and package_name in manual_packages:
                        # Add the package to the set/list
                        explicitly_installed.add(package_name)
                    else:
                        print(f"parse_dpkg_status package_name: {package_name} package_installed: {package_installed}")
                        print(f"line: {line}")
                    # Reset variables for next package
                    package_name      = None
                    package_installed = False
        return list(explicitly_installed)
    except FileNotFoundError:
        print(f"Error: {dpkg_status_path} not found.")
        return []

if __name__ == "__main__":
    dpkg_status_path     = "/var/lib/dpkg/status"
    extended_states_path = "/var/lib/apt/extended_states"

    if os.path.exists(dpkg_status_path):
        manual_packages         = parse_manual_packages(extended_states_path)
        user_installed_packages = parse_dpkg_status(dpkg_status_path, manual_packages)

        if not user_installed_packages:
            print("No explicitly installed packages found!")
        else:
            print("Packages explicitly installed by the user:")
            for pkg in user_installed_packages:
                print(f"- {pkg}")
    else:
        print(f"{dpkg_status_path} does not exist. This script targets Debian-based systems only.")
