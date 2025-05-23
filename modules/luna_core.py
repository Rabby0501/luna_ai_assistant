import os
import openai
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
from openai import OpenAI
from typing import Generator

# Initialize environment
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Voice Configuration ---
TTS_ENGINE = pyttsx3.init()
TTS_ENGINE.setProperty('rate', 150)
TTS_ENGINE.setProperty('volume', 0.9)
TTS_VOICE = TTS_ENGINE.getProperty('voices')[1].id  # Female voice
TTS_ENGINE.setProperty('voice', TTS_VOICE)

# --- AI Configuration ---
MODEL_NAME = "gpt-3.5-turbo"
MAX_HISTORY = 14
TEMPERATURE = 0.75

LUNA_SYSTEM_PROMPT = """
[Previous system prompt with enhancements]
You can now understand and generate speech.
When appropriate, add sound-related emojis like 🎵🔊🎶
"""

def manage_history(messages: list) -> list:
    """Optimize conversation context"""
    return [messages[0]] + messages[-(MAX_HISTORY-1):] if len(messages) > MAX_HISTORY else messages

def text_to_speech(text: str) -> None:
    """Convert text to speech with error handling"""
    try:
        TTS_ENGINE.say(text)
        TTS_ENGINE.runAndWait()
    except Exception as e:
        print(f"TTS Error: {str(e)}")

def speech_to_text() -> str:
    """Convert speech to text using microphone"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source, timeout=10)
        try:
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            return "Could you please repeat that?"
        except Exception as e:
            return f"Voice error: {str(e)}"

def get_luna_response(messages: list) -> Generator[str, None, None]:
    """Generate streaming response with enhanced error handling"""
    try:
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=manage_history(messages),
            temperature=TEMPERATURE,
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        yield f"🌧️ Oops! A little hiccup: {str(e)}. Let's try again?"