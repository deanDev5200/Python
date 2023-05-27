test = False
import pyautogui
import speech_recognition as sr
from gtts import gTTS
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import requests
import webbrowser
import json
from pydub import AudioSegment
from pydub.playback import play
import time
import AppOpener
import datetime
from time import ctime
import serial
import wikipedia as wiki
import requests
import os
from nltk.tokenize import word_tokenize
question_words = ["apa", "apakah", "siapa", "bagaimana", "kenapa", "kapan", "dimana", 
              "mengapa", "pernahkah", 
             "mana", "bisakah", "maukah", 
             "haruskah", "punyakah", "berapa", "berapakah"]
bangun = False
x = open('const.json').read()
x = json.loads(x)
wiki.set_lang('id')
API_key = x["weather_key"]
city_id = x["city"]
username = x["username"]
myname = x["myname"]
ver = x["version"]
r = sr.Recognizer()
mic = sr.Microphone()

def find_wiki(q:str):
    p = "Aku tidak menemukan apapun"

    try:
        p = wiki.page(q)
        m = p.content.split("\n")[0]
        p = m.split(m.split("(")[1].split(")")[0])
        p = p[0] + p[1]
        return p
    except:
        return p

def stem(text:str):
    fact = StemmerFactory()
    stemmer = fact.create_stemmer()
    return stemmer.stem(text)

def answer_question(question:str):
    respond = "Saya tidak mengerti"
    question = question.lower()
    stemmed = stem(question)
    print(stemmed)
    tokenized = word_tokenize(question)
    if question != "":
        if any(x in tokenized[0] for x in question_words):
            if tokenized[0] == question_words[0]:
                if stemmed.find("adalah cerdas buat") != -1:
                    respond = "Benar sekali!"
                elif stemmed.find("kabar") != -1:
                    mon = ctime().split(" ")[1]
                    day = ctime().split(" ")[2]
                    if mon == "May" and day == "12":
                        respond = f"Aku sangat baik terimakasih telah bertanya, Oh ya {username} hari ini ulang tahunmu. Selamat ulang tahun ya"
                    else:
                        respond = f"Aku sangat baik terimakasih telah bertanya, bagaimana denganmu {username}"
                elif stemmed.find("hobi") != -1:
                    respond = f"Aku hanyalah kecerdasan buatan jadi aku tidak punya hobi"
            elif tokenized[0] == question_words[1]:
                if stemmed.find("adalah cerdas buat") != -1:
                    respond = "Benar sekali!"
                elif stemmed.find("kamu cerdas buat") != -1:
                    respond = "Benar sekali!"
            elif tokenized[0] == question_words[2]:
                print(tokenized[1])
                if tokenized[1] == "namamu":
                    respond = f"Nama saya adalah " + myname + " versi " + ver + "seenggol dong!"
                elif tokenized[1] == "kamu":
                    d = datetime.datetime.now().year
                    respond = f"Namaku " + myname + " versi " + ver + ". Aku dibuat oleh seorang anak bernama Dean Putra, Sekarang umurnya " + str(d-2010) + "Tahun. Dia sangat suka programming, Dia berasal dari Buleleng, Bali"
                else:
                    search_term = question.split(tokenized[0])[-1]
                    respond = find_wiki(search_term)
            elif tokenized[0] == question_words[3]:
                if stemmed.find("gempa kini") != -1:
                    respond = earthquake()
                if tokenized[1] == "cuaca":
                    weather_data = requests.get(Final_url).json()
                    temp = weather_data['main']['temp']
            
                    wind_speed = weather_data['wind']['speed']
            
                    description = weather_data['weather'][0]['description']

                    respond = f"Cuaca: {description}, Suhu: {str(temp-273.15)[0:5].replace('.',',')} °C, Kecepatan Angin: {str(wind_speed).replace('.',',')} km/h"
        print(respond)
        speak(respond)

def record_audio(recognizer:sr.Recognizer, microphone:sr.Microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio, None, "id-ID")
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

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
        if term in res["transcription"].lower():
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
    print(voice_data)
    global bangun
    if bangun:
        if there_exists(['hai', 'hello', 'halo']) and not there_exists(['robot bangun']):
            
            
            greetings = f"hai, bagaimana aku bisa membantu " + username

            speak(greetings)
        
        elif there_exists(["aku baik saja", "aku baik-baik saja", "saya baik-baik saja"]):
            
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
        
        elif there_exists(["hadiahnya mana", "mana hadiahnya"]):
            speak(f"baiklah {username}")
            webbrowser.get().open("https://youtu.be/NCzdcy4lnXk?t=24")
            speak("Ini hadiahnya")

        elif there_exists(["buka aplikasi"]):
            app = voice_data.split("Buka aplikasi")[-1].replace(' ', '')
            speak(f"membuka {app}")
            AppOpener.open(app, match_closest=True)

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


try:
    os.remove('ttstmp.mp3')
except:
    pass

Final_url = f"http://api.openweathermap.org/data/2.5/weather?appid={API_key}&q={city_id}&lang=id"

comport = input('Masukkan Nama Port Dari Robot: ')
port = None

try:
    port = serial.Serial(port=comport, baudrate=9600)
    
    print("Badan Robot, Terhubung")
except:
    print("Tidak Bisa Terhubung Ke Badan Robot, Sebaiknya hubungkan untuk pengalaman yang lebih baik")

while (1):
    if test == False:
        res = record_audio(r, mic)
    else:
        res = {
            "success": True,
            "error": None,
            "transcription": input("Enter: ")
        }
    
    if res["error"] == None and res["transcription"] != None:
        respond(res["transcription"])
    else:
        print(res["error"])
