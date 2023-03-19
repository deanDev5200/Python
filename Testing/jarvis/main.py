import speech_recognition as sr  # recognise speech
import pyautogui
import pyttsx3
import time
import webbrowser  # open browser
from time import ctime
import serial  # control arduino
import wikipedia as wiki  # Webscrapes wikipedia content.
import requests
 
# API KEY
API_key = "78c067d5244c3b1392a1de0288f15207"
 
# This stores the url
base_url = "http://api.openweathermap.org/data/2.5/weather?"
 
# This will ask the user to enter city ID
city_id = "Singaraja"
 
# This is final url. This is concatenation of base_url, API_key and city_id
Final_url = base_url + "appid=" + API_key + "&q=" + city_id
username = "Master"
try:
    port = serial.Serial(port="COM5", baudrate=115200)
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
            voice_data = r.recognize_google(audio, "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw")  # convert audio to text
        except sr.UnknownValueError:  # error: recognizer does not understand
            port.write(b'.')
            speak('I did not get that')
            port.write(b',')
        except sr.RequestError:
            port.write(b'.')
            speak('Sorry, the service is down')  # error: recognizer is not connected
            port.write(b',')
        print(f">> {voice_data.lower()}")  # type: ignore
        return voice_data.lower()# type: ignore


# get string and make a audio file to be played
def speak(audio_string):
    engine.say(audio_string)
    engine.runAndWait()


speak('Welcome ' + username)


def respond(voice_data):
    # 1: greeting
    if there_exists(['hey', 'hi', 'hello']):
        port.write(b'.')
        
        greetings = [f"hey, how can I help you " + username]

        speak(greetings)
        port.write(b',')
        
    # 3: greeting
    if there_exists(["how are you", "how are you doing"]):
        port.write(b'.')
        speak(f"I'm very well, thanks for asking " + username)
        port.write(b',')

    # 4: time
    if there_exists(["what's the time", "tell me the time", "what time is it"]):
        port.write(b'.')
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = f'{hours} {minutes}'
        speak(time)
        port.write(b',')

    if there_exists(["what's the weather", "how's the weather", "how is the weather today"]):
        port.write(b'.')
        weather_data = requests.get(Final_url).json()
        temp = weather_data['main']['temp']
 
        wind_speed = weather_data['wind']['speed']
 
        description = weather_data['weather'][0]['description']

        final_text = "Weather: " + description + ", Temperature: " + str(temp-273.16) + " degrees celcius, Wind Speed: " + str(wind_speed) + "KM/H"
        
        speak(final_text);
        print(final_text);
        port.write(b',')

    if there_exists(["f***", "s***"]):
        port.write(b'.')
        speak("Moving On. By The Way you are a little piece of sh*t,")
        port.write(b',')
        exit()

    # 5: search google
    if there_exists(["search for"]) and 'youtube' not in voice_data:
        port.write(b'.')
        search_term = voice_data.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on google')
        port.write(b',')

    # 6: search youtube
    if there_exists(["play"]):
        port.write(b'.')
        search_term = voice_data.split("play")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on youtube, clicking....')
        pyautogui.moveTo(650, 300, duration=1)
        pyautogui.leftClick()
        port.write(b',')

    # 7: wikipedia summary
    if there_exists(['summarise']):
        port.write(b'.')

        search_term = voice_data.split("summarise")[-1]
        speak(wiki.summary(search_term, sentences=5))
        port.write(b',')

    if there_exists(['summarize']):
        port.write(b'.')

        search_term = voice_data.split("summarize")[-1]
        speak(wiki.summary(search_term, sentences=5))
        port.write(b',')

    # shutdown program
    if there_exists(["exit", "quit", "goodbye"]):
        port.write(b'.')
        speak("going offline")
        port.write(b',')
        exit()


time.sleep(1)

while (1):
    voice_data = record_audio()  # get the voice input
    respond(voice_data)  # respond