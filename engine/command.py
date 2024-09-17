import pyttsx3
import speech_recognition as sr
import eel
import time
import webbrowser

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 174)
    volume = engine.getProperty('volume')
    engine.setProperty('volume',1)    
    print(voices)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        #query = r.recognize_google(audio,language = 'en-hi')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        # speak(query)
        time.sleep(2)
        #eel.ShowHood()

    except Exception as e:
        return ""

    return query.lower()


# text = takecommand()

# #speak("India is my country, all indians are my brothers and sisters")
# speak(text)

@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message

        eel.senderText(query)
    try:
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "send message" in query or "make phone call" in query or "make video call" in query:
            from engine.features import findContact, whatsApp
            flag = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    flag = 'message'
                    speak("what message to send")
                    query = takecommand()

                elif "phone call" in query:
                    flag = 'call'
                else:
                    flag = 'video call'

                whatsApp(contact_no, query, flag, name)

        else:
            # print("unable to run")
            from engine.features import chatBot
            chatBot(query)

    except:
        print("error in giving commands")  

    eel.ShowHood()
