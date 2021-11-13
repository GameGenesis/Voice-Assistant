import speech_recognition as sr
import pyttsx3 as tts
import webbrowser
import wikipedia
import datetime
import urllib.request
import re
import random

import jokes

listener = sr.Recognizer()
engine = tts.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

name = "Joan"
user_name = ""

def play_yt(search_keyword: str):
    search_keyword = search_keyword.replace(" ", "+")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = f"https://www.youtube.com/watch?v={video_ids[0]}"
    webbrowser.get().open(url)

def search_web(voice_data, commands):
    command_str = f"{commands[0]} " if commands[0] in voice_data else "{command_strs[1]} "
    index_start = voice_data.find(command_str) + len(command_str)
    query = voice_data[index_start:]
    url = f"https://www.google.com/search?q={query}"
    webbrowser.get().open(url)

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

    if "play " in voice_data or "youtube " in voice_data or "video " in voice_data:
        if "video " in voice_data:
            command_str = "video "
        elif "youtube " in voice_data:
            command_str = "youtube "
        elif "play " in voice_data:
            command_str = "play "

        index_start = voice_data.find(command_str) + len(command_str)
        song = voice_data[index_start:]
        say_prompt(f"Playing {song}")
        play_yt(song)

    if "time" in voice_data:
        time = datetime.datetime.now().strftime("%I:%M %p")
        say_prompt(f"The time is {time}")

    if "who" in voice_data or "what" in voice_data or "when" in voice_data or "where" in voice_data:
        query = ""
        if "is " in voice_data:
            index_start = voice_data.find("is ") + len("is ")
            query = voice_data[index_start:]
        elif "are " in voice_data:
            index_start = voice_data.find("are ") + len("are ")
            query = voice_data[index_start:]
        elif "'s " in voice_data:
            index_start = voice_data.find("'s ") + len("'s' ")
            query = voice_data[index_start:]
        if "was " in voice_data:
            index_start = voice_data.find("was ") + len("was ")
            query = voice_data[index_start:]
        if "were " in voice_data:
            index_start = voice_data.find("were ") + len("were ")
            query = voice_data[index_start:]
        elif "did " in voice_data:
            index_start = voice_data.find("did ") + len("did ")
            index_end = voice_data.find("happen")
            query = voice_data[index_start:index_end]
        elif "does " in voice_data:
            index_start = voice_data.find("did ") + len("did ")
            index_end = voice_data.find("happen")
            query = voice_data[index_start:index_end]
        
        if query != "":
            try:
                try:
                    info = wikipedia.summary(query, 1)
                    say_prompt(info)
                    print(wikipedia.page(query).url)
                except:
                    info = wikipedia.summary(wikipedia.suggest(query), 1)
                    say_prompt(info)
                    print(wikipedia.page(wikipedia.suggest(query)).url)
            except wikipedia.PageError:
                pass

    if "search" in voice_data or "google" in voice_data:
        commands = ["search", "google"]
        search_web(voice_data.lower(), commands)

    if "joke" in voice_data:
        say_prompt(random.choice(jokes.jokes))

name = prompt_user()
while True:
    voice_data = record_audio()
    respond(voice_data, True)