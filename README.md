# **dpkg-status**

`dpkg-status`  is a Python3 script for parsing and analyzing the `/var/lib/dpkg/status` file on Debian-based systems. 
  - The script identifies packages explicitly installed by the user, excluding dependencies. 
  - Below are the current details of the project.

---

## **Table of Contents**
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Features](#features)
4. [Prerequisites](#prerequisites)
5. [System Requirements](#system-requirements)
6. [Project Configuration & Development Environment Setup](#project-configuration--development-environment-setup)
7. [Setting up a Target Debian 12 VM for Testing](#setting-up-a-target-debian-12-vm-for-testing)
8. [Detection Algorithm](#detection-algorithm)
9. [Notes on Key Files](#notes-on-key-files)
10. [Qt Application: `appdpkg-status`](#qt-application-appdpkg-status)
11. [GitHub Actions](#github-actions)
12. [Releases](#releases)
13. [Troubleshooting](#troubleshooting)
14. [License](#license)

## **1. Introduction**

This repository contains:
- A Python3 script for managing `dpkg status` files.
- A Qt-based application for display results of the `dpkg_status.py` script.
- Supporting scripts for environment setup and installation.

The project is designed to report packages installed on Debian-based systems.

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
   - The Python script includes a shebang `(#!/usr/bin/env python3)` at the top and can be executed directly:
   - ```bash
     /usr/share/appdpkg-status/dpkg_status.py
     ```
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

## **5. System Requirements**

- **Memory**: Minimum 512 MB of RAM.
- **Disk Space**: Minimal (only requires access to `/var/lib/dpkg/` and `/var/lib/apt/`).
- **Linux Distribution**: Compatible with all Debian-based distributions.
- **Commands**: `python3.10`, `pip`, `apt`, `dpkg`, `wget` and `git` command line utilities 

---

## **6. Project Configuration & Development Environment Setup**

Follow these steps to set up the project for development:

1. Install Qt 6.7 or newer in `/opt/Qt`:
    - Download the installer from the Qt website and follow the installation instructions.

2. Set up a project directory
    - ```bash 
      mkdir ~/Projects/
      ```
      
3. Install development tools
    - `sudo apt-get install git cmake build-essential` 
   
4. Clone the repository:
   - ```bash
     git clone https://github.com/jfprogramming/dpkg-status.git
     cd dpkg-status
     ```
   
5. Project directory structure:
   - ```plaintext
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
        │   ├── requirements.txt
        ├── tests/
        │   ├── test_dpkg_status.py
        ├── releases/
        │   ├── dpkg-status-<version>-Linux.deb
        ├── README.md
     ```

6. (Optional) Set up a virtual environment:
   - ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

7. Install dependencies, if required:
   - ```bash
     pip install -r requirements.txt
     ```

8. Run the python script:
   - ```bash
     ./dpkg_status.py
     ```
   
9. Qt Creator Project Setup and Build Settings
    - Development Environment: Ubuntu 22.04
    - Qt Version: 6.7.2
    - Installation Path: /opt/Qt
   
10. Qt Build Settings
    - To build the project and create a Debian package, add additional build parameters:
      - `-v --target custom_package -j4` 
    - Run Environment configuration 
      - set `LD_LIBRARY_PATH` to Qt's installation directory
        -  Ex. `LD_LIBRARY_PATH=/opt/Qt/6.7.2/gcc_64/lib/`

---

## **7. Setting up a Target Debian 12 VM for Testing**

1. Set up a virtual machine with Debian 12 Operating system
   - https://www.debian.org/download
   - Install the operating system set up a user.
     - Download the deb package, install and test and changes on a clean target system.
     - Install dependencies and run application.
       - ```bash
         sudo dpkg -i dpkg-status-1.0.0-Linux.deb
         # use to install missing qt dependencies
         sudo apt-get install -f
         ```
       - Install Directories
         - `/usr/bin/appdpkg-status`:
           - This is where the main executable binary (or launcher script) for Qt application resides. 
           - The file *appdpkg-status* is typically the entry point for users to run the application directly from the terminal or desktop environment. 
           - When a user runs the command appdpkg-status, it executes this binary or script. 
         - `/usr/share/appdpkg-status/`:
           - This directory is used to store shared resources and data files for the application.
           - Python scripts (dpkg_status.py or other backend scripts) for processing.
           - QML files for the Qt GUI (e.g., UI components and layouts).
           - Static assets like icons, images, or translations are used by the application.
           - It ensures that the application’s data files are accessible system-wide without being tied to a specific user.
         - `/usr/lib/appdpkg-status/:`
           - This directory is typically used for application-specific libraries or modules.
           - Shared libraries required by the application, such as compiled `.so` files.
           - Dependency files specific to the application's runtime.
           - These libraries are used internally by the application to ensure that all required dependencies are available without conflicting with the system's global libraries.
         - *How the Directories Work Together*
           - The `appdpkg-status` binary in `/usr/bin/` acts as the main launcher. 
             - Loads and runs backend scripts or logic located in `/usr/share/appdpkg-status/`. 
             - Dynamically links or loads any required libraries from `/usr/lib/appdpkg-status/`.
           - This separation ensures:
             - *Modularity*: Code, resources, and libraries are organized logically.
             - *System Integrity*: Libraries and scripts are isolated, preventing conflicts with system-wide components.
             - *Ease of Maintenance*: Updates or bug fixes can target specific directories without affecting the entire system.
   - Setting up ENV Variables: 
     - The deb package should automatically run the `set-target-env-vars.sh`
       - if needed the script can be run manually to it should write the changes to the `bashrc` profile.
         - `/usr/share/appdpkg-status/set-target-env-vars.sh`  
           - `export QML2_IMPORT_PATH="/usr/share/appdpkg-status/qml/`
           - `export LD_LIBRARY_PATH="/usr/lib/appdpkg-status/:$LD_LIBRARY_PATH`
           - `export QT_PLUGIN_PATH="/usr/lib/appdpkg-status/:$QT_PLUGIN_PATH`
           - `export QT_QUICK_BACKEND="software"`
     - *NOTE:* these environment variables are necessary for the Qt GUI Application to run.
   - **Rendering Backend**
     - The rendering in the Qt application is configured to use `QT_QUICK_BACKEND="software"` 
     - This setting allows for compatibility across systems without depending on XCB, Wayland, or OpenGL.

---

## **8. Detection Algorithm**

The script determines explicitly installed packages by analyzing various system files. It follows these steps:

1. **Parse `/var/lib/dpkg/status`**:
   - Extract package names, statuses, and metadata (e.g., `Status: install ok installed`).

2. **Filter Auto-Installed Packages**:
   - Checks `/var/lib/apt/extended_states` for `Auto-Installed: 1` markers and excludes those packages.

3. **Compare with `apt-mark showmanual`** *(optional)*:
   - Utility `apt-mark showmanual` used to verify pyhton3 script results.

4. **Identify Explicitly Installed Packages**:
   - Packages are explicitly installed if:
     - `Status: install ok installed` in `/var/lib/dpkg/status`.
     - Not listed as `Auto-Installed: 1` in `/var/lib/apt/extended_states`.
     - Validated against `apt-mark showmanual` output (if applicable).

5. **Final Output**:
   - Outputs a deduplicated list of explicitly installed packages.
   - The script saves the list of explicitly installed packages to `/tmp/explicitly_installed_packages.txt` file
     - ```bash 
       /tmp/explicitly_installed_packages.txt
       ``` 

---

## **9. Notes on Key Files**

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

## **10. Qt Application: `appdpkg-status`**

`appdpkg-status` is an optional Qt-based GUI for visualizing the Python script's output.

### **Features**:
- Displays parsed results in an interactive table.
- Responsive UI built with QML for modern design.
- Pre-integrated with `dpkg_status.py` for seamless backend processing.

### **Running the Qt App**:
3. After installing the `.deb` package:
   - ```bash
     appdpkg-status
     ```

4. Debugging:
   - Possible packages need to run qt *appdpkg-status* app on Target Debian 12 system
   - Check `appdpkg-satus` application library dependencies 
   - ```bash
     ldd appdpkg-status
     dpkg -c dpkg-status-<version>-Linux.deb
     ```     

### Using `cpack` to Bundle Qt Libraries and Generate .deb package

###**Packaging the Application with LinuxDeployQt and CPack**

This section explains how the project's `CMakeLists.txt` file, project structure, and `.deb` package work together with **LinuxDeployQt** and **CPack** to package the Qt application.

---

### **Using LinuxDeployQt**

#### **What is LinuxDeployQt?**
LinuxDeployQt is a tool for bundling Qt applications with their dependencies. It ensures the application is portable and includes all necessary Qt libraries and plugins to run on a target system.

#### **How It Works**
1. **Qt Application Binary**:
   - The Qt application binary (`appdpkg-status`) is built and located in the `/usr/bin/` directory.
   - LinuxDeployQt scans the binary to identify its dependencies, such as Qt modules and libraries.

2. **QML Directory**:
   - The `-qmldir` option specifies the directory containing QML files.
   - For example: `/path/to/qml` is scanned to ensure all required QML components are included.

3. **AppImage Creation** (Optional):
   - LinuxDeployQt can generate an AppImage for broader portability.
   - Example command:
     ```bash
     linuxdeployqt appdpkg-status -appimage -qmldir=/path/to/qml
     ```
   - This step is optional if you only need a `.deb` package.

---

### **Using CPack**

#### **Description**
  - *CPack* is a tool integrated with CMake that automates the creation of software packages. 
  - It supports multiple formats, including `.deb` packages for Debian-based Linux distributions.

#### **How CPack Workst**
1. **Configuration in `CMakeLists.txt`**:
   - The `CMakeLists.txt` file includes specific configurations for CPack. Below are some key configurations:
     ```cmake
     set(CPACK_PACKAGE_NAME "dpkg-status")
     set(CPACK_PACKAGE_VERSION "1.0.0")
     set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "A tool for managing dpkg status files")
     set(CPACK_DEBIAN_PACKAGE_MAINTAINER "Your Name <your.email@example.com>")
     set(CPACK_PACKAGE_HOMEPAGE_URL "https://github.com/jfprogramming/dpkg-status")
     set(CPACK_PACKAGE_LICENSE "MIT")
     set(CPACK_GENERATOR "DEB")
     set(CPACK_DEBIAN_PACKAGE_DEPENDS "libqt6core6, libqt6gui6, libqt6qml6, python3")
     set(CPACK_PACKAGING_INSTALL_PREFIX "/usr")
     include(CPack)
     ```
     - **Package Name and Version**: Defines the name (`dpkg-status`) and version (`1.0.0`) of the package.
     - **Dependencies**: Lists required dependencies like `libqt6core6`, `libqt6gui6`, and `python3`.
     - **Install Prefix**: Specifies `/usr` as the root directory for installation.
     - **Package Format**: `CPACK_GENERATOR` is set to `DEB` to create a Debian package.
     - **Maintainer and License**: Adds metadata for the package.

2. **Installation Directories**:
   - The `install` commands in the `CMakeLists.txt` specify where files are placed in the package:
     ```cmake
     install(TARGETS appdpkg-status DESTINATION bin)
     install(DIRECTORY ${CMAKE_SOURCE_DIR}/qml DESTINATION share/appdpkg-status)
     install(FILES ${CMAKE_SOURCE_DIR}/dpkg_status.py DESTINATION share/appdpkg-status PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ WORLD_EXECUTE WORLD_READ)
     ```
     - **Binary**: The application binary (`appdpkg-status`) is installed in `/usr/bin/`.
     - **Resources**: QML files and Python scripts are installed in `/usr/share/appdpkg-status/`.

3. **Generating the `.deb` Package**:
   - Once the build is complete, run CPack to generate the `.deb` package:
     ```bash
     cpack -G DEB
     ```
   - This creates a `.deb` package in the build directory, which can be distributed and installed on Debian-based systems.
   - Note: parameters will build `.deb` by default. 
---

### **How the Components Work Together**

1. **Project Structure**:
   - This project is organized to separate binaries, resources, and libraries into standard directories:
     ```
     /usr/bin/appdpkg-status          # Main executable binary
     /usr/share/appdpkg-status/       # QML files and Python scripts
     /usr/lib/appdpkg-status/         # Shared libraries (if any)
     ```

2. **CMake Configuration**:
   - The `CMakeLists.txt` file defines how the project is built, where files are installed, and how the package is created.

3. **LinuxDeployQt**:
   - LinuxDeployQt ensures all Qt libraries and plugins required by `appdpkg-status` are included in the package.

4. **CPack**:
   - CPack bundles everything into a `.deb` package, providing an easy way to distribute and install the application on Debian-based systems.

--- 

### Using RPATH
  - RPATH (Runtime Library Search Path) is used to define library paths at runtime for the application. 
  - This ensures that the application can locate required shared libraries during execution.
  - Even if the libraries are not installed in standard system paths.

#### Configuring RPATH in `CMakeLists.txt`
  - Below are the configurations to enable and use RPATH in the `CMakeLists.txt` file:
  - ```cmake
    set(CMAKE_SKIP_BUILD_RPATH FALSE)
    set(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)
    set(CMAKE_INSTALL_RPATH "$ORIGIN/../lib")
    set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
    ```
  - *Explanation of Configurations*:
    - `CMAKE_INSTALL_RPATH`:
      - Defines the runtime library path relative to the executable.
    - `$ORIGIN` 
      - Is a placeholder for the directory containing the executable.
    - `CMAKE_INSTALL_RPATH_USE_LINK_PATH:`
      - Ensures that the RPATH includes all linked libraries. 
  - Advantages of RPATH
    - Simplifies library loading by embedding the library paths directly into the executable.
    - Avoids the need to set environment variables like LD_LIBRARY_PATH at runtime.

#### Testing RPATH
  - To verify the RPATH in the binary, use the readelf command:
    - ```bash
      readelf -d /path/to/appdpkg-status | grep RPATH
      ```

---

### Manual Build Steps VIA CMD Line  
To package the `appdpkg-status` binary with its required Qt libraries and dependencies, follow these steps:

1. **Configure CMakeList.txt file**:
   - Ensure `CMakeList` file is configured for `linuxdeployqt` and `cpack`.
    
2. **Configure the project:**
   - ```bash
     cmake .. -DCMAKE_INSTALL_RPATH="$ORIGIN/lib;/opt/Qt/6.7.2/gcc_64/lib"
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
   - Create a new release, add tag, add notes.
   - Upload the deb file created to the GitHub release created
 

### Known Anomalies and Bugs:
   - Dependencies on Qt 6
     
---

## **11. GitHub Actions**
  - The project uses *GitHub Actions* for Continuous Integration (CI) and Continuous Deployment (CD). 
  - The CI/CD pipeline builds the project, runs tests, and packages the application.

--- 

## **12. Releases**

### **Creating a `.deb` Package**:
1. Releases are created and tested local
   - build and test the deb package locally
   
2. Publish on GitHub:
   - Attach the `.deb` package to a GitHub release with appropriate release notes.
   - update readme with the latest version of the deb package to install 

---

## **13. Troubleshooting**

### **General Issues & Debugging**:
- **Missing Dependencies**:
  - ```bash
    sudo apt-get install -f
    ```

- **Reinstall the Package**:
  - ```bash
    sudo dpkg -r dpkg-status
    sudo dpkg -i dpkg-status-1.0.0-Linux.deb
    ```
  
- **Verify installed script**:
   - Check directories for application binary, supporting scripts and libraries 
     - `/usr/bin/appdpkg-status`
     - `/usr/share/appdpkg-status`
     - `/usr/lib/appdpkg-status`
   - run the `set-target-env.vars.sh` script to set up env vars need to run Qt GUI App. 
     - `/usr/share/appdpkg-status/set-target-env.vars.sh`
   - Set Plugin debug Env. Var and re-run application
     - ```bash 
       export QT_DEBUG_PLUGINS=1
       appdpkg-status
       ``` 
  
### **Python3 Script Debugging**:
1. Enable debug logging for Python3 Script:
   - ```plaintext
     logging.basicConfig(level=logging.DEBUG)
     ```
---

## **14. License**
  - This project is licensed under the **MIT License**.

### **Key Permissions and Conditions:**
  - **Permissions**:
    - Commercial use
    - Modification
    - Distribution
    - Private use
  - **Conditions**:
    - You must include the original copyright and license notice in any copy of the software.

  - A full copy of the license is included in the repository. See the [LICENSE](./LICENSE) file for more details.

  - ```plaintext
    MIT License

    Copyright (c) 2025 jfprogramming

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    ```
