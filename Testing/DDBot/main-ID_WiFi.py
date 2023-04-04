import speech_recognition as sr
import pyautogui
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import time
import datetime
import webbrowser
from time import ctime
import wikipedia as wiki
import requests
import os
import httpx

def record_audio(ask='None'):
    with sr.Microphone() as source:
        if ask != 'None':
            speak(ask)
        print('Mulai Bicara')

        audio = r.listen(source=source, timeout=10, phrase_time_limit=7)
        print('Mengenali...')
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio_data=audio, language="id-ID")
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            
            speak('Maaf server sedang sibuk')
            
        print(f">> {voice_data.lower()}")  # type: ignore
        return voice_data.lower()# type: ignore

def respond(voice_data):

    if there_exists(['hai', 'hi', 'hello', 'halo', 'hai robot', 'hi robot', 'halo robot']):
        
        
        greetings = f"hai, bagaimana saya bisa membantu " + username

        speak(greetings)
        
        

    elif there_exists(["apa kabarmu", "apa kabar", "Bagaimana kabarmu"]):
        
        speak(f"Saya sangat baik, terimakasih telah bertanya, bagaimana dengan anda " + username)
    
    elif there_exists(["siapa namamu", "namamu siapa"]):
        
        speak(f"Nama saya adalah " + myname + " versi " + ver + "seenggol dong!")
        
    elif there_exists(["bisakah anda membantu saya", "bisakah kamu membantu saya", "bisakah kamu menolong saya", "bisakah anda menolong saya", "bantu saya", "tolong saya"]):
        
        speak(f"Tentu saja aku bisa menolongmu")

    elif there_exists(["ceritakan tentang dirimu", "ceritakan tentang kamu", "siapa anda", "siapa kamu"]):
        d = datetime.datetime.now().year
        speak(f"Nama saya " + myname + " versi " + ver + ". Aku dibuat oleh seorang anak bernama Dean Putra, Sekarang umurnya " + str(d-2010) + "Tahun. Dia sangat suka programming, Dia berasal dari Buleleng, Bali")
        

    elif there_exists(["hentikan musik", "musik berhenti"]):
        try:
            httpx.get("http://" + ipaddr + "/?a=1")
        except:
            pass
        speak(f"Menghentikan...")

    elif there_exists(["mainkan musik", "musik"]):
        req = voice_data.split("music")[-1]
        speak(f"Memainkan...")
        if 'satu' in req:
            try:
                httpx.get("http://" + ipaddr + "/?a=c")
            except:
                pass
        elif 'dua' in req:
            try:
                httpx.get("http://" + ipaddr + "/?a=w")
            except:
                pass
        elif 'tiga' in req:
            try:
                httpx.get("http://" + ipaddr + "/?a=m")
            except:
                pass
        elif 'empat' in req:
            try:
                httpx.get("http://" + ipaddr + "/?a=q")
            except:
                pass
        


    elif there_exists(["jam berapa sekarang", "katankan jam berapa sekarang", "sekarang jam berapa"]):
        
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = f"Sekarang jam {hours} {minutes}"
        speak(time)
        

    elif there_exists(["bagaimana cuacanya", "bagaimana cuaca sekarang", "bagaimana cuaca hari ini"]):
        
        weather_data = requests.get(Final_url).json()
        temp = weather_data['main']['temp']
 
        wind_speed = weather_data['wind']['speed']
 
        description = weather_data['weather'][0]['description']

        final_text = "Cuaca: " + description + ", Suhu: " + str(temp-273.15) + " derajat celcius, Kecepatan Angin: " + str(wind_speed) + "Kilometer per jam"
        
        print(final_text)
        speak(final_text)
        


    elif there_exists(["cari di google tentang"]):
        search_term = voice_data.split("cari di google tentang")[-1]
        if search_term != '':
            url = f"https://google.com/search?q={search_term}"
            webbrowser.get().open(url)
            speak(f'Ini adalah apa yang saya dapat untuk {search_term} di google')
            


    elif there_exists(["putar video youtube tentang"]):
        search_term = voice_data.split("putar video youtube tentang")[-1]
        if search_term != '':
            url = f"https://www.youtube.com/results?search_query={search_term}"
            webbrowser.get().open(url)
            
            speak(f'Ini adalah apa yang saya dapat untuk {search_term} di youtube, mengklik....')
            try:
                pyautogui.moveTo(650, 350, duration=1)
                pyautogui.leftClick()
            except pyautogui.FailSafeException:
                pass


    elif there_exists(['cari di wikipedia tentang']):
        search_term = voice_data.split("cari di wikipedia tentang")[-1]
        f = ""
        try:
            f = wiki.summary(search_term, sentences=5)
        except wiki.exceptions.PageError:
            pass
        print(f)
        speak(f)
        


    elif there_exists(["shutdown", "selamat tinggal", "matikan sistem", "sampai jumpa"]):
        
        speak("mematikan sistem...")
        
        try:
            httpx.get("http://" + ipaddr + "/?a=2", timeout=timeout)
        except:
            pass
        exit()

def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True

def speak(audio_string):

    try:
        tts = gTTS(text=audio_string, lang='id')
        tts.save('ttstmp.mp3')
        song = AudioSegment.from_mp3('ttstmp.mp3')
        
        try:
            httpx.get("http://" + ipaddr + "/?a=.", timeout=timeout)
        except:
            print("p")
            pass
        play(song)
    except:
        pass

    try:
        httpx.get("http://" + ipaddr + "/?a=,", timeout=timeout)
    except:
        print("p")
        pass




timeout = httpx.Timeout(10.0, connect_timeout=60.0)


try:
    os.remove('ttstmp.mp3')
except:
    pass

API_key = "78c067d5244c3b1392a1de0288f15207"
 

base_url = "http://api.openweathermap.org/data/2.5/weather?"
 

city_id = "Singaraja"

Final_url = base_url + "appid=" + API_key + "&q=" + city_id
username = "Bos"
myname = "D D Bot"
ver = "1"
ipaddr = input("Masukkan IP dari robot: ")

try:
    httpx.get("http://" + ipaddr + "/?a=3", timeout=timeout)
    print("Badan Robot, Terhubung")
except:
    print("Tidak Bisa Terhubung Ke Badan Robot, Sebaiknya hubungkan untuk pengalaman yang lebih baik")
    pass

listener = sr.Recognizer()



r = sr.Recognizer()



speak('Selamat Datang ' + username)





time.sleep(1)

while (1):
    voice_data = record_audio()
    respond(voice_data)