import pytest
from unittest.mock import patch

from friday_simulator import main_exit, SYSTEM_NAME

@patch("friday_simulator.console.print")
def test_main_exit(mock_print):
    """Test that main_exit prints the correct shutdown message."""
    main_exit()

    mock_print.assert_called_once_with(
        f"\n[bold magenta]{SYSTEM_NAME}:[/bold magenta] [dim]Emergency shutdown. Logged out.[/dim]"
    )
