import speech_recognition as sr
import pyttsx3 as tts

listener = sr.Recognizer()

name = "Joan"
user_name = ""

def prompt_user():
    print("Hi, I will be your new virtual assistent! What would you like to call me!")
    name = record_audio()
    print(f"{name} at your service!")
    return name

def record_audio():
    with sr.Microphone() as source:
        audio = listener.listen(source)
        voice_data = ""
        try:
            voice_data = listener.recognize_google(audio)
        except:
            pass
        return voice_data

def respond(voice_data):
    voice_data = voice_data.lower()
    global user_name

    if "what" in voice_data and "your name" in voice_data:
        if user_name == "":
            print(f"My name is {name}! What's yours?")
            user_name = record_audio()
            print(f"Awesome! Nice to meet you {user_name}")
        else:
            print(f"My name is {name}!")
    
    if name.lower() not in voice_data:
        return
    
    if "my name" in voice_data:
        if user_name == "":
            print(f"I don't know! What is it?")
            user_name = record_audio()
        else:
            print(f"I remember you told me it was {user_name}. Is that right?")
            reply = record_audio()
            if reply == "no":
                print("Oh! What is it?")
                user_name = record_audio()
                print(f"Awesome! Nice to meet you {user_name}")
            elif "yes":
                print("Awesome")
            else:
                return

    
name = prompt_user()
while True:
    voice_data = record_audio()
    respond(voice_data)