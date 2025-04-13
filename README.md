# dpkg-status

`dpkg-status` is a Python3 script for parsing and analyzing the `/var/lib/dpkg/status` file on Debian-based systems. The script helps identify packages explicitly installed by the user, excluding dependencies and auto-installed packages.

---

## Features:
- Parses `/var/lib/dpkg/status` to list explicitly installed packages.
- Utilizes `/var/lib/apt/extended_states` for auto-installed metadata.
- Optionally integrates with `apt-mark showmanual` for enhanced accuracy.

---

## Prerequisites:
To run the script, ensure the following prerequisites are met:
1. **Operating System**: Debian-based system (e.g., Debian 12, Ubuntu, Linux Mint).
2. **Python Version**: Python 3.6 or newer.
3. **Required Files**:
   - `/var/lib/dpkg/status`: The dpkg status file.
   - `/var/lib/apt/extended_states`: The extended states file.
4. **Permissions**:
   - Read access to `/var/lib/dpkg/status` and `/var/lib/apt/extended_states`.

---

## System Requirements:
Before running the script, ensure your system meets the following requirements:
- **Memory**: At least 512 MB RAM.
- **Disk Space**: Minimal disk space is required, but ensure `/var/lib/dpkg/` and `/var/lib/apt/` are accessible.
- **Linux Distribution**: This script is designed for Debian-based distributions.

---

## Installation:
1. Clone the repository:
   - ```bash
     git clone https://github.com/jfprogramming/dpkg-status.git
     cd dpkg-status
   
2. Set up a virtual environment (optional but recommended):
   - ```bash
     python3 -m venv .venv
     source .venv/bin/activate

3. Install dependencies (if required):
   - ```bash 
     pip install -r requirements.txt
     
4. Running  
   - ```bash
     ./main.py 

## Detection Algorithm:
The script determines whether a package is explicitly installed by analyzing key package management files and metadata. It excludes auto-installed packages (dependencies installed as part of another package) and focuses on packages explicitly installed by the user. The process involves the following steps:

1. **Parsing the `/var/lib/dpkg/status` File**:
   - The script reads the `dpkg status` file line by line.
   - It extracts information such as package names, statuses, and metadata fields like `Status: install ok installed`.

2. **Filtering Auto-Installed Packages**:
   - Auto-installed packages are identified by cross-checking with `/var/lib/apt/extended_states`.
   - Packages with the marker `Auto-Installed: 1` in the `extended_states` file are excluded from the explicitly installed list.

3. **Combining with `apt-mark showmanual`**:
   - The script optionally integrates with the output of `apt-mark showmanual` to incorporate packages manually marked by the user as installed.

4. **Identifying Explicitly Installed Packages**:
   - Packages are considered explicitly installed if:
     - They are marked as `Status: install ok installed` in `/var/lib/dpkg/status`.
     - They are not listed as auto-installed in `/var/lib/apt/extended_states`.
     - They are included in the output of `apt-mark showmanual` (if applicable).

5. **Output**:
   - The script outputs a final list of explicitly installed packages by merging the results from the above steps, ensuring no duplicates.

## Notes:
  - **File: /var/lib/dpkg/status**
    - This file is part of the dpkg system, which is the backend package manager used by Debian-based systems.
    It serves as the central database of installed packages.
    Tracks every package installed on the system, along with its metadata.


  - **File: /var/lib/apt/extended_states**
    - This file is used by the APT package manager to track extra information about packages, specifically their installation status.
    - Tracks whether a package was Auto-installed as a dependency (Auto-Installed: 1).
    - Not explicitly marked as auto-installed (field absent or Auto-Installed: 0).
    - Helps determine which packages were installed automatically as dependencies.
    

  **Note**: On Debian-based systems, APT maintains logs that record package installations, upgrades, and removals. 
    
  **Here are the key log files:**

  - **File: /var/log/dpkg.log**
    - Tracks all package management actions performed by dpkg, including those initiated by apt.
    - Logs package installations, removals, and upgrades.
    

  - **File: /var/log/apt/term.log**
    - Logs detailed terminal output for apt commands.
    - Includes verbose information about package downloads, installations, and configurations.
    

  - **File: /var/log/apt/history.log**
    - Tracks high-level actions performed by apt, such as package installations, upgrades, and removals.
    - Records the command used (e.g., apt install) and the list of affected packages.

## Example file contents:

1. **File:`/var/lib/dpkg/status`**:
  ```plaintext
  Package: adwaita-icon-theme
  Status: install ok installed
  Priority: optional
  Section: gnome
  Installed-Size: 5234
  Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
  Architecture: all
  Multi-Arch: foreign
  Version: 41.0-1ubuntu1
  Replaces: adwaita-icon-theme-full (<< 41.0-1ubuntu1), gnome-themes-standard-data (<< 3.18.0-2~)
  Depends: hicolor-icon-theme, gtk-update-icon-cache, ubuntu-mono | adwaita-icon-theme-full
  Recommends: librsvg2-common
  Breaks: adwaita-icon-theme-full (<< 41.0-1ubuntu1), gnome-themes-standard-data (<< 3.18.0-2~)
  Description: default icon theme of GNOME (small subset)
  This package contains the default icon theme used by the GNOME desktop.
  The icons are used in many of the official GNOME applications like eog,
  evince, system monitor, and many more.
  .
  This package only contains a small subset of the original GNOME icons which
  are not provided by the Humanity icon theme, to avoid installing many
  duplicated icons. Please install adwaita-icon-theme-full if you want the full set.
  Original-Maintainer: Debian GNOME Maintainers <pkg-gnome-maintainers@lists.alioth.debian.org>
  
  Package: aglfn
  Status: install ok installed
  Priority: optional
  Section: fonts
  Installed-Size: 123
  Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
  Architecture: all
  Multi-Arch: foreign
  Version: 1.7+git20191031.4036a9c-2
  Description: Adobe Glyph List For New Fonts
  AGL (Adobe Glyph List) maps glyph names to Unicode values for the
  purpose of deriving content. AGLFN (Adobe Glyph List For New Fonts) is a
  subset of AGL that excludes the glyph names associated with the PUA
  (Private Use Area), and is meant to specify preferred glyph names for
  new fonts. Also included is the ITC Zapf Dingbats Glyph List, which is
  similar to AGL in that it maps glyph names to Unicode values for the
  purpose of deriving content, but only for the glyphs in the ITC Zapf
  Dingbats font.
  .
  Be sure to visit the AGL Specification and Developer Documentation pages
  for detailed information about naming glyphs, interpreting glyph names,
  and developing OpenType fonts.
  Original-Maintainer: Debian Fonts Task Force <pkg-fonts-devel@lists.alioth.debian.org>
  Homepage: https://github.com/adobe-type-tools/agl-aglfn
  
  Package: aisleriot
  Status: install ok installed
  Priority: optional
  Section: games
  Installed-Size: 8808
  Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
  Architecture: amd64
  Version: 1:3.22.22-1
  Depends: dconf-gsettings-backend | gsettings-backend, guile-2.2-libs, libatk1.0-0 (>= 1.12.4), libc6 (>= 2.34), libcairo2 (>= 1.10.0), libcanberra-gtk3-0 (>= 0.25), libcanberra0 (>= 0.2), libgdk-pixbuf-2.0-0 (>= 2.22.0), libglib2.0-0 (>= 2.37.3), libgtk-3-0 (>= 3.19.12), librsvg2-2 (>= 2.32.0)
  Recommends: yelp
  Suggests: gnome-cards-data
  Description: GNOME solitaire card game collection
  This is a collection of over eighty different
  ```


2. **File: `/var/lib/apt/extended_states`**: 
  ```plaintext
  Package: libtraceevent1
  Architecture: amd64
  Auto-Installed: 1

  Package: linux-hwe-6.8-headers-6.8.0-57
  Architecture: amd64
  Auto-Installed: 1

  Package: linux-modules-6.8.0-57-generic
  Architecture: amd64
  Auto-Installed: 1

  Package: linux-hwe-6.8-tools-6.8.0-57
  Architecture: amd64
  Auto-Installed: 1

  Package: linux-image-6.8.0-57-generic
  Architecture: amd64
  Auto-Installed: 1

  Package: linux-headers-6.8.0-57-generic
  Architecture: amd64
  Auto-Installed: 1

  Package: linux-tools-6.8.0-57-generic
  Architecture: amd64
  Auto-Installed: 1

   Package: linux-modules-extra-6.8.0-57-generic
  Architecture: amd64
  Auto-Installed: 1
  ```

## Creating Debian package to install dpkg-status script
  - Debian packages have a specific directory structure. Organize your project like this:

    ```plaintext
    dpkg-status/               # Root directory of your project
    ├── debian/                # Contains files needed for building the package
    │   ├── control            # Metadata about the package
    │   ├── changelog          # Change history for the package
    │   ├── copyright          # Licensing information
    │   ├── rules              # Instructions for building the package
    │   ├── install            # Files to be installed and their destinations
    │   ├── compat             # Debhelper compatibility level
    ├── src/                   # Your Python source code
    │   ├── dpkg_status.py     # Your main script
    │   ├── other_files.py     # Any other Python files
    ├── README.md              # Project documentation
    ├── setup.py               # Python packaging file (optional, if needed)
    ```
2. **Create the debian/ Directory**
  - This directory contains all the files required to build a Debian package.
  - Required Files:
    - **Control** - This defines the package metadata. 
      - Create a file named control in the **debian/** directory with the following content:
      - ```plaintext 
        Source: dpkg-status
        Section: utils
        Priority: optional
        Maintainer: Your Name <your.email@example.com>
        Build-Depends: debhelper-compat (= 13), python3
        Standards-Version: 4.5.0
        Homepage: https://github.com/jfprogramming/dpkg-status

        Package: dpkg-status
        Architecture: all
        Depends: ${python3:Depends}, ${misc:Depends}
        Description: A Python script to parse dpkg status files on Debian systems.
        This script determines explicitly installed packages on Debian-based systems.
        ```
    - **Changelog** - Document the changes made to your package. 
      - Use the **dch** command to create and manage the changelog:
      - ```bash 
        dch --create --package dpkg-status --newversion 1.1 --distribution unstable
        ```
        
3. **Copyright**
  - Add licensing information. Example:
  - ```plaintext 
    Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
    Upstream-Name: dpkg-status
    Source: https://github.com/jfprogramming/dpkg-status

    Files: *
    Copyright: 2025 Your Name <your.email@example.com>
    License: MIT
    ```
    
4. **Rules**
  - Instructions for building the package. Example:
  - ```bash
    #!/usr/bin/make -f
    %:
	dh $@
    ```
5. **compat**
  - Specify the debhelper compatibility level. 
  - Add this file with the following content:
  - ```plaintext 
    13
    ```
    
6. **Install the `.deb` Package VIA GitHub release and Wget**
  - Download the .deb Package:
    - Provide a direct URL for the .deb file (from your GitHub release or another host):
    ```bash
    wget https://github.com/jfprogramming/dpkg-status/releases/download/v1.1/dpkg-status_1.1_all.deb
    ```
  - Install the Package:
    - Use dpkg to install the package:
    ```bash
    sudo dpkg -i dpkg-status_1.1_all.deb
    ```
    
7. **Install the `.deb` Package by cloning repo**
   - Navigate to the directory where the `.deb` package is located:
      ```bash
      cd ~/PycharmProjects/dpkg-status
     ```
   - Use dpkg to install the package:
     ```bash 
     sudo dpkg -i ../dpkg-status_1.0-1_all.deb
     ```
   - If there are missing dependencies, fix them using:
     ```bash
      sudo apt-get install -f
     ```
   - Run the Script
     - Confirm the script is installed in /usr/bin:
     ```bash
      ls /usr/bin/dpkg_status
     ```
   - Run the script directly:
     ```bash
      dpkg_status
     ```
     
## **Debugging Installation Issues** 
     - If the installation fails, check for errors in the terminal and resolve them.
     - To remove the package and reinstall it:
     ```bash
     sudo dpkg -r dpkg-status
     sudo dpkg -i ../dpkg-status_1.1_all.deb
     ```
     - Verify the Installation: Check if the script is now installed without the .py extension:
     ```bash
     ls /usr/bin/dpkg_status
     ```
     - If the output shows /usr/bin/dpkg_status, the script has been successfully renamed. 
     - Run the Script: You can now run the script without the .py extension:
     ```bash
     dpkg_status
     ```