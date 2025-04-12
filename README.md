# dpkg-status

- **Python3 script** that parses the dpkg status file to extract packages explicitly installed by the user.
  - `file_path`: Path to `/var/lib/dpkg/status` file.
  - `return`: List of explicitly installed packages.

- **Detection Algorithm**:
  The script determines whether a package is explicitly installed by examining the `dpkg status` file. It considers packages marked as `Status: install ok installed`, filtering out dependencies or auto-installed packages (those installed as part of another package). The process involves:
    1. Parsing `/var/lib/dpkg/status` line by line.
    2. Extracting package names and their associated metadata.
    3. Identifying explicitly installed packages based on relevant markers (e.g., status, dependencies).

- **Example `/var/lib/dpkg/status` file contents**:

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
