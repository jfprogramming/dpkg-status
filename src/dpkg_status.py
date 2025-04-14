#!/usr/bin/env python3
import logging
import subprocess

"""
dpkg-status Parser Script

Description:
This Python3 script parses the `/var/lib/dpkg/status` file on Debian-based systems (e.g., Debian 12)
to extract packages explicitly installed by the user. It correlates data from the dpkg status file 
and `/var/lib/apt/extended_states` to identify packages that were manually installed, excluding dependencies 
and auto-installed packages.

Usage:
- Ensure that the `/var/lib/dpkg/status` file and `/var/lib/apt/extended_states` file exist and are accessible.
- Run the script on a Debian-based system to generate a list of user-installed packages.

Requirements:
- Python3
- Read permissions for the required files

Notes:
- This script is designed specifically for Debian-based systems and may not work correctly on other distributions.
- Modify the detection logic to accommodate more complex scenarios, if necessary.

Author:
Jesse Finn
"""

# Configure logging. Set logging level to DEBUG for verbose debugging output.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_dpkg_status(dpkg_status_path, auto_installed_packages):
    """
    Parses the dpkg status file to extract packages explicitly installed by the user.
    :param dpkg_status_path: Path to `/var/lib/dpkg/status` file.
    :param auto_installed_packages: Set of auto-installed package names (from extended_states or other sources).
    :return: Set of packages explicitly installed by the user.
    """
    explicitly_installed = set()  # Set to store explicitly user-installed packages

    try:
        # Open the dpkg status file in read mode with UTF-8 encoding for processing
        with open(dpkg_status_path, 'r', encoding='utf-8') as dpkg_file:
            # Iterate over each line in the dpkg status file to extract package metadata
            package_name = None
            package_installed = False

            for line in dpkg_file:
                line = line.strip()  # Remove leading/trailing whitespace from the line
                if line.startswith("Package:"):
                    # Extract the package name from the current line
                    package_name = line.split(":")[1].strip()
                    continue
                elif line.startswith("Status:") and "install ok installed" in line:
                    # Mark the package as installed
                    package_installed = True

                # Check for the end of a package block and evaluate its installation status
                if (line == "" or line.startswith("Package:")) and package_name:
                    if package_installed and package_name not in auto_installed_packages:
                        # Add the explicitly installed package to the set
                        explicitly_installed.add(package_name)
                        logger.debug(f"Added to explicitly installed: {package_name}")
                    else:
                        logger.debug(
                            f"Skipped package: {package_name} (Installed: {package_installed}, Auto-Installed: {package_name in auto_installed_packages})")

                    # Reset metadata variables for the next package block
                    package_installed = False

    except FileNotFoundError:
        # Log an error if the dpkg status file is not found
        logger.error(f"Error: {dpkg_status_path} not found.")
    return explicitly_installed


def parse_extended_states(extended_states_path):
    """
    Parses the extended_states file to extract auto-installed and manually installed packages.
    :param extended_states_path: Path to `/var/lib/apt/extended_states` file.
    :return: Tuple of sets (auto_installed_packages, manually_installed_packages).
    """
    auto_installed_packages = set()  # Set for auto-installed packages
    manual_packages_from_states = set()  # Set for manually installed packages

    try:
        # Open the extended_states file in read mode with UTF-8 encoding for processing
        with open(extended_states_path, "r", encoding="utf-8") as extended_file:
            # Iterate over each line in the extended_states file to extract package metadata
            package_name = None
            auto_installed = None

            for line in extended_file:
                line = line.strip()  # Remove leading/trailing whitespace from the line
                if line.startswith("Package:"):
                    # Extract the package name from the current line
                    package_name = line.split(":")[1].strip()
                    auto_installed = None  # Reset the auto-installed flag for the next package
                    logger.debug(f"Found package: {package_name}")
                    continue
                elif line.startswith("Auto-Installed:"):
                    # Parse the auto-installed flag from the current line
                    auto_installed = line.split(":")[1].strip() == "1"
                    logger.debug(f"  Auto-Installed: {auto_installed}")

                # Add the package to the appropriate set at the end of a package block
                if (line == "" or line.startswith("Package:")) and package_name:
                    if auto_installed is None:
                        # Handle missing Auto-Installed field by treating the package as manually installed
                        manual_packages_from_states.add(package_name)
                    elif auto_installed is True:
                        # Add the package to the auto-installed set
                        auto_installed_packages.add(package_name)
                        logger.debug(f"Added to auto-installed: {package_name}")
                    elif auto_installed is False:
                        # Add the package to the manually installed set
                        manual_packages_from_states.add(package_name)
                        logger.debug(f"Added to manually installed: {package_name}")

                    # Reset metadata for the next package block
                    auto_installed = None

    except FileNotFoundError:
        # Log a warning if the extended_states file is not found
        logger.warning(f"Warning: {extended_states_path} not found. Auto-installed data will be incomplete.")

    return auto_installed_packages, manual_packages_from_states


def get_apt_mark_showmanual():
    """
    Runs the `apt-mark showmanual` command to retrieve a list of manually installed packages.
    :return: Set of manually installed package names.
    """
    try:
        # Run the command and capture its output
        result = subprocess.run(["apt-mark", "showmanual"], stdout=subprocess.PIPE, check=True, text=True)
        return set(result.stdout.splitlines())
    except subprocess.CalledProcessError as e:
        # Log an error if the command fails
        logger.error(f"Error running apt-mark showmanual: {e}")
        return set()


def main():
    """
    Main function orchestrating the parsing of dpkg status and extended_states files,
    combining results with the `apt-mark showmanual` command, and outputting the final list of
    explicitly installed packages.
    """
    dpkg_status_path = "/var/lib/dpkg/status"
    extended_states_path = "/var/lib/apt/extended_states"

    # Parse extended_states for auto-installed and manually installed packages
    auto_installed_packages, manual_packages_from_states = parse_extended_states(extended_states_path)

    # Parse dpkg status for explicitly installed packages
    explicitly_installed_packages = parse_dpkg_status(dpkg_status_path, auto_installed_packages)

    # Get the list of packages returned by apt-mark showmanual
    apt_mark_manual = get_apt_mark_showmanual()

    # Convert set to list for displaying to console in one line for easier debugging
    explicitly_installed_list = list(explicitly_installed_packages)
    logger.debug(f"explicitly_installed_list: {explicitly_installed_list}")

    # Save results to a file and display them
    output_file = "explicitly_installed_packages.txt"
    try:
        # Open the output file in write mode with UTF-8 encoding
        with open(output_file, "w", encoding="utf-8") as file:
            print("Packages explicitly installed by the user:")
            file.write("Packages explicitly installed by the user:\n")
            # Display each package to the console & Write each package to the output file
            for pkg in sorted(explicitly_installed_packages):
                # Iterate over the final list of explicitly installed packages
                print(f"- {pkg}")
                file.write(f"- {pkg}\n")
        logger.info(f"Results saved to {output_file}")
    except Exception as e:
        # Log an error if writing to the file fails
        logger.error(f"Failed to save results to {output_file}: {e}")

    # Cross-check results for inconsistencies
    logger.info("\nCross-checking results for inconsistencies...")
    inconsistencies_found = False
    for pkg in explicitly_installed_packages:
        # Check if a package detected by the script is missing from `apt-mark showmanual`
        if pkg not in apt_mark_manual:
            logger.warning(f"Package {pkg} detected by the script but not listed by apt-mark showmanual.")
            inconsistencies_found = True
    for pkg in apt_mark_manual:
        # Check if a package listed by `apt-mark showmanual` is missing from the script's results
        if pkg not in explicitly_installed_packages:
            logger.warning(f"Package {pkg} listed by apt-mark showmanual but not detected by the script.")
            inconsistencies_found = True
    if not inconsistencies_found:
        # Log if no inconsistencies are found
        logger.info("No inconsistencies were found between the script's results and apt-mark showmanual.")


if __name__ == "__main__":
    main()