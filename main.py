import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
import winsound
from dotenv import load_dotenv
import os

# ----------------------------
# Load API key from .env
# ----------------------------
load_dotenv()  # loads .env file
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# ----------------------------
# Init Recognizer + TTS
# ----------------------------
recognizer = sr.Recognizer()
recognizer.pause_threshold = 1

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  # male/female
engine.setProperty("rate", 170)
engine.setProperty("volume", 1)

print("🤖 Gemini Voice Assistant is ready! Say something... (say 'exit' to quit)")

# ----------------------------
# Main Loop
# ----------------------------
while True:
    with sr.Microphone() as source:
        winsound.Beep(100, 200)
        print("\n🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        print("🗣️ You said:", user_input)

        if user_input.lower() in ["exit", "stop", "quit"]:
            print("👋 Goodbye!")
            engine.say("Goodbye, have a nice day!")
            engine.runAndWait()
            break

        response = model.generate_content(user_input)
        gemini_text = response.text
        print("🤖 Gemini AI says:", gemini_text)

        engine.say(gemini_text)
        engine.runAndWait()

    except sr.UnknownValueError:
        print("❌ Sorry, I could not understand.")
    except sr.RequestError as e:
        print(f"⚠️ Could not request results; {e}")
