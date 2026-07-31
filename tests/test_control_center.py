import os
import pytest
from unittest.mock import patch

import control_center

@patch("control_center.load_dotenv")
def test_get_status_all_missing(mock_load_dotenv):
    # Ensure environment variables defined in REQUIRED_KEYS are not set
    with patch.dict(os.environ, {}, clear=True):
        status, missing = control_center.get_status()

        # Check that load_dotenv was called
        mock_load_dotenv.assert_called_once_with(control_center.ENV_FILE, override=True)

        # Verify all required keys are in the missing list
        assert len(missing) == len(control_center.REQUIRED_KEYS)
        assert set(missing) == set(control_center.REQUIRED_KEYS.keys())

        # Verify status tuples
        for key, stat_str, desc in status:
            assert stat_str == "[red]Missing/Placeholder[/red]"
            assert desc == control_center.REQUIRED_KEYS[key]

@patch("control_center.load_dotenv")
def test_get_status_placeholders(mock_load_dotenv):
    placeholders = {
        "LIVEKIT_URL": "wss://your-project.livekit.cloud",
        "LIVEKIT_API_KEY": "APIxxxx",
        "LIVEKIT_API_SECRET": "sk_12345678", # len < 15 and starts with sk_
        "GOOGLE_API_KEY": "your-project-id",
        "OPENAI_API_KEY": "sk_abc",
        "SARVAM_API_KEY": "APIxxxx_something",
        "LLM_PROVIDER": "", # Empty string
    }

    with patch.dict(os.environ, placeholders, clear=True):
        status, missing = control_center.get_status()

        # Verify all are considered missing
        assert len(missing) == len(control_center.REQUIRED_KEYS)
        assert set(missing) == set(control_center.REQUIRED_KEYS.keys())

        for key, stat_str, desc in status:
            assert stat_str == "[red]Missing/Placeholder[/red]"

@patch("control_center.load_dotenv")
def test_get_status_configured(mock_load_dotenv):
    configured = {
        "LIVEKIT_URL": "wss://my-real-project.livekit.cloud",
        "LIVEKIT_API_KEY": "real_api_key_here",
        "LIVEKIT_API_SECRET": "real_api_secret_that_is_long",
        "GOOGLE_API_KEY": "AIzaSy_some_real_key_here",
        "OPENAI_API_KEY": "sk_real_key_with_length_greater_than_15",
        "SARVAM_API_KEY": "sarvam_real_key",
        "LLM_PROVIDER": "gemini",
    }

    with patch.dict(os.environ, configured, clear=True):
        status, missing = control_center.get_status()

        # None should be missing
        assert len(missing) == 0

        # Verify status tuples correctly mask the configured keys
        for key, stat_str, desc in status:
            assert "[green]Configured[/green]" in stat_str
            val = configured[key]

            # Replicate masking logic to verify
            expected_mask = val[:8] + "*" * (len(val) - 8) if len(val) > 8 else "***"
            assert expected_mask in stat_str

@patch("control_center.load_dotenv")
def test_get_status_mixed(mock_load_dotenv):
    mixed_env = {
        "LIVEKIT_URL": "wss://my-real-project.livekit.cloud", # Configured
        "LIVEKIT_API_KEY": "APIxxxx", # Placeholder (Missing)
        # LIVEKIT_API_SECRET not provided (Missing)
        "GOOGLE_API_KEY": "AIzaSy_some_real_key_here", # Configured
        "OPENAI_API_KEY": "sk_abc", # Placeholder (Missing)
        "SARVAM_API_KEY": "sarvam", # Configured (length <= 8)
        "LLM_PROVIDER": "your-project", # Placeholder (Missing)
    }

    with patch.dict(os.environ, mixed_env, clear=True):
        status, missing = control_center.get_status()

        # Expected missing
        expected_missing = ["LIVEKIT_API_KEY", "LIVEKIT_API_SECRET", "OPENAI_API_KEY", "LLM_PROVIDER"]
        assert set(missing) == set(expected_missing)

        # Verify specific status entries
        status_dict = {k: stat_str for k, stat_str, _ in status}

        assert status_dict["LIVEKIT_URL"] == f"[green]Configured[/green] (wss://my***************************)"
        assert status_dict["LIVEKIT_API_KEY"] == "[red]Missing/Placeholder[/red]"
        assert status_dict["LIVEKIT_API_SECRET"] == "[red]Missing/Placeholder[/red]"
        assert status_dict["GOOGLE_API_KEY"] == f"[green]Configured[/green] (AIzaSy_s*****************)"
        assert status_dict["OPENAI_API_KEY"] == "[red]Missing/Placeholder[/red]"
        assert status_dict["SARVAM_API_KEY"] == f"[green]Configured[/green] (***)"
        assert status_dict["LLM_PROVIDER"] == "[red]Missing/Placeholder[/red]"
