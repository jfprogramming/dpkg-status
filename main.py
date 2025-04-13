#!/usr/bin/env python3
import os
import argparse
import logging


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



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_manual_packages(extended_states_path):
    """
    Parses the extended_states file to determine explicitly installed packages.
    :param extended_states_path: Path to /var/lib/apt/extended_states file.
    :return: Set of explicitly installed package names.
    """
    manual_packages_set = set()
    try:
        if os.path.exists(extended_states_path) and os.access(extended_states_path, os.R_OK):
            with open(extended_states_path, "r", encoding="utf-8") as extended_file:
                package_name = None
                auto_installed = False

                for line in extended_file:
                    line = line.strip()
                    if line.startswith("Package:"):
                        package_name = line.split(":")[1].strip()
                        auto_installed = False  # Reset flag for new package
                    elif line.startswith("Auto-Installed:"):
                        auto_installed = line.split(":")[1].strip() == "1"

                    # At the end of a package block, add to manual_packages_set if not auto-installed
                    if line == "" and package_name:
                        if not auto_installed:
                            manual_packages_set.add(package_name)
                        package_name = None  # Reset for the next package
        else:
            print(f"Cannot access file: {extended_states_path}")
    except FileNotFoundError:
        print(f"Error: {extended_states_path} not found.")
    return manual_packages_set


def parse_dpkg_status(dpkg_status_path, manual_packages):
    """
    Parses the dpkg status file to extract packages explicitly installed by the user and verified against manual_packages.
    :param dpkg_status_path: Path to /var/lib/dpkg/status file.
    :param manual_packages: Set of manually installed package names.
    :return: List of explicitly installed packages.
    """
    explicitly_installed = set()
    try:
        with open(dpkg_status_path, 'r', encoding='utf-8') as dpkg_file:
            package_name = None
            package_installed = False

            for line in dpkg_file:
                if line.startswith("Package:"):
                    package_name = line.split(":")[1].strip()
                elif line.startswith("Status:") and "install ok installed" in line:
                    package_installed = True
                elif line.strip() == "" and package_name:
                    if package_installed and package_name in manual_packages:
                        explicitly_installed.add(package_name)
                    package_name = None
                    package_installed = False
        return list(explicitly_installed)
    except FileNotFoundError:
        logger.error(f"Error: {dpkg_status_path} not found.")
        return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse dpkg status and extended states files.")
    parser.add_argument('--status', default='/var/lib/dpkg/status', help='Path to dpkg status file')
    parser.add_argument('--states', default='/var/lib/apt/extended_states', help='Path to extended states file')
    args = parser.parse_args()

    dpkg_status_path = args.status
    extended_states_path = args.states

    if os.path.exists(dpkg_status_path) and os.access(dpkg_status_path, os.R_OK):
        manual_packages = parse_manual_packages(extended_states_path)
        user_installed_packages = parse_dpkg_status(dpkg_status_path, manual_packages)

        if not user_installed_packages:
            print("No explicitly installed packages found!")
        else:
            print("Packages explicitly installed by the user:")
            for pkg in user_installed_packages:
                print(f"- {pkg}")
    else:
        logger.error(f"{dpkg_status_path} does not exist or is not accessible.")