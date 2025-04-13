#!/usr/bin/env python3
import os
import argparse
import logging
import subprocess

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


def parse_extended_states(extended_states_path):
    """
    Parses the extended_states file to get auto-installed and manually installed package information.
    :param extended_states_path: Path to /var/lib/apt/extended_states file.
    :return: Tuple of sets (auto_installed_packages, manual_packages).
    """
    auto_installed_packages = set()
    manual_packages = set()
    try:
        with open(extended_states_path, "r", encoding="utf-8") as extended_file:
            package_name = None
            auto_installed = None  # None means no info yet

            for line in extended_file:
                line = line.strip()
                if line.startswith("Package:"):
                    package_name = line.split(":")[1].strip()
                    auto_installed = None  # Reset for the next package
                elif line.startswith("Auto-Installed:"):
                    auto_installed = line.split(":")[1].strip() == "1"

                # Add package to the appropriate set at the end of the block
                if (line == "" or line.startswith("Package:")) and package_name:
                    if auto_installed is True:
                        auto_installed_packages.add(package_name)
                    elif auto_installed is False:  # Explicitly marked as manually installed
                        manual_packages.add(package_name)
                    package_name = None
                    auto_installed = None
    except FileNotFoundError:
        logger.error(f"Error: {extended_states_path} not found.")
    return auto_installed_packages, manual_packages


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
                line = line.strip()
                if line.startswith("Package:"):
                    package_name = line.split(":")[1].strip()
                elif line.startswith("Status:") and "install ok installed" in line:
                    package_installed = True

                # Add package at the end of block or when reaching a new package
                if (line == "" or line.startswith("Package:")) and package_name:
                    if package_installed and package_name in manual_packages:
                        explicitly_installed.add(package_name)
                    package_name = None
                    package_installed = False
        return list(explicitly_installed)
    except FileNotFoundError:
        logger.error(f"Error: {dpkg_status_path} not found.")
        return []


def get_apt_mark_showmanual():
    """
    Uses the `apt-mark showmanual` command to get a list of manually installed packages.
    :return: Set of manually installed package names.
    """
    try:
        result = subprocess.run(["apt-mark", "showmanual"], stdout=subprocess.PIPE, check=True, text=True)
        return set(result.stdout.splitlines())
    except subprocess.CalledProcessError as e:
        logger.error("Error running apt-mark showmanual: %s", e)
        return set()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse dpkg status and extended states files.")
    parser.add_argument('--status', default='/var/lib/dpkg/status', help='Path to dpkg status file')
    parser.add_argument('--states', default='/var/lib/apt/extended_states', help='Path to extended states file')
    args = parser.parse_args()

    dpkg_status_path = args.status
    extended_states_path = args.states

    if os.path.exists(dpkg_status_path) and os.access(dpkg_status_path, os.R_OK):
        # Get auto-installed and manually installed packages from extended_states
        auto_installed_packages, manual_packages_from_states = parse_extended_states(extended_states_path)
        # Get explicitly installed packages from dpkg status
        user_installed_packages = parse_dpkg_status(dpkg_status_path, auto_installed_packages.union(manual_packages_from_states))
        # Cross-check with apt-mark showmanual
        apt_mark_manual = get_apt_mark_showmanual()

        # Print results
        print("Packages explicitly installed by the user:")
        for pkg in sorted(user_installed_packages):
            print(f"- {pkg}")

        # Optional: Compare with apt-mark showmanual and log inconsistencies
        print("\nCross-checking with apt-mark showmanual...")
        for pkg in sorted(user_installed_packages):
            if pkg not in apt_mark_manual:
                logger.warning(f"Package {pkg} not listed by apt-mark showmanual.")
        for pkg in sorted(apt_mark_manual):
            if pkg not in user_installed_packages:
                logger.warning(f"Package {pkg} listed by apt-mark showmanual but not detected by the script.")
    else:
        logger.error(f"{dpkg_status_path} does not exist or is not accessible.")