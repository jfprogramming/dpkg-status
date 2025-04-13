#!/usr/bin/env python3
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_dpkg_status(dpkg_status_path, auto_installed_packages):
    """
    Parses the dpkg status file to extract packages explicitly installed by the user.
    :param dpkg_status_path: Path to /var/lib/dpkg/status file.
    :param auto_installed_packages: Set of auto-installed package names (from extended_states or other sources).
    :return: Set of packages explicitly installed by the user.
    """

    # Create data Set() for storing package names for user explicitly installed packages
    # Does not allow duplicate elements.
    explicitly_installed = set()

    try:
        # Open the file in read mode with UTF-8 encoding
        with open(dpkg_status_path, 'r', encoding='utf-8') as dpkg_file:
            # Variables to store metadata pulled from file
            package_name      = None
            package_installed = False

            # Loop through the file line by line for processing
            for line in dpkg_file:
                # Remove any white space from the line to be evaluated
                line = line.strip()
                if line.startswith("Package:"):
                    # Parse the package name from the current line
                    package_name = line.split(":")[1].strip()
                    # Do not evaluate yet continue processing the next line
                    continue
                elif line.startswith("Status:") and "install ok installed" in line:
                    # Verified package is installed set package_installed flag to true
                    package_installed = True

                # End of package block check for explicit installation by user
                if (line == "" or line.startswith("Package:")) and package_name:
                    if package_installed and package_name not in auto_installed_packages:
                        # Add the package to the explicitly_installed data set for final output
                        explicitly_installed.add(package_name)
                        print(f"Added to explicitly installed: {package_name}")
                    else:
                        print(f"Skipped package: {package_name} (Installed: {package_installed}, Auto-Installed: {package_name in auto_installed_packages})")

                    # Reset metadat variables
                    package_name      = None
                    package_installed = False

    except FileNotFoundError:
        logger.error(f"Error: {dpkg_status_path} not found.")
    return explicitly_installed


def parse_extended_states(extended_states_path):
    """
    Parses the extended_states file to get auto-installed and manually installed package information.
    :param extended_states_path: Path to /var/lib/apt/extended_states file.
    :return: Set of auto-installed and manually installed packages.
    """

    # Create data Set() for storing package names for auto and manually installed packages
    # Does not allow duplicate elements.
    auto_installed_packages     = set()
    manual_packages_from_states = set()

    try:
        # Open the file in read mode with UTF-8 encoding
        with open(extended_states_path, "r", encoding="utf-8") as extended_file:
            # Variables to store metadata pulled from file
            package_name   = None
            auto_installed = None

            # Loop through the file line by line for processing
            for line in extended_file:
                # Remove any white space from the line to be evaluated
                line = line.strip()
                if line.startswith("Package:"):
                    # Parse the package name from the current line
                    package_name = line.split(":")[1].strip()
                    # Reset for the next package
                    auto_installed = None
                    print(f"Found package: {package_name}")
                    # Do not evaluate yet continue processing the next line
                    continue
                elif line.startswith("Auto-Installed:"):
                    # Store boolean value for if package was auto installed
                    auto_installed = line.split(":")[1].strip() == "1"
                    print(f"  Auto-Installed: {auto_installed}")

                # Add package to the appropriate set at the end of the block
                if (line == "" or line.startswith("Package:")) and package_name:
                    if auto_installed is None:
                        # Handle missing Auto-Installed field
                        manual_packages_from_states.add(package_name)
                    elif auto_installed is True:
                        # Add package name to list of auto install packages
                        auto_installed_packages.add(package_name)
                        print(f"Added to auto-installed: {package_name}")
                    elif auto_installed is False:
                        # Add package name to list of manually user installed packages
                        manual_packages_from_states.add(package_name)
                        print(f"Added to manually installed: {package_name}")

                    # Reset metadat variables
                    package_name   = None
                    auto_installed = None

        # Output the lists in a readable format for debugging
        print("Auto-Installed Packages:")
        for pkg in sorted(auto_installed_packages):
            print(f"  - {pkg}")

        print("\nManually Installed Packages (from extended states):")
        for pkg in sorted(manual_packages_from_states):
            print(f"  - {pkg}")

    except FileNotFoundError:
        logger.warning(f"Warning: {extended_states_path} not found. Auto-installed data will be incomplete.")

    return auto_installed_packages, manual_packages_from_states


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


def main():
    dpkg_status_path     = "/var/lib/dpkg/status"
    extended_states_path = "/var/lib/apt/extended_states"

    # Parse extended_states for auto and manual packages
    auto_installed_packages, manual_packages_from_states = parse_extended_states(extended_states_path)

    # Parse dpkg status for explicitly installed packages
    explicitly_installed_packages = parse_dpkg_status(dpkg_status_path, auto_installed_packages)

    # Combine results with apt-mark showmanual
    apt_mark_manual = get_apt_mark_showmanual()
    final_explicitly_installed = explicitly_installed_packages.union(manual_packages_from_states, apt_mark_manual)

    # Display results
    print("Packages explicitly installed by the user:")
    for pkg in sorted(final_explicitly_installed):
        print(f"- {pkg}")

    # Optional: Log inconsistencies
    logger.info("\nCross-checking results...")
    for pkg in explicitly_installed_packages:
        if pkg not in apt_mark_manual:
            logger.warning(f"Package {pkg} detected by the script but not listed by apt-mark showmanual.")
    for pkg in apt_mark_manual:
        if pkg not in explicitly_installed_packages:
            logger.warning(f"Package {pkg} listed by apt-mark showmanual but not detected by the script.")


if __name__ == "__main__":
    main()