import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

import local_brain
from local_brain import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_history():
    # Reset messages_history before each test to ensure test isolation
    local_brain.messages_history = [{"role": "system", "content": local_brain.SYSTEM_PROMPT}]
    yield

@patch("local_brain.client.chat.completions.create")
def test_chat_basic(mock_create):
    mock_response = MagicMock()
    mock_msg = MagicMock()
    mock_msg.tool_calls = None
    mock_msg.content = "Hello, Tony."
    mock_response.choices = [MagicMock(message=mock_msg)]
    mock_create.return_value = mock_response

    response = client.post("/chat", json={"message": "Hi Friday"})

    assert response.status_code == 200
    assert response.json() == {"response": "Hello, Tony."}

    # Assert system prompt, user prompt and assistant reply
    assert len(local_brain.messages_history) == 3
    assert local_brain.messages_history[-1] == {"role": "assistant", "content": "Hello, Tony."}

@patch("local_brain.client.chat.completions.create")
def test_chat_history_truncation(mock_create):
    mock_response = MagicMock()
    mock_msg = MagicMock()
    mock_msg.tool_calls = None
    mock_msg.content = "I'm still here."
    mock_response.choices = [MagicMock(message=mock_msg)]
    mock_create.return_value = mock_response

    # Setup history with 21 messages (1 system + 20 user)
    local_brain.messages_history = [{"role": "system", "content": local_brain.SYSTEM_PROMPT}]
    for i in range(20):
        local_brain.messages_history.append({"role": "user", "content": f"Message {i}"})

    # Making request with 21 messages + 1 new message = 22 messages
    # Truncation logic: if len > 20: [0] + [-19:] -> 1 + 19 = 20 messages before processing
    # After response, there should be 21 messages

    response = client.post("/chat", json={"message": "One more"})

    assert response.status_code == 200
    assert response.json() == {"response": "I'm still here."}
    assert len(local_brain.messages_history) == 21
    assert local_brain.messages_history[0]["role"] == "system"

@patch("local_brain.client.chat.completions.create")
@patch.dict("local_brain.AVAILABLE_TOOLS", {"get_current_time": MagicMock(return_value="It's 12:00 PM")})
def test_chat_native_tool_call(mock_create):
    # First response: call a tool
    mock_msg_tool = MagicMock()
    mock_msg_tool.content = None

    mock_tc = MagicMock()
    mock_tc.id = "call_123"
    mock_tc.function.name = "get_current_time"
    mock_tc.function.arguments = "{}"
    mock_msg_tool.tool_calls = [mock_tc]

    mock_response_1 = MagicMock()
    mock_response_1.choices = [MagicMock(message=mock_msg_tool)]

    # Second response: normal text after tool call
    mock_msg_text = MagicMock()
    mock_msg_text.tool_calls = None
    mock_msg_text.content = "It's 12:00 PM"

    mock_response_2 = MagicMock()
    mock_response_2.choices = [MagicMock(message=mock_msg_text)]

    # Set mock to return response 1 then response 2
    mock_create.side_effect = [mock_response_1, mock_response_2]

    response = client.post("/chat", json={"message": "What time is it?"})

    assert response.status_code == 200
    assert response.json() == {"response": "It's 12:00 PM"}

    # Verify tool was called
    local_brain.AVAILABLE_TOOLS["get_current_time"].assert_called_once()

    # Verify history: system + user + tool_call + tool_result + assistant
    assert len(local_brain.messages_history) == 5
    assert local_brain.messages_history[-2]["role"] == "tool"
    assert local_brain.messages_history[-2]["content"] == "It's 12:00 PM"

@patch("local_brain.client.chat.completions.create")
@patch.dict("local_brain.AVAILABLE_TOOLS", {"set_system_volume": MagicMock(return_value="Volume set to 50")})
def test_chat_fallback_json(mock_create):
    # First response: output fallback JSON as content
    mock_msg_json = MagicMock()
    mock_msg_json.tool_calls = None
    mock_msg_json.content = '{"name": "set_system_volume", "parameters": {"level": 50}}'

    mock_response_1 = MagicMock()
    mock_response_1.choices = [MagicMock(message=mock_msg_json)]

    # Second response: assistant responds
    mock_msg_text = MagicMock()
    mock_msg_text.tool_calls = None
    mock_msg_text.content = "I set the volume."

    mock_response_2 = MagicMock()
    mock_response_2.choices = [MagicMock(message=mock_msg_text)]

    mock_create.side_effect = [mock_response_1, mock_response_2]

    response = client.post("/chat", json={"message": "Set volume to 50"})

    assert response.status_code == 200
    assert response.json() == {"response": "I set the volume."}

    # Verify tool was called
    local_brain.AVAILABLE_TOOLS["set_system_volume"].assert_called_once_with(level=50)

@patch("local_brain.client.chat.completions.create")
def test_chat_brain_sync_error(mock_create):
    mock_create.side_effect = Exception("API down")

    response = client.post("/chat", json={"message": "Hello"})

    assert response.status_code == 200
    assert "Brain sync error: API down" in response.json()["response"]
