# **dpkg-status**

`dpkg-status`  is a Python3 script for parsing and analyzing the `/var/lib/dpkg/status` file on Debian-based systems. 
  - The script identifies packages explicitly installed by the user, excluding dependencies. 
  - Below are the current details of the project.

---

## **Table of Contents**
1. [Introduction](#introduction)
2. [Installation](#installation)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [System Requirements](#system-requirements)
5. [Project Configuration](#project-configuration)
6. [Detection Algorithm](#detection-algorithm)
7. [Notes on Key Files](#notes-on-key-files)
8. [Qt Application: `appdpkg-status`](#qt-application-appdpkg-status)
9. [Releases](#releases)
10. [Troubleshooting](#troubleshooting)

## **1. Introduction**

This repository contains:
- A Python3 script for managing `dpkg status` files.
- A Qt-based application for rendering and managing dependencies.
- Supporting scripts for environment setup and packaging.

The project is designed to simplify dependency management and application packaging for Debian-based systems.

---

---

## **2. Installation**

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
     ```
   - If deb fails to install due to dependencies, use apt to fix installation
     ```bash
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

## **3. Features**

- Parses `/var/lib/dpkg/status` to list explicitly installed packages.
- Leverages `/var/lib/apt/extended_states` for analyzing auto-installed packages.
- Integrates with `apt-mark showmanual` for script report verification.

---

## **4. Prerequisites**

To successfully run the script, ensure the following prerequisites are met:

1. **Operating System**: Debian-based system (e.g., Debian 12, Ubuntu, Linux Mint).
2. **Python**: Version 3.6 or newer.
3. **Required Files**:
   - `/var/lib/dpkg/status`
   - `/var/lib/apt/extended_states`
4. **Permissions**: Read access to `/var/lib/dpkg/status` and `/var/lib/apt/extended_states`.

5. **CMAKE Defined Package Dependencies**: 
    - `libqt6core6`, `libqt6gui6`, `libqt6qml6`, `python3`,
      `libwayland-client0`, `libwayland-cursor0`, `libwayland-egl1`,
      `libxcb-cursor0`, `libxcb1`, `libx11-xcb1`, `libxcb-util1`,
      `libxcb-xkb1, libxkbcommon0`, `libxkbcommon-x11-0`,
      `libxcb-cursor-dev`, `binutils`, `libglx-mesa0`, `libopengl-dev`,
      `qml-module-qtquick2`, `qml-module-qtquick-controls2`, `qml-module-qtquick-layouts`.

6. **The following dependencies are automatically installed using `sudo apt-get -f install`**:
    - `binutils`, `binutils-common`, `binutils-x86-64-linux-gnu`, `libb2-1`,
      `libbinutils`, `libctf-nobfd0`, `libctf0`, `libdouble-conversion3`,
      `libgprofng0`, `libmd4c0`, `libpcre2-16-0`, `libpthread-stubs0-dev`,
      `libqt5core5a`, `libqt5dbus5`, `libqt5gui5`, `libqt5network5`,
      `libqt5qml5`, `libqt5qmlmodels5`, `libqt5qmlworkerscript5`, `libqt5quick5`,
      `libqt5quickcontrols2-5` ,`libqt5quicktemplates2-5` ,`libqt5svg5`, `libqt5waylandclient5`,
      `libqt5waylandcompositor5` ,`libqt5widgets5`, `libqt6core6`, `libqt6dbus6`,
      `libqt6gui6`, `libqt6network6`, `libqt6qml6`, `libts0`,
      `libxau-dev`, `libxcb-cursor-dev`, `libxcb-cursor0`, `libxcb-image0-dev`,
      `libxcb-render-util0-dev` ,`libxcb-render0-dev`  ,`libxcb-shm0-dev`, `libxcb-xinerama0`,
      `libxcb-xinput0`, `libxcb1-dev`, `libxdmcp-dev`, `qml-module-qtquick-controls2`,
      `qml-module-qtquick-layouts` ,`qml-module-qtquick-templates2` ,`qml-module-qtquick2`,
      `qt5-gtk-platformtheme`, `qt6-gtk-platformtheme` ,`qt6-qpa-plugins`, `qt6-translations-l10n` ,
      `qttranslations5-l10n`, `qtwayland5`, `x11proto-dev`, `xorg-sgml-doctools`.

---

## **4. System Requirements**

- **Memory**: Minimum 512 MB of RAM.
- **Disk Space**: Minimal (only requires access to `/var/lib/dpkg/` and `/var/lib/apt/`).
- **Linux Distribution**: Compatible with all Debian-based distributions.
- **Commands**: python3.10, pip, apt, dpkg, wget and git command line utilities 

---

## **5. Project Configuration & Development Environment Setup**

Follow these steps to set up the project for development:

1. Install Qt 6.7 or newer in `/opt/Qt`:
    - Download the installer from the Qt website and follow the installation instructions.

2. Set up a project directory
    - ```bash 
      mkdir ~/Projects/
      ```
3. Clone the repository:
   - ```bash
     git clone https://github.com/jfprogramming/dpkg-status.git
     cd dpkg-status
     ```
   
2. Project directory structure:
   ```plaintext
   dpkg-status/
   ├── qt/
   │   ├── build
   │   │   ├── lib
   │   │   ├── plugins 
   │   │   ├── qml
   │   ├── qml
   │   │   ├── Main.qml
   │   ├── CMakelist.txt
   │   ├── main.cpp
   │   ├── dpkgmodeldata.cpp
   │   ├── dpkgmodeldata.h
   │   ├── dpkg_status.py
   │   ├── set-target-env-vars.sh
   │   ├── find_libs.sh
   │   ├── icon.png 
   │   ├── defualt.desktop
   │   ├── README.md
   │   ├── vm_settings.png
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
