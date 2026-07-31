import pytest
from unittest.mock import patch, call
from friday_simulator import typewriter_print

@patch('friday_simulator.time.sleep')
@patch('friday_simulator.sys.stdout')
@patch('builtins.print')
def test_typewriter_print_normal_text(mock_print, mock_stdout, mock_sleep):
    """Test that normal text is printed character by character with the given speed."""
    typewriter_print("Hi", speed=0.05)

    mock_stdout.write.assert_has_calls([call('H'), call('i')])
    mock_stdout.flush.assert_has_calls([call(), call()])
    mock_sleep.assert_has_calls([call(0.05), call(0.05)])
    mock_print.assert_called_once_with()

@patch('friday_simulator.time.sleep')
@patch('friday_simulator.sys.stdout')
@patch('builtins.print')
def test_typewriter_print_default_speed(mock_print, mock_stdout, mock_sleep):
    """Test that typewriter_print uses the default speed of 0.03 when not provided."""
    typewriter_print("A")

    mock_stdout.write.assert_called_once_with('A')
    mock_stdout.flush.assert_called_once()
    mock_sleep.assert_called_once_with(0.03)
    mock_print.assert_called_once_with()

@patch('friday_simulator.time.sleep')
@patch('friday_simulator.sys.stdout')
@patch('builtins.print')
def test_typewriter_print_empty_string(mock_print, mock_stdout, mock_sleep):
    """Test that an empty string prints nothing but still calls print() at the end."""
    typewriter_print("")

    mock_stdout.write.assert_not_called()
    mock_stdout.flush.assert_not_called()
    mock_sleep.assert_not_called()
    mock_print.assert_called_once_with()
