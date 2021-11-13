from math import trunc
from posixpath import commonpath
import speech_recognition as sr
import pyttsx3 as tts
import pywhatkit
import webbrowser
import wikipedia
import datetime

listener = sr.Recognizer()
engine = tts.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

name = "Joan"
user_name = ""

def say_prompt(prompt):
    print(prompt)
    engine.say(prompt)
    engine.runAndWait()

def prompt_user():
    say_prompt("Hi, I will be your new virtual assistant! What would you like to call me?")
    name = record_audio()
    say_prompt(f"{name} at your service!")
    return name

def record_audio():
    with sr.Microphone() as source:
        print("Listening...")
        listener.adjust_for_ambient_noise(source)
        audio = listener.listen(source)
        voice_data = ""
        try:
            voice_data = listener.recognize_google(audio)
        except:
            pass
        print(voice_data)
        return voice_data

def respond(voice_data, sequential=False):
    voice_data = voice_data.lower()
    global user_name

    if "what" in voice_data and "your name" in voice_data:
        if user_name == "":
            say_prompt(f"My name is {name}! What's yours?")
            user_name = record_audio()
            say_prompt(f"Awesome! Nice to meet you {user_name}")
        else:
            say_prompt(f"My name is {name}!")
    
    if name.lower() not in voice_data and not sequential:
        return
    
    if "my name" in voice_data:
        if user_name == "":
            say_prompt(f"I don't know! What is it?")
            user_name = record_audio()
        else:
            say_prompt(f"I remember you told me it was {user_name}. Is that right?")
            reply = record_audio()
            if reply == "no":
                say_prompt("Oh! What is it?")
                user_name = record_audio()
                say_prompt(f"Awesome! Nice to meet you {user_name}")
            elif "yes":
                say_prompt("Awesome")
            else:
                return


name = prompt_user()
while True:
    voice_data = record_audio()
    respond(voice_data, True)