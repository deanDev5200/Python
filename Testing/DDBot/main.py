import speech_recognition as sr  # recognise speech
import pyautogui
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import time
import datetime
import webbrowser  # open browser
from time import ctime
import serial  # control arduino
import wikipedia as wiki  # Webscrapes wikipedia content.
import requests
import os

p = os.system('del ttstmp.mp3')

API_key = "78c067d5244c3b1392a1de0288f15207"
 

base_url = "http://api.openweathermap.org/data/2.5/weather?"
 

city_id = "Singaraja"

def speak(audio_string):
    port.write(b'.')
    tts = gTTS(text=audio_string, lang='en')
    try:
        tts.save('ttstmp.mp3')
    except TypeError:
        pass
    song = AudioSegment.from_mp3('ttstmp.mp3')
    play(song)
    port.write(b',')
# This is final url. This is concatenation of base_url, API_key and city_id
Final_url = base_url + "appid=" + API_key + "&q=" + city_id
username = "Master"
myname = "DDBot"
ver = "1"
try:
    port = serial.Serial(port="COM5", baudrate=115200)
    print("Physical body, connected.")
except:
    print("Unable to connect to my physical body")

listener = sr.Recognizer()


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
        print('Start')

        audio = r.listen(source=source, timeout=10, phrase_time_limit=7)
        print('Recognizing...')
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio_data=audio, language="en-US")  # convert audio to text
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            
            speak('Sorry, the service is down')  # error: recognizer is not connected
            
        print(f">> {voice_data.lower()}")  # type: ignore
        return voice_data.lower()# type: ignore


# get string and make a audio file to be played

port.write(b'%') # type: ignore

speak('Welcome ' + username)


def respond(voice_data):
    # 1: greeting
    if there_exists(['hey', 'hi', 'hello']):
        
        
        greetings = [f"hey, how can I help you " + username]

        speak(greetings)
        
        
    # 3: greeting
    elif there_exists(["how are you", "how are you doing"]):
        
        speak(f"I'm very well, thanks for asking " + username)
    
    elif there_exists(["what's your name", "what is your name"]):
        
        speak(f"My name is " + myname + " version " + ver)
        
    elif there_exists(["can you help me", "please help me"]):
        
        speak(f"Of course i can help you")

    elif there_exists(["tell me about your ", "tell me about yourself"]):
        d = datetime.datetime.now().year
        speak(f"My name is " + myname + " version " + ver + ". I created by a young boy named Dean Putra, he is" + str(d-2010) + "years old and he really likes programming")
        

    elif there_exists(["stop the music", "music stop"]):
        port.write(b'!')# type: ignore
        speak(f"Stopping...")

    elif there_exists(["play the music", "music"]):
        req = voice_data.split("music")[-1]
        speak(f"Playing...")
        if 'one' in req:
            port.write(b'c')# type: ignore
        elif 'too' in req:
            port.write(b'w')# type: ignore
        elif 'two' in req:
            port.write(b'w')# type: ignore
        elif 'to' in req:
            port.write(b'w')# type: ignore
        elif 'three' in req:
            port.write(b'q')# type: ignore
        elif 'four' in req:
            port.write(b'm')# type: ignore
        elif 'for' in req:
            port.write(b'm')# type: ignore
        

    # 4: time
    elif there_exists(["what's the time", "tell me the time", "what time is it"]):
        
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = f"it's {hours} {minutes}"
        speak(time)
        

    elif there_exists(["what's the weather", "how's the weather", "how is the weather today"]):
        
        weather_data = requests.get(Final_url).json()
        temp = weather_data['main']['temp']
 
        wind_speed = weather_data['wind']['speed']
 
        description = weather_data['weather'][0]['description']

        final_text = "Weather: " + description + ", Temperature: " + str(temp-273.15) + " degrees celcius, Wind Speed: " + str(wind_speed) + "KM/H"
        
        print(final_text)
        speak(final_text)
        

    # 5: search google
    elif there_exists(["search on google for"]):
        search_term = voice_data.split("search on google for")[-1]
        if search_term != '':
            url = f"https://google.com/search?q={search_term}"
            webbrowser.get().open(url)
            speak(f'Here is what I found for {search_term} on google')
            

    # 6: search youtube
    elif there_exists(["play the video"]):
        search_term = voice_data.split("play the video")[-1]
        if search_term != '':
            url = f"https://www.youtube.com/results?search_query={search_term}"
            webbrowser.get().open(url)
            
            speak(f'Here is what I found for {search_term} on youtube, clicking....')
            try:
                pyautogui.moveTo(650, 300, duration=1)
                pyautogui.leftClick()
            except pyautogui.FailSafeException:
                pass

    # 7: wikipedia summary
    elif there_exists(['summarise']):
        

        search_term = voice_data.split("summarise")[-1]
        speak(wiki.summary(search_term, sentences=5))
        

    elif there_exists(['summarize']):
        

        search_term = voice_data.split("summarize")[-1]
        f = ""
        try:
            f = wiki.summary(search_term, sentences=5)
        except wiki.exceptions.PageError:
            pass
        print(f)
        speak(f)
        

    # shutdown program
    elif there_exists(["exit", "quit", "goodbye"]):
        
        speak("going offline")
        
        port.write(b'#') #type: ignore
        exit()




time.sleep(1)

while (1):
    voice_data = record_audio()  # get the voice input
    respond(voice_data)  # respond