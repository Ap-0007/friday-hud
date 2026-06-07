from unittest.mock import Mock, patch
from friday.prompts import register_all_prompts

@patch("friday.prompts.templates.register")
def test_register_all_prompts(mock_register):
    # Arrange
    mock_mcp = Mock()

    # Act
    register_all_prompts(mock_mcp)

    # Assert
    mock_register.assert_called_once_with(mock_mcp)
