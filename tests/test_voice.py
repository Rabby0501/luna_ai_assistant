import pytest
from unittest.mock import patch, MagicMock
from modules.luna_core import speech_to_text, text_to_speech

@pytest.fixture
def mock_recognizer():
    with patch('modules.luna_core.sr.Recognizer') as mock:
        yield mock

@pytest.fixture
def mock_engine():
    with patch('modules.luna_core.TTS_ENGINE') as mock:
        yield mock

def test_speech_to_text_success(mock_recognizer):
    mock_recognizer.return_value.recognize_google.return_value = "Hello"
    assert speech_to_text() == "Hello"

def test_speech_to_text_failure(mock_recognizer):
    mock_recognizer.return_value.recognize_google.side_effect = Exception("Error")
    result = speech_to_text()
    assert "error" in result.lower()

def test_text_to_speech(mock_engine):
    text_to_speech("Test message")
    mock_engine.say.assert_called_with("Test message")
    mock_engine.runAndWait.assert_called_once()