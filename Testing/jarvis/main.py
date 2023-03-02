import speech_recognition as sr  # recognise speech
from gtts import gTTS  # google text to speech
import random
import pyautogui
import pyttsx3
from time import ctime  # get time details
import webbrowser  # open browser
import time
import serial  # control arduino
import wikipedia as wiki  # Webscrapes wikipedia content.
import requests
from pprint import pprint
 
# API KEY
API_key = "78c067d5244c3b1392a1de0288f15207"
 
# This stores the url
base_url = "http://api.openweathermap.org/data/2.5/weather?"
 
# This will ask the user to enter city ID
city_id = "Jakarta"
 
# This is final url. This is concatenation of base_url, API_key and city_id
Final_url = base_url + "appid=" + API_key + "&q=" + city_id
username = "Master"
try:
    port = serial.Serial("COM6", 9600)
    print("Physical body, connected.")
except:
    print("Unable to connect to my physical body")

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def there_exists(terms):
    print("...")
    for term in terms:
        if term in voice_data:
            return True


r = sr.Recognizer()  # initialise a recogniser


# listen for audio and convert it to text:
def record_audio(ask=False):
    with sr.Microphone() as source:  # microphone as source
        if ask:
            speak(ask)

        audio = r.listen(source)  # listen for the audio via source
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)  # convert audio to text
        except sr.UnknownValueError:  # error: recognizer does not understand
            speak('I did not get that')
        except sr.RequestError:
            speak('Sorry, the service is down')  # error: recognizer is not connected
        print(f">> {voice_data.lower()}")  # print what user said
        return voice_data.lower()


# get string and make a audio file to be played
def speak(audio_string):
    engine.say(audio_string)
    engine.runAndWait()


speak('Welcome ' + username)


def respond(voice_data):
    # 1: greeting
    if there_exists(['hey', 'hi', 'hello']):
        
        greetings = [f"hey, how can I help you " + username]

        speak(greetings)
        port.write(b'p')
        
    # 3: greeting
    if there_exists(["how are you", "how are you doing"]):
        speak(f"I'm very well, thanks for asking " + username)

    # 4: time
    if there_exists(["what's the time", "tell me the time", "what time is it"]):
        port.write(b'u')
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = f'{hours} {minutes}'
        speak(time)

    if there_exists(["what's the weather", "how's the weather", "how is the weather today"]):
        weather_data = requests.get(Final_url).json()
        temp = weather_data['main']['temp']
 
        wind_speed = weather_data['wind']['speed']
 
        description = weather_data['weather'][0]['description']

        final_text = "Weather: " + description + ", Temperature: " + str(temp-273.16) + " degrees celcius, Wind Speed: " + str(wind_speed) + "KM/H"
        
        speak(final_text);
        print(final_text);

    if there_exists(["what the hell", "f***", "s***"]):
        speak("Moving On. By The Way you are a little piece of shit,")
        exit()

    # 5: search google
    if there_exists(["search for"]) and 'youtube' not in voice_data:
        port.write(b'u')
        port.write(b'l')
        search_term = voice_data.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on google')

    # 6: search youtube
    if there_exists(["play"]):
        port.write(b'l')
        port.write(b'u')
        search_term = voice_data.split("play")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on youtube, clicking....')
        pyautogui.moveTo(650, 300, duration=1)
        pyautogui.leftClick()

    # 7: wikipedia summary
    if there_exists(['summarise']):
        port.write(b'u')
        port.write(b'l')

        search_term = voice_data.split("summarise")[-1]
        speak(wiki.summary(search_term, sentences=5))

    if there_exists(['summarize']):
        port.write(b'u')
        port.write(b'l')

        search_term = voice_data.split("summarize")[-1]
        speak(wiki.summary(search_term, sentences=5))

    if there_exists(["combat mode"]):
        speak('uppercut')
        port.write(b'U')
        speak('Jarvis smash!')
        port.write(b's')
        speak('yessir')

    # shutdown program
    if there_exists(["exit", "quit", "goodbye"]):
        speak("going offline")
        port.write(b'u')
        exit()


time.sleep(1)

while (1):
    voice_data = record_audio()  # get the voice input
    respond(voice_data)  # respond