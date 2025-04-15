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
   ```bash
   wget https://github.com/jfprogramming/dpkg-status/releases/download/v1.4/dpkg-status_1.4_amd64.deb
   ```

2. Install the Package:
   - ```bash
     sudo dpkg -i dpkg-status_1.4_amd64.deb
     ```
   - ```bash
     sudo apt-get install ./dpkg-status_1.4_amd64.deb
     sudo apt --fix-broken install
     ```

4. Run the Script:
   ```bash
   dpkg_status.py
   ```

### **Option 2: Install via Cloning the Repository**

1. Clone the repository:
   ```bash
   git clone https://github.com/jfprogramming/dpkg-status.git
   cd dpkg-status
   ```

2. Install dependencies and build the `.deb` package:
   ```bash
   sudo apt-get install -f
   sudo dpkg -i dpkg-status_1.4_amd64.deb
   ```

---

## **2. Features**

- Parses `/var/lib/dpkg/status` to list explicitly installed packages.
- Leverages `/var/lib/apt/extended_states` for analyzing auto-installed packages.
- Optionally integrates with `apt-mark showmanual` for enhanced accuracy.

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

---

## **5. Project Configuration**

Follow these steps to set up the project for development:

1. Clone the repository:
   ```bash
   git clone https://github.com/jfprogramming/dpkg-status.git
   cd dpkg-status
   ```

2. (Optional) Set up a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies, if required:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the script:
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
1. Possible packages need to run qt appdpkg-status app on Traget Debian 12 system
   ```bash
   sudo apt install libxcb-cursor0
                    libxcb-cursor-dev
                    libqt6quick6
                    libqt6quickcontrols2-6
                    libqt6quicklayouts6
                    qt6-declarative-dev
                    qt6-declarative-dev-tools
                    build-essential
                    libxcb-xinerama0
                    libxcb1
                    libxcb-render0
                    libxcb-shape0
                    libxcb-glx0
                    qt6-wayland
   ```
3. 
      
3. After installing the `.deb` package:
   ```bash
   appdpkg-status
   ```

4. Debugging:
   - If the application doesn't run, enable debugging:
     ```bash
     QT_DEBUG_PLUGINS=1 appdpkg-status
     ```
   - Installation of Qt 6.2.4 maybe necessary on target device to provide qml files for qt applicaiton
     - Qt Online Installer:
       ```bash
       wget https://download.qt.io/official_releases/online_installers/qt-online-installer-linux-x64-online.run
       ```
       
  - Make the downloaded file executable:
    ```bash
    chmod +x qt-online-installer-linux-x64-online.run
    ```
    
  - Run the installer:
    ```bash
    ./qt-online-installer-linux-x64-online.run
    ```
    
  -  Set LD_LIBRARY_PATH ENV VAR
      ```bash
      export PATH=/opt/Qt/6.2.4/bin:$PATH
      ```

---

## **9. Releases**

### **Creating a `.deb` Package**:
1. Set up the project directory structure:
   ```plaintext
   dpkg-status/
   ├── debian/
   │   ├── control
   │   ├── changelog
   │   ├── copyright
   │   ├── rules
   │   ├── install
   │   ├── compat
   ├── src/
   │   ├── dpkg_status.py
   ├── releases/
   │   ├── dpkg-status_<version>_all.deb
   ├── README.md
   ```

2. Build the package:
   ```bash
   debuild -us -uc
   ```

3. Verify the package:
   ```bash
   lintian ../dpkg-status_<version>_all.deb
   ```

4. Publish on GitHub:
   - Attach the `.deb` package to a GitHub release with appropriate release notes.

---

## **10. Troubleshooting**

### **General Issues**:
- **Missing Dependencies**:
  ```bash
  sudo apt-get install -f
  ```

- **Reinstall the Package**:
  ```bash
  sudo dpkg -r dpkg-status
  sudo dpkg -i dpkg-status_1.4_amd64.deb
  ```

### **Debugging Installation**:
1. Enable debug logging:
   ```plaintext
   logging.basicConfig(level=logging.DEBUG)
   ```

2. Verify installed script:
   ```bash
   ls /usr/bin/dpkg_status.py
   ```

---
