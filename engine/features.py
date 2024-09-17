from playsound import playsound
from pipes import quote
import eel
import os
import re
from engine.command import speak
from engine.Assistantinfo import ASSISTANT_NAME
import mysql.connector
import webbrowser
import pywhatkit as kit
import struct
import pyaudio
import pvporcupine
import time
import subprocess
import pyautogui
from engine.helper import remove_words
from hugchat import hugchat

#from engine.helper import extract_yt_term

# Connect to MySQL
con = mysql.connector.connect(
    host="localhost",  # Change to your host
    user="ALICE",  # Change to your MySQL username
    password="krusanali",  # Change to your MySQL password
    database="alice"  # Change to your database name
)
cursor = con.cursor()

# Playing assistant sound function
@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "").strip().lower()

    app_name = query.strip()
      # if query!="":
    #     speak("Opening "+query)
    #     os.system('start '+query)
    # else:
    #      speak("not found")
    if app_name != "":
        try:
            # Fetch application path from the database
            cursor.execute('SELECT path FROM sys_command WHERE name = %s', (app_name,))
            results = cursor.fetchall()

            if results:
                speak(f"Opening {query}")
                os.startfile(results[0][0])

            else:
                # Fetch URL from the database
                cursor.execute('SELECT url FROM web_command WHERE name = %s', (app_name,))
                results = cursor.fetchall()

                if results:
                    speak(f"Opening {query}")
                    webbrowser.open(results[0][0])
                else:
                    speak(f"Trying to open {query}")
                    try:
                        os.system(f'start {query}')
                    except Exception as e:
                        speak("Application not found")
                        print("OS Command Error:", str(e))
        except mysql.connector.Error as err:
            speak("Something went wrong with the database operation")
            print("Database Error:", str(err))
        except Exception as e:
            speak("Something went wrong")
            print("General Error:", str(e))

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak(f"Playing {search_term} on YouTube")
    kit.playonyt(search_term)

def extract_yt_term(command):

    # Define a regular expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    # Use re.search to find the match in the command
    match = re.search(pattern, command, re.IGNORECASE)
    # If a match is found, return the extracted song name; otherwise, return None
    return match.group(1) if match else None


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:

        # pre trained keywords    
        #porcupine=pvporcupine.create(keywords=["alice","alexa"]) 
          # Load the custom model for "ALICE"
        porcupine = pvporcupine.create(
            access_key='SPgxFmsqO9hYOg22NVWyQvQaxgs3HgrUtsCk7sLmf2OC06SqZCGkGQ==',
            keyword_paths=[r"C:\Users\spand\Downloads\Hey-Alice_en_windows_v3_0_0\Hey-Alice_en_windows_v3_0_0.ppn"]
        )
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)

        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")

    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


# find contacts
def findContact(query):

    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)

    # Debugging: Check the final query after word removal
    print(f"Processed query after removing words: '{query}'")

    if not query:  # If query is empty after removing words
        print("Query is empty after word removal.")
        return 0, 0

    try:
        query = query.strip().lower()
        
        # Debugging: Show the final query passed to the SQL
        print(f"Final query for SQL: '{query}'")

        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE %s OR LOWER(name) LIKE %s", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()

        # Check if results were found
        if results:
            print(f"Mobile number found: {results[0][0]}")
            mobile_number_str = str(results[0][0])

            # Add country code if not present
            if not mobile_number_str.startswith('+91'):
                mobile_number_str = '+91' + mobile_number_str

            return mobile_number_str, query
        else:
            print("No contacts found.")
            return 0, 0

    except Exception as e:
        # Print detailed error for debugging
        print(f"An error occurred: {e}")
        return 0, 0


def whatsApp(mobile_no, message, flag, name):


    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)

    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response    