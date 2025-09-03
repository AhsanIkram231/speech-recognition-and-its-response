import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
import winsound  # for beep sound (Windows only)

# ----------------------------
# Configure Gemini
# ----------------------------
genai.configure(api_key="AIzaSyCy1ofN1VFRiXohwSPlzuqu_6PsFOhqgTc")
model = genai.GenerativeModel("models/gemini-1.5-flash")

# ----------------------------
# Init Recognizer + TTS
# ----------------------------
recognizer = sr.Recognizer()
recognizer.pause_threshold = 1  # wait for 1 sec of silence before ending speech

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  # change index for male/female
engine.setProperty("rate", 170)
engine.setProperty("volume", 1)

print("🤖 Gemini Voice Assistant is ready! Say something... (say 'exit' to quit)")

# ----------------------------
# Main Loop
# ----------------------------
while True:
    with sr.Microphone() as source:
        # 🔔 Beep before listening
        winsound.Beep(100, 200)  # frequency=1000Hz, duration=200ms

        print("\n🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        audio = recognizer.listen(source)

    try:
        # Convert speech to text
        user_input = recognizer.recognize_google(audio)
        print("🗣️ You said:", user_input)

        # Exit condition
        if user_input.lower() in ["exit", "stop", "quit"]:
            print("👋 Goodbye!")
            engine.say("Goodbye, have a nice day!")
            engine.runAndWait()
            break

        # ----------------------------
        # Send text to Gemini
        # ----------------------------
        response = model.generate_content(user_input)
        gemini_text = response.text
        print("🤖 Gemini AI says:", gemini_text)

        # Speak response
        engine.say(gemini_text)
        engine.runAndWait()

    except sr.UnknownValueError:
        print("❌ Sorry, I could not understand.")
    except sr.RequestError as e:
        print(f"⚠️ Could not request results; {e}")
