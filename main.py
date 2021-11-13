import speech_recognition as sr #Recognize user voice input
import pyttsx3 as tts #Uses speech to text APIs
import webbrowser #Open URLs in a web browser
import wikipedia #Wikipedia Search
import datetime #Date and time
import urllib.request #URL handling
import re #Regular expressions

import jokes #Jokes file in project

#Speech recognizer
listener = sr.Recognizer()

#text to speech initialization
engine = tts.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id) #Use female voice

#global values
name = "Joan" #Voice assistant name
user_name = "" #User name

#Find most relevant (first) video on YouTube for the topic specified
def play_yt(search_keyword: str):
    search_keyword = search_keyword.replace(" ", "+")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = f"https://www.youtube.com/watch?v={video_ids[0]}"
    webbrowser.get().open(url)

#Google search
def search_web(voice_data, commands):
    command_str = f"{commands[0]} " if commands[0] in voice_data else f"{commands[1]} "
    index_start = voice_data.find(command_str) + len(command_str)
    query = voice_data[index_start:]
    url = f"https://www.google.com/search?q={query}"
    webbrowser.get().open(url)

#Text to speech implementation
def say_prompt(prompt):
    print(prompt)
    engine.say(prompt)
    engine.runAndWait()

#Introduction: Ask user for assistant name
def prompt_user():
    say_prompt("Hi, I will be your new virtual assistant! What would you like to call me?")
    name = record_audio()
    say_prompt(f"{name} at your service!")
    return name

#Get microphone audio and use google API to recognize speech
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

#Repsong to the user using tts based on the condition met for the voice command
#Sequential specifies whether the assistant name must be said
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

    elif "what" in voice_data and "your name" in voice_data:
        if user_name == "":
            say_prompt(f"My name is {name}! What's yours?")
            user_name = record_audio()
            say_prompt(f"Awesome! Nice to meet you {user_name}")
        else:
            say_prompt(f"My name is {name}!")
    
    elif name.lower() not in voice_data and not sequential:
        return
    
    elif "my name" in voice_data:
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

    elif "play " in voice_data or "youtube " in voice_data or "video " in voice_data:
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

    elif "time" in voice_data:
        time = datetime.datetime.now().strftime("%I:%M %p")
        say_prompt(f"The time is {time}")

    elif ("who" in voice_data or "what" in voice_data or "when" in voice_data or "where" in voice_data) and "your " not in voice_data:
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

    elif "search" in voice_data or "google" in voice_data:
        commands = ["search", "google"]
        search_web(voice_data, commands)

    elif "joke" in voice_data:
        say_prompt(jokes.get_joke())
    
    elif "exit" in voice_data:
        exit()
    
    else:
        small_talk_response = jokes.small_talk(voice_data)
        if small_talk_response is not None:
            say_prompt(small_talk_response)
    
    voice_data = ""

#Run assistant
name = prompt_user()
while True:
    voice_data = record_audio()
    respond(voice_data, True)