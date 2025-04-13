import unittest
from unittest.mock import mock_open, patch
from main import parse_manual_packages, parse_dpkg_status


class TestDpkgStatusParser(unittest.TestCase):
    def test_parse_manual_packages(self):
        # Mock content of /var/lib/apt/extended_states
        mock_states_content = """
        Package: package1
        Auto-Installed: 1

        Package: package2

        Package: package3
        Auto-Installed: 1

        Package: package4
        """
        with patch("builtins.open", mock_open(read_data=mock_states_content)):
            result = parse_manual_packages("/mock/path/extended_states")
            self.assertEqual(result, {"package2", "package4"})  # Manually installed packages

    def test_parse_dpkg_status(self):
        # Mock content of /var/lib/dpkg/status
        mock_status_content = """
        Package: package1
        Status: install ok installed

        Package: package2
        Status: install ok installed

        Package: package3
        Status: purge ok not-installed
        """
        manual_packages = {"package1", "package2"}  # Mock manually installed packages

        with patch("builtins.open", mock_open(read_data=mock_status_content)):
            result = parse_dpkg_status("/mock/path/status", manual_packages)
            self.assertEqual(result, ["package1", "package2"])  # Explicitly installed packages only


if __name__ == "__main__":
    unittest.main()