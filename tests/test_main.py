import unittest
import subprocess
from unittest.mock import patch, mock_open
from src.main import parse_dpkg_status, parse_extended_states, get_apt_mark_showmanual


class TestDpkgStatusParser(unittest.TestCase):
    def test_parse_extended_states(self):
        # Mock data for /var/lib/apt/extended_states
        mock_extended_states = """\
        Package: package1
        Architecture: amd64
        Auto-Installed: 1
        
        Package: package2
        Architecture: amd64
        Auto-Installed: 0
        
        Package: package3
        Architecture: amd64
        Auto-Installed: 1
        
        Package: package4
        Architecture: amd64
        """

        with patch("builtins.open", mock_open(read_data=mock_extended_states)):
            auto_installed, manual_installed = parse_extended_states("/fake/path/extended_states")

            # Verify auto-installed packages
            self.assertEqual(auto_installed, {"package1", "package3"})

            # Verify manually installed packages
            self.assertEqual(manual_installed, {"package2", "package4"})

    def test_parse_dpkg_status(self):
        # Mock data for /var/lib/dpkg/status
        mock_dpkg_status = """\
        Package: package1
        Status: install ok installed
        Priority: optional
        Section: libdevel
        Installed-Size: 592

        Package: package2
        Status: install ok installed
        Priority: optional
        Section: libdevel
        Installed-Size: 592

        Package: package3
        Status: install ok not-installed
        Priority: optional
        Section: libdevel
        Installed-Size: 592
        
        Package: package4
        Status: install ok installed
        Priority: optional
        Section: libdevel
        Installed-Size: 592
        """

        # Mock auto-installed packages
        auto_installed_packages = {"package1", "package3"}

        with patch("builtins.open", mock_open(read_data=mock_dpkg_status)):
            explicitly_installed = parse_dpkg_status("/fake/path/dpkg_status", auto_installed_packages)
            print(f"explicitly_install: {explicitly_installed}")

            # Verify explicitly installed packages
            self.assertEqual(explicitly_installed, {"package2", "package4"})

    @patch("subprocess.run")
    def test_get_apt_mark_showmanual(self, mock_subprocess):
        # Mock output of `apt-mark showmanual`
        mock_subprocess.return_value = subprocess.CompletedProcess(
            args=["apt-mark", "showmanual"],
            returncode=0,
            stdout="package2\npackage4\npackage5\n"
        )

        manual_packages = get_apt_mark_showmanual()

        # Verify manually installed packages
        self.assertEqual(manual_packages, {"package2", "package4", "package5"})


if __name__ == "__main__":
    unittest.main()