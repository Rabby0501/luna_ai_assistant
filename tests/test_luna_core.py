import pytest
from unittest.mock import patch, MagicMock
from modules.luna_core import manage_history, get_luna_response

@pytest.fixture
def mock_openai_client():
    with patch('modules.luna_core.client') as mock_client:
        yield mock_client

@pytest.fixture
def sample_messages():
    return [
        {"role": "system", "content": "Test system prompt"},
        *[{"role": "user", "content": f"Message {i}"} for i in range(15)]
    ]

def test_manage_history_truncation(sample_messages):
    managed = manage_history(sample_messages)
    assert len(managed) == 14  # System + last 13 messages
    assert managed[0] == sample_messages[0]

def test_manage_history_no_truncation():
    messages = [{"role": "system", "content": "Test"}] + [
        {"role": "user", "content": f"Msg {i}"} for i in range(5)
    ]
    assert len(manage_history(messages)) == 6

def test_get_luna_response_stream(mock_openai_client):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(delta=MagicMock(content="Hello"))]
    mock_openai_client.chat.completions.create.return_value = [mock_response]

    messages = [{"role": "user", "content": "Hi"}]
    response = list(get_luna_response(messages))
    
    assert "Hello" in response[0]
    mock_openai_client.chat.completions.create.assert_called_once()

def test_get_luna_response_error_handling(mock_openai_client):
    mock_openai_client.chat.completions.create.side_effect = Exception("Test error")
    response = list(get_luna_response([{"role": "user", "content": "Hi"}]))
    assert "error" in response[0].lower()