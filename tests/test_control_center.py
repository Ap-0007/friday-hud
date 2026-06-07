import pytest
from unittest.mock import patch, MagicMock

# Import the module to be tested
import control_center

@patch('builtins.input')
@patch('control_center.console.print')
@patch('socket.socket')
def test_handle_choice_2_online(mock_socket_class, mock_print, mock_input):
    # Setup mock socket instance
    mock_sock = MagicMock()
    # connect_ex returns 0 when connection is successful
    mock_sock.connect_ex.return_value = 0
    mock_socket_class.return_value = mock_sock

    # Run the function with choice "2"
    control_center.handle_choice("2")

    # Verify socket setup and connection
    mock_socket_class.assert_called_once()
    mock_sock.settimeout.assert_called_once_with(1)
    mock_sock.connect_ex.assert_called_once_with(('127.0.0.1', 8000))

    # Verify console output
    mock_print.assert_any_call("\n[dim]Scanning local network for MCP server...[/dim]")
    mock_print.assert_any_call("[green]Found Brain Backend (MCP) on port 8000.[/green]")

    # Verify user interaction
    mock_input.assert_called_once_with("\nPress Enter to continue...")

@patch('builtins.input')
@patch('control_center.console.print')
@patch('socket.socket')
def test_handle_choice_2_offline(mock_socket_class, mock_print, mock_input):
    # Setup mock socket instance
    mock_sock = MagicMock()
    # connect_ex returns an error code (e.g., 111 for connection refused) when unsuccessful
    mock_sock.connect_ex.return_value = 111
    mock_socket_class.return_value = mock_sock

    # Run the function with choice "2"
    control_center.handle_choice("2")

    # Verify socket setup and connection
    mock_socket_class.assert_called_once()
    mock_sock.settimeout.assert_called_once_with(1)
    mock_sock.connect_ex.assert_called_once_with(('127.0.0.1', 8000))

    # Verify console output
    mock_print.assert_any_call("\n[dim]Scanning local network for MCP server...[/dim]")
    mock_print.assert_any_call("[red]Brain Backend (MCP) is currently OFFLINE.[/red]")

    # Verify user interaction
    mock_input.assert_called_once_with("\nPress Enter to continue...")
