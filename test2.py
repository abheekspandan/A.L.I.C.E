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

# Establish MySQL connection
con = mysql.connector.connect(
    host="localhost",  # Change to your host
    user="ALICE",  # Change to your MySQL username
    password="krusanali",  # Change to your MySQL password
    database="alice"  # Change to your database name
)
cursor = con.cursor()

# Function to remove unnecessary words from query
def remove_words(input_string, words_to_remove):
    words = input_string.split()
    filtered_words = [word for word in words if word.lower() not in words_to_remove]
    result_string = ' '.join(filtered_words)
    return result_string

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

# Test the function with the query
query = 'send message to Daddy'
findContact(query)
