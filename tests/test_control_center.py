import unittest
from unittest.mock import patch
from control_center import clear_screen

class TestControlCenter(unittest.TestCase):

    @patch('control_center.os.system')
    @patch('control_center.os.name', 'nt')
    def test_clear_screen_windows(self, mock_system):
        clear_screen()
        mock_system.assert_called_once_with('cls')

    @patch('control_center.os.system')
    @patch('control_center.os.name', 'posix')
    def test_clear_screen_posix(self, mock_system):
        clear_screen()
        mock_system.assert_called_once_with('clear')

if __name__ == '__main__':
    unittest.main()
