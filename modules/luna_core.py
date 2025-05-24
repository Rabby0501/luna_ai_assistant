import os
import httpx
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
from openai import OpenAI
from typing import Generator

# ---- Configuration ----
# ---- Configuration ----
load_dotenv()
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# With this proxy-disabled client:
# Initialize OpenAI client with proxy handling
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    http_client=httpx.Client(
        transport=httpx.HTTPTransport(
            retries=3,
            proxy=None  # Explicitly disable proxies
        )
    )
)

# ---- Constants ----
LUNA_SYSTEM_PROMPT = """
You are 'Luna', a cheerful AI assistant. Use emojis 🌸✨, be supportive, and stay positive.
Always respond kindly. Your hobbies: stargazing, tea, and helping humans.
"""

# ---- Voice Engine ----
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)
tts_engine.setProperty('volume', 0.9)

# ---- Core Functions ----
def manage_history(messages: list) -> list:
    return [messages[0]] + messages[-13:] if len(messages) > 14 else messages

def text_to_speech(text: str) -> None:
    try:
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")

def speech_to_text() -> str:
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=8)
            return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could you please repeat that?"
    except Exception as e:
        return f"Error: {str(e)}"

def get_luna_response(messages: list) -> Generator[str, None, None]:
    try:
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=manage_history(messages),
            temperature=0.7,
            stream=True
        )
        for chunk in stream:
            if content := chunk.choices[0].delta.content:
                yield content
    except Exception as e:
        yield f"🌧️ Oops! A little hiccup: {str(e)}"