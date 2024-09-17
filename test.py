import speech_recognition as sr
import pyautogui as autogui
import time

def hotword():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)

        print("Listening for the hotword 'ALICE'...")
        while True:
            audio = recognizer.listen(source)
            try:
                # Convert the audio to text
                transcription = recognizer.recognize_google(audio).lower()
                print(f"Recognized: {transcription}")

                # Check if "alice" was recognized
                if "alice" in transcription:
                    print("Hotword 'ALICE' detected")

                    # Press the shortcut key Win+J
                    autogui.keyDown("win")
                    autogui.press("j")
                    time.sleep(2)
                    autogui.keyUp("win")

            except sr.UnknownValueError:
                # Speech was unintelligible
                print("Could not understand audio")
            except sr.RequestError:
                # API was unreachable or unresponsive
                print("Could not request results from Google Speech Recognition service")

hotword()