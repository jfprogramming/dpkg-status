import unittest
from unittest.mock import mock_open, patch
from main import parse_manual_packages, parse_dpkg_status


class TestDpkgStatusParser(unittest.TestCase):
    def test_parse_manual_packages(self):
        # Mock content of /var/lib/apt/extended_states
        mock_states_content = """\
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
        """
        with patch("builtins.open", mock_open(read_data=mock_states_content)):
            result = parse_manual_packages("/mock/path/extended_states")
            self.assertEqual(result, {"linux-modules-6.8.0-57-generic", "linux-modules-extra-6.8.0-57-generic"})  # Manually installed packages

    def test_parse_dpkg_status(self):
        # Mock content of /var/lib/dpkg/status
        mock_status_content = """\
        Package: zlib1g
        Status: install ok installed
        Priority: required
        Section: libs
        Installed-Size: 164
        Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
        Architecture: amd64
        Multi-Arch: same
        Source: zlib
        Version: 1:1.2.11.dfsg-2ubuntu9.2
        Provides: libz1
        Depends: libc6 (>= 2.14)
        Breaks: libxml2 (<< 2.7.6.dfsg-2), texlive-binaries (<< 2009-12)
        Conflicts: zlib1 (<= 1:1.0.4-7)
        Description: compression library - runtime
         zlib is a library implementing the deflate compression method found
         in gzip and PKZIP.  This package includes the shared library.
        Homepage: http://zlib.net/
        Original-Maintainer: Mark Brown <broonie@debian.org>
        
        Package: zlib1g-dev
        Status: install ok installed
        Priority: optional
        Section: libdevel
        Installed-Size: 592
        Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
        Architecture: amd64
        Multi-Arch: same
        Source: zlib
        Version: 1:1.2.11.dfsg-2ubuntu9.2
        Provides: libz-dev
        Depends: zlib1g (= 1:1.2.11.dfsg-2ubuntu9.2), libc6-dev | libc-dev
        Conflicts: zlib1-dev
        Description: compression library - development
         zlib is a library implementing the deflate compression method found
         in gzip and PKZIP.  This package includes the development support
         files.
        Homepage: http://zlib.net/
        Original-Maintainer: Mark Brown <broonie@debian.org>
        
        Package: zstd
        Status: install ok installed
        Priority: optional
        Section: utils
        Installed-Size: 1655
        Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
        Architecture: amd64
        Source: libzstd
        Version: 1.4.8+dfsg-3build1
        Depends: libc6 (>= 2.34), libgcc-s1 (>= 3.3.1), liblz4-1 (>= 0.0~r127), liblzma5 (>= 5.1.1alpha+20120614), libstdc++6 (>= 12), zlib1g (>= 1:1.1.4)
        Description: fast lossless compression algorithm -- CLI tool
         Zstd, short for Zstandard, is a fast lossless compression algorithm, targeting
         real-time compression scenarios at zlib-level compression ratio.
         .
         This package contains the CLI program implementing zstd.
        Homepage: https://github.com/facebook/zstd
        Original-Maintainer: Debian Med Packaging Team <debian-med-packaging@lists.alioth.debian.org>
        """
        manual_packages = {"package1", "package2"}  # Mock manually installed packages

        with patch("builtins.open", mock_open(read_data=mock_status_content)):
            result = parse_dpkg_status("/mock/path/status", manual_packages)
            self.assertEqual(result, ["zlib1g", "zstd"])  # Explicitly installed packages only


if __name__ == "__main__":
    unittest.main()