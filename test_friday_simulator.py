import unittest
from unittest.mock import patch

from friday_simulator import get_response, CANNED_RESPONSES

class TestFridaySimulator(unittest.TestCase):
    @patch('friday_simulator.random.choice')
    def test_get_response_news(self, mock_choice):
        mock_choice.return_value = "Mocked news response"
        # Test exact keyword
        self.assertEqual(get_response("Give me the news"), "Mocked news response")
        mock_choice.assert_called_with(CANNED_RESPONSES["news"])
        # Test casing
        self.assertEqual(get_response("What is HAPPENING?"), "Mocked news response")
        # Test another keyword in same block
        self.assertEqual(get_response("Short brief please"), "Mocked news response")

    @patch('friday_simulator.random.choice')
    def test_get_response_system(self, mock_choice):
        mock_choice.return_value = "Mocked system response"
        self.assertEqual(get_response("Check system"), "Mocked system response")
        mock_choice.assert_called_with(CANNED_RESPONSES["system"])
        self.assertEqual(get_response("Run diagnostic"), "Mocked system response")
        self.assertEqual(get_response("status report"), "Mocked system response")

    @patch('friday_simulator.random.choice')
    def test_get_response_market(self, mock_choice):
        mock_choice.return_value = "Mocked market response"
        self.assertEqual(get_response("How is the market?"), "Mocked market response")
        mock_choice.assert_called_with(CANNED_RESPONSES["market"])
        self.assertEqual(get_response("Any stock updates?"), "Mocked market response")
        self.assertEqual(get_response("What's the price?"), "Mocked market response")

    def test_get_response_hello(self):
        # random.choice is not called here
        expected_response = "Hello boss. Ready to build something incredible?"
        self.assertEqual(get_response("hello friday"), expected_response)
        self.assertEqual(get_response("hi there"), expected_response)
        self.assertEqual(get_response("hey!"), expected_response)

    def test_get_response_who_are_you(self):
        # random.choice is not called here
        expected_response = "I'm F.R.I.D.A.Y. — Fully Responsive Intelligent Digital Assistant for You. At your service, always."
        self.assertEqual(get_response("who are you?"), expected_response)
        self.assertEqual(get_response("what are you?"), expected_response)

    @patch('friday_simulator.random.choice')
    def test_get_response_default(self, mock_choice):
        mock_choice.return_value = "Mocked default response"
        self.assertEqual(get_response("perform a completely unknown task"), "Mocked default response")
        mock_choice.assert_called_with(CANNED_RESPONSES["default"])
        self.assertEqual(get_response("random input that does not match"), "Mocked default response")

if __name__ == '__main__':
    unittest.main()
