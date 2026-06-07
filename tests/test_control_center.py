import sys
from unittest.mock import patch

# Adjust sys.path to allow importing from the parent directory
sys.path.append('.')

import control_center

class TestControlCenter:
    @patch('builtins.input')
    @patch('control_center.console.print')
    @patch('control_center.clear_screen')
    def test_show_launch_instructions(self, mock_clear_screen, mock_console_print, mock_input):
        control_center.show_launch_instructions()

        mock_clear_screen.assert_called_once()
        mock_console_print.assert_called_once()

        args, kwargs = mock_console_print.call_args
        assert args[0].__class__.__name__ == 'Panel'

        mock_input.assert_called_once_with("\nPress Enter to return to Command Center...")
