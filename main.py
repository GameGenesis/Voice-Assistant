import speech_recognition as sr #Recognize user voice input
import pyttsx3 as tts #Uses speech to text APIs
import webbrowser #Open URLs in a web browser
import wikipedia #Wikipedia Search
import datetime #Date and time
import urllib.request #URL handling
import re #Regular expressions
from bs4 import BeautifulSoup
import requests

import jokes #Jokes file in project

#Speech recognizer
listener = sr.Recognizer()

#text to speech initialization
engine = tts.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id) #Use female voice

#global values
name = "Riley" #Voice assistant name
user_name = "" #User name
prompt = False #Introduction prompt

#Check if either of the commands are present in the voice data
def command_exists(voice_data, terms):
    if type(terms) is str:
        if terms in voice_data:
            return True
        else:
            return False
    for term in terms:
        if term in voice_data:
            return True
    return False

#Check if all of the commands are present in the voice data
def command_exists_all(voice_data, terms):
    for term in terms:
        if term not in voice_data:
            return False
    return True

#Find most relevant (first) video on YouTube for the topic specified
def play_yt(query: str):
    query = query.replace(" ", "+")
    html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={query}")
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = f"https://www.youtube.com/watch?v={video_ids[0]}"
    webbrowser.get().open(url)

#Google search
def search_web(voice_data, commands):
    command_str = commands[0] if commands[0] in voice_data else commands[1]
    index_start = voice_data.find(command_str) + len(command_str)
    query = voice_data[index_start:]
    url = f"https://www.google.com/search?q={query}"
    webbrowser.get().open(url)
    say_prompt(f"Here's what I found for {query}")

#Google Maps search
def find_location(voice_data, commands):
    for c in commands:
        if c in voice_data:
            command_str = c
            break
    
    index_start = voice_data.find(command_str) + len(command_str)
    query = voice_data[index_start:]
    url = f"https://www.google.ca/maps/place/{query}"
    webbrowser.get().open(url)
    say_prompt(f"Here's a map of {query}")

def weather_data(voice_data, commands):
    # enter city name
    for c in commands:
        if c in voice_data:
            command_str = c
            break
    
    index_start = voice_data.find(command_str) + len(command_str)
    query = voice_data[index_start:]
    query = query.replace(" ", "+")

    # creating url and requests instance
    url = f"https://www.google.com/search?q=weather+{query}"
    html = requests.get(url).content

    try:
        # getting raw data
        soup = BeautifulSoup(html, "html.parser")
        temp = soup.find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"}).text
        str = soup.find('div', attrs={"class": "BNeawe tAd8D AP7Wnd"}).text

        # formatting data
        data = str.split("\n")
        time = data[0]
        sky = data[1]

        # printing all data
        say_prompt(f"The weather in {query} on {time} is {sky} with a temperature of {temp}.")
    except:
        say_prompt(f"Sorry, I could not find any weather data for {query}.")


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
        return voice_data

#Respond to the user using tts based on the condition met for the voice command
#Wakeup command specifies whether the assistant name must be said
def respond(voice_data, wake_up_command=True):    
    voice_data = voice_data.lower()
    global user_name

    if command_exists_all(voice_data, ["what", "your name"]):
        if user_name == "":
            say_prompt(f"My name is {name}! What's yours?")
            user_name = record_audio()
            say_prompt(f"Awesome! Nice to meet you {user_name}")
        else:
            say_prompt(f"My name is {name}!")
    
    elif name.lower() not in voice_data and wake_up_command:
        return
    
    elif command_exists(voice_data, "my name"):
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

    elif command_exists(voice_data, ["video ", "youtube ", "play "]):
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

    elif command_exists(voice_data, "time"):
        time = datetime.datetime.now().strftime("%I:%M %p")
        say_prompt(f"The time is {time}")

    elif command_exists(voice_data, ["search ", "google "]):
        commands = ["search ", "google "]
        search_web(voice_data, commands)

    elif command_exists(voice_data, ["find ", "where ", "location "]):
        commands = ["is ", "are ", "of ", "find ", "where ", "location "]
        find_location(voice_data, commands)
    
    elif command_exists(voice_data, ["weather ", "temperature ", "humidity "]):
        commands = ["in ", "of ", "weather ", "temperature ", "humidity "]
        weather_data(voice_data, commands)

    elif command_exists(voice_data, ["who", "what", "when"]) and "your " not in voice_data:
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

    elif command_exists(voice_data, "joke"):
        say_prompt(jokes.get_joke())
    
    elif command_exists(voice_data, "exit"):
        exit()
    
    else:
        small_talk_response = jokes.small_talk(voice_data)
        if small_talk_response is not None:
            say_prompt(small_talk_response)
    
    voice_data = ""

#Run assistant
if prompt:
    name = prompt_user()
while True:
    voice_data = record_audio()
    respond(voice_data, False)