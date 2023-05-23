import pyautogui
import speech_recognition as sr
from gtts import gTTS
from bs4 import BeautifulSoup
import requests
import webbrowser
from pydub import AudioSegment
from pydub.playback import play
import time
import datetime
from time import ctime
import serial
import wikipedia as wiki
import requests
import os
question_words = ["apa", "apakah", "siapa", "bagaimana", "kenapa", "kapan", "dimana", 
              "mengapa", "pernahkah", 
             "mana", "bisakah", "maukah", 
             "haruskah", "punyakah", "berapa", "berapakah"]

def find_wiki(q:str):
    p = "Aku tidak menemukan apapun"
    try:
        p = wiki.page(q)
        return p.content.split("\n")[0]
    except:
        return p

def answer_question(question:str):
    respond = "Saya tidak mengerti"

    print(respond)
    speak(respond)
bangun = False


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
        except sr.RequestError:
            exit()
        except:
            pass
            
        print(f">> {voice_data.lower()}")  # type: ignore
        return voice_data.lower()# type: ignore

def speak(audio_string):

    try:
        tts = gTTS(text=audio_string, lang='id')
        tts.save('ttstmp.mp3')
        song = AudioSegment.from_mp3('ttstmp.mp3')
        
        try:
            port.write(b'.') #type: ignore
        except:
            pass
        play(song)
    except:
        pass

    try:
        port.write(b',') #type: ignore
    except:
        pass

def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True

def earthquake():
    content = 'https://www.bmkg.go.id/'
    req = requests.get(content)
    soup = BeautifulSoup(req.text, 'html.parser')
    date = soup.find('span', {'class': 'waktu'}).string.split(', ') #type: ignore

    nondate = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
    nondate = nondate.findChildren('li') #type: ignore

    magnitude = "0"
    depth = "99 km"
    loc = "laut"

    i = 0
    for j in nondate:

        if i == 1:
            magnitude = j.text
        elif i == 2:
            depth = j.text
        elif i == 4:
            loc = j.text
        i = i + 1

    datt = dict()
    datt['date'] = date
    datt['magnitude'] = magnitude.replace('.',',')
    datt['depth'] = depth
    datt['loc'] = loc

    return f"Gempa terkini terjadi tanggal {datt['date'][0]} pada {datt['date'][1][0:5]} Waktu Indonesia Barat. Dengan magnitudo {datt['magnitude']} skala richter. Di kedalaman {datt['depth']}. {datt['loc']}"

def respond(voice_data):
    global bangun
    if bangun:
        if there_exists(['hai', 'hello', 'halo']) and not there_exists(['robot bangun']):
            
            
            greetings = f"hai, bagaimana aku bisa membantu " + username

            speak(greetings)
        
        elif there_exists(["saya baik baik saja", "aku baik baik saja", "saya baik-baik saja"]):
            
            speak("Baguslah kalau begitu")
        
        elif there_exists(["bisakah anda membantu saya", "bisakah kamu membantu saya", "bisakah kamu menolong saya", "bisakah anda menolong saya", "bantu saya", "tolong saya"]):
            
            speak(f"Tentu saja aku bisa menolongmu")

        elif there_exists(["jam berapa sekarang", "katakan jam berapa sekarang", "sekarang jam berapa"]):
            
            time = ctime().split(" ")[3].split(":")[0:2]
            if time[0] == "00":
                hours = '12'
            else:
                hours = time[0]
            minutes = time[1]
            time = f"Sekarang jam {hours} {minutes}"
            speak(time)

        elif there_exists(['ucapkan']):
            word = voice_data.split("ucapkan")[-1]
            if word.find("selamat hari raya nyepi") != -1:
                speak(word + "tahun saka 1945, semoga bahagia")
            elif word.find("selamat ulang tahun untuk kota singaraja") != -1:
                speak(word + " yang ke 419, kuat dan bangkit bersama")
            else:
                speak(word)
            
        elif there_exists(["putar lagu"]):
            search_term = voice_data.split("putar lagu")[-1]
            if search_term != '':
                url = f"https://www.youtube.com/results?search_query={search_term}"
                webbrowser.get().open(url)
                
                speak(f'Ini adalah apa yang aku dapat untuk {search_term} di youtube, mengklik....')
                try:
                    pyautogui.moveTo(650, 350, duration=1)
                    pyautogui.leftClick()
                except pyautogui.FailSafeException:
                    pass

        elif there_exists(["keluar", "selamat tinggal", "matikan sistem", "matikan system", "sampai jumpa"]):
            speak("mematikan sistem...")
            
            try:
                port.write(b'#') #type: ignore
            except:
                pass
            bangun = False

        else:
            answer_question(voice_data)

    elif there_exists(['robot bangun', 'bangun', 'hai robot bangun', 'hai robot aktifkan']):
        bangun = True
        try:
            port.write(b'%') # type: ignore
        except:
            pass
        speak('Selamat Datang ' + username)




wiki.set_lang('id')
try:
    os.remove('ttstmp.mp3')
except:
    pass

API_key = "78c067d5244c3b1392a1de0288f15207"
 

base_url = "http://api.openweathermap.org/data/2.5/weather?"
 

city_id = "Singaraja"

Final_url = f"{base_url}appid={API_key}&q={city_id}&lang=id"
username = "teman"
myname = "D D Bot"
ver = "2"
comport = input('Masukkan Nama Port Dari Robot: ')
port = None

try:
    port = serial.Serial(port=comport, baudrate=9600)
    
    print("Badan Robot, Terhubung")
except:
    print("Tidak Bisa Terhubung Ke Badan Robot, Sebaiknya hubungkan untuk pengalaman yang lebih baik")

listener = sr.Recognizer()




r = sr.Recognizer()


while (1):
    voice_data = record_audio()
    respond(voice_data)