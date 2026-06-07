import pytest
from unittest.mock import patch
from control_center import display_dashboard

@patch("control_center.Prompt.ask")
@patch("control_center.console.print")
@patch("control_center.get_status")
@patch("control_center.clear_screen")
def test_display_dashboard_with_missing_keys(mock_clear_screen, mock_get_status, mock_console_print, mock_prompt_ask):
    mock_get_status.return_value = (
        [
            ("LIVEKIT_URL", "[red]Missing/Placeholder[/red]", "LiveKit Project URL")
        ],
        ["LIVEKIT_URL"]
    )
    mock_prompt_ask.return_value = "1"

    result = display_dashboard()

    assert result == "1"
    mock_clear_screen.assert_called_once()
    mock_get_status.assert_called_once()
    mock_prompt_ask.assert_called_once()

    printed_texts = [str(call.args[0]) for call in mock_console_print.call_args_list if call.args]
    assert any("1 system components are offline" in text for text in printed_texts)

@patch("control_center.Prompt.ask")
@patch("control_center.console.print")
@patch("control_center.get_status")
@patch("control_center.clear_screen")
def test_display_dashboard_all_systems_nominal(mock_clear_screen, mock_get_status, mock_console_print, mock_prompt_ask):
    mock_get_status.return_value = (
        [
            ("LIVEKIT_URL", "[green]Configured[/green] (wss://***)", "LiveKit Project URL")
        ],
        []
    )
    mock_prompt_ask.return_value = "4"

    result = display_dashboard()

    assert result == "4"
    mock_clear_screen.assert_called_once()
    mock_get_status.assert_called_once()

    printed_texts = [str(call.args[0]) for call in mock_console_print.call_args_list if call.args]
    assert any("Systems Nominal." in text for text in printed_texts)
