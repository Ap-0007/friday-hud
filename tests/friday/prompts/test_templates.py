from unittest.mock import MagicMock
import pytest
from friday.prompts.templates import register

def test_register():
    mcp = MagicMock()

    # Store decorated functions
    decorated_funcs = {}

    def mock_prompt():
        def decorator(func):
            decorated_funcs[func.__name__] = func
            return func
        return decorator

    mcp.prompt = mock_prompt

    register(mcp)

    assert "summarize" in decorated_funcs
    assert "explain_code" in decorated_funcs

    # Test summarize
    summarize = decorated_funcs["summarize"]
    assert summarize("hello") == "Summarize the following text concisely:\n\nhello"

    # Test explain_code
    explain_code = decorated_funcs["explain_code"]
    assert explain_code("print('hello')") == "Explain the following Python code in plain English, step by step:\n\n```python\nprint('hello')\n```"
    assert explain_code("console.log('hello')", "JavaScript") == "Explain the following JavaScript code in plain English, step by step:\n\n```javascript\nconsole.log('hello')\n```"
