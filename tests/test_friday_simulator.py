import unittest
from unittest.mock import patch, call, MagicMock
import friday_simulator

class TestFridaySimulator(unittest.TestCase):

    @patch('friday_simulator.time.sleep')
    @patch('friday_simulator.console.print')
    @patch('friday_simulator.Progress')
    @patch('friday_simulator.random.choice')
    @patch('friday_simulator.typewriter_print')
    def test_simulate_boot(self, mock_typewriter_print, mock_random_choice, mock_progress, mock_console_print, mock_time_sleep):
        # Setup mock behavior
        mock_random_choice.return_value = "Test greeting boss."
        mock_progress_instance = MagicMock()
        mock_progress.return_value.__enter__.return_value = mock_progress_instance

        # Call the function
        friday_simulator.simulate_boot()

        # Assert Progress context manager is used and add_task is called
        self.assertEqual(mock_progress_instance.add_task.call_count, 4)
        mock_progress_instance.add_task.assert_has_calls([
            call(description="Initializing Neural Core...", total=None),
            call(description="Syncing Satellite Uplink...", total=None),
            call(description="Loading Vocal Synthesis...", total=None),
            call(description="Authenticating Boss...", total=None),
        ])

        # Assert time.sleep is called
        self.assertEqual(mock_time_sleep.call_count, 5)
        mock_time_sleep.assert_has_calls([
            call(1),
            call(0.8),
            call(1.2),
            call(0.5),
            call(0.5)
        ])

        # Assert console.print is called correctly
        self.assertEqual(mock_console_print.call_count, 2)
        # The first call is for the Panel, which is harder to assert exact match for because of Align and Panel objects.
        # So we just check it was called. We'll check the second call which is simpler.

        # We can check that the last console.print has end=""
        mock_console_print.assert_any_call("\n[bold magenta]F.R.I.D.A.Y.:[/bold magenta] ", end="")

        # Assert typewriter_print is called with the mock greeting
        mock_typewriter_print.assert_called_once_with("Test greeting boss.")

if __name__ == '__main__':
    unittest.main()
