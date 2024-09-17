import pyaudio
import pvporcupine
import time
import struct

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        # Load the custom model for "ALICE"
        porcupine = pvporcupine.create(
            access_key='SPgxFmsqO9hYOg22NVWyQvQaxgs3HgrUtsCk7sLmf2OC06SqZCGkGQ==',
            keyword_paths=[r"C:\Users\spand\Downloads\Hey-Alice_en_windows_v3_0_0\Hey-Alice_en_windows_v3_0_0.ppn"]
        )
        
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)

        # Loop for streaming
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            # Processing keyword from mic
            keyword_index = porcupine.process(keyword)

            # Checking if the keyword was detected
            if keyword_index >= 0:
                print("Hotword 'ALICE' detected")

                # Pressing shortcut key Win+J
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

hotword()   