# **dpkg-status**

`dpkg-status` is a Python3 script for parsing and analyzing the `/var/lib/dpkg/status` file on Debian-based systems. The script identifies packages explicitly installed by the user, excluding dependencies and auto-installed packages.

---

## **Table of Contents**

1. [Installation](#installation)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [System Requirements](#system-requirements)
5. [Project Configuration](#project-configuration)
6. [Detection Algorithm](#detection-algorithm)
7. [Notes on Key Files](#notes-on-key-files)
8. [Qt Application: `appdpkg-status`](#qt-application-appdpkg-status)
9. [Releases](#releases)
10. [Troubleshooting](#troubleshooting)

---

## **1. Installation**

### **Option 1: Install `.deb` Package via GitHub Release**

1. Download the `.deb` Package:
   - ```bash
     wget https://github.com/jfprogramming/dpkg-status/releases/download/v1/dpkg-status-1.0.0-Linux.deb
     ```

2. Install the Package:
   - Using dpkg to install
     ```bash
     sudo dpkg -i dpkg-status-1.0.0-Linux.deb
     
     # use to install missing qt dependencies
     sudo apt -f install
     ```
   - Using apt to install
     ```bash
     sudo apt-get install ./dpkg-status-1.0.0-Linux.deb
     # use to install missing qt dependencies
     sudo apt -f install
     ```

3. Run the Qt GUI Application:
   - ```bash 
     appdpkg-status
     ``` 
   - select the button "run script" on the Qt GUI Application 

4. Run the Python Script without Qt GUI Application:
   - ```bash
     /usr/share/appdpkg-status/dpkg_status.py
     ```

### **Option 2: Install via Cloning the Repository**

1. Clone the repository:
   - ```bash
     git clone https://github.com/jfprogramming/dpkg-status.git
     cd dpkg-status
     ```

2. Install dependencies and build the `.deb` package:
   - Using dpkg to install
     ```bash
     cd releases/
     sudo dpkg -i dpkg-status-1.0.0-Linux.deb
     # use to install missing qt dependencies
     sudo apt-get install -f
     ```
   - Using apt to install
     ```bash
     sudo apt-get install ./dpkg-status-1.0.0-Linux.deb
     # use to install missing qt dependencies
     sudo apt-get install -f
     ```
     
3. Run the Qt GUI Application:
   - ```bash 
     appdpkg-status
     ``` 
   - select the button "run script" on the Qt GUI Application 

4. Run the Python Script without Qt GUI Application:
   - ```bash
     /usr/share/appdpkg-status/dpkg_status.py
---

## **2. Features**

- Parses `/var/lib/dpkg/status` to list explicitly installed packages.
- Leverages `/var/lib/apt/extended_states` for analyzing auto-installed packages.
- Integrates with `apt-mark showmanual` for script accuracy.

---

## **3. Prerequisites**

To successfully run the script, ensure the following prerequisites are met:

1. **Operating System**: Debian-based system (e.g., Debian 12, Ubuntu, Linux Mint).
2. **Python**: Version 3.6 or newer.
3. **Required Files**:
   - `/var/lib/dpkg/status`
   - `/var/lib/apt/extended_states`
4. **Permissions**: Read access to `/var/lib/dpkg/status` and `/var/lib/apt/extended_states`.

---

## **4. System Requirements**

- **Memory**: Minimum 512 MB of RAM.
- **Disk Space**: Minimal (only requires access to `/var/lib/dpkg/` and `/var/lib/apt/`).
- **Linux Distribution**: Compatible with all Debian-based distributions.
- **Commands**: python3.10, pip, wget and git command line utilities 

---

## **5. Project Configuration**

Follow these steps to set up the project for development:

1. Clone the repository:
   ```bash
   git clone https://github.com/jfprogramming/dpkg-status.git
   cd dpkg-status
   ```
   
2. Project directory structure:
   ```plaintext
   dpkg-status/
   ├── qt/
   │   ├── build
   │   ├── qml
   │   ├── main.cpp
   │   ├── dpkg_status.py
   │   ├── install
   │   ├── compat
   ├── src/
   │   ├── dpkg_status.py
   ├── tests/
   │   ├── test_dpkg_status.py
   ├── releases/
   │   ├── dpkg-status-<version>-Linux.deb
   ├── README.md
   ```

3. (Optional) Set up a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies, if required:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the script:
   ```bash
   ./dpkg_status.py
   ```

---

## **6. Detection Algorithm**

The script determines explicitly installed packages by analyzing various system files. It follows these steps:

1. **Parse `/var/lib/dpkg/status`**:
   - Extract package names, statuses, and metadata (e.g., `Status: install ok installed`).

2. **Filter Auto-Installed Packages**:
   - Checks `/var/lib/apt/extended_states` for `Auto-Installed: 1` markers and excludes those packages.

3. **Compare with `apt-mark showmanual`** *(optional)*:
   - Includes packages manually marked as installed via `apt-mark`.

4. **Identify Explicitly Installed Packages**:
   - Packages are explicitly installed if:
     - `Status: install ok installed` in `/var/lib/dpkg/status`.
     - Not listed as `Auto-Installed: 1` in `/var/lib/apt/extended_states`.
     - Included in `apt-mark showmanual` output (if applicable).

5. **Final Output**:
   - Outputs a deduplicated list of explicitly installed packages.
   - The script saves the list of explicitly installed packages to /tmp/explicitly_installed_packages.txt file
     - ```bash 
       /tmp/explicitly_installed_packages.txt
       ``` 

---

## **7. Notes on Key Files**

### **/var/lib/dpkg/status**
- Tracks every package installed on the system, along with its metadata.
- Acts as the backend database for Debian's `dpkg` package manager.

### **/var/lib/apt/extended_states**
- Used by APT to track extra metadata (e.g., whether a package is auto-installed as a dependency).
- Packages with `Auto-Installed: 1` are considered dependencies.

### **APT Log Files**
- `/var/log/apt/history.log`: Details high-level actions (installations, upgrades, removals).
- `/var/log/apt/term.log`: Tracks detailed command outputs.
- `/var/log/dpkg.log`: Logs actions performed by `dpkg` directly.

---

## **8. Qt Application: `appdpkg-status`**

`appdpkg-status` is an optional Qt-based GUI for visualizing the Python script's output.

### **Features**:
- Displays parsed results in an interactive table.
- Responsive UI built with QML for modern design.
- Pre-integrated with `dpkg_status.py` for seamless backend processing.

### **Running the Qt App**:
3. After installing the `.deb` package:
   ```bash
   appdpkg-status
   ```

4. Debugging:
   - Possible packages need to run qt *appdpkg-status* app on Target Debian 12 system
   ```bash
   sudo apt install git
                    wget
   ```
   
   - If the application doesn't run, rebuild, repackage and reinstall deb package
     

## Using `cpack` to Bundle Qt Libraries and Generate .deb package

To package the `appdpkg-status` binary with its required Qt libraries and dependencies, follow these steps:

1. **Configure CMakeList.txt file**:
   - Ensure CMakeList file is configured for cpack:
     - set(CPACK_PACKAGE_NAME "dpkg-status")
     - set(CPACK_PACKAGE_VERSION "1.0.0")
     - set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "A tool for managing dpkg status files")
     - set(CPACK_DEBIAN_PACKAGE_MAINTAINER "Full Name <Email>")
     - set(CPACK_PACKAGE_HOMEPAGE_URL "https://example.com")
     - set(CPACK_PACKAGE_LICENSE "MIT")
     - set(CPACK_GENERATOR "DEB")
     - set(CPACK_DEBIAN_PACKAGE_DEPENDS "libqt6core6, libqt6gui6, libqt6qml6, python3")
     - set(CPACK_PACKAGING_INSTALL_PREFIX "/usr")
     - include(CPack)
     - install(TARGETS appdpkg-status DESTINATION bin)
     - install(DIRECTORY ${CMAKE_SOURCE_DIR}/qml DESTINATION share/appdpkg-status)
     - install(FILES ${CMAKE_SOURCE_DIR}/dpkg_status.py DESTINATION share/appdpkg-status PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ WORLD_EXECUTE WORLD_READ)

    
2. **Configure the project:**
   - ```bash
     cmake ..
     ```

3. **Build the project**:
   - ```bash
     make
     ```

4. **Package with CPack**:
   - ```bash
     cpack -G DEB
     ```
     
5. **Copy deb package**
   - Copy the deb package to the release folder for upload to GitHub 
   - Create a new release, add tag, add notes and upload deb file created 
 

### Known Anomalies and Bugs:
   - Dependency on Qt 6.2.4
     - install any missing dependencies  
---

## **9. Releases**

### **Creating a `.deb` Package**:
1. Releases are created and tested local
   - build and test the deb package locally
   
2. Publish on GitHub:
   - Attach the `.deb` package to a GitHub release with appropriate release notes.
   - update readme with latest version of deb package to install 

---

## **10. Troubleshooting**

### **General Issues & Debugging**:
- **Missing Dependencies**:
  ```bash
  sudo apt-get install -f
  ```

- **Reinstall the Package**:
  ```bash
  sudo dpkg -r dpkg-status
  sudo dpkg -i dpkg-status-1.0.0-Linux.deb
  ```
  
- **Verify installed script**:
   ```bash
   ls -l /usr/bin/appdpkg-status
   ls -l /usr/bin/appdpkg-status/
   ```
  
### **Qt Debugging Settings**:
1. Enable debug logging for Qt GUI App:
   ```plaintext
   logging.basicConfig(level=logging.DEBUG)
   ```

---
