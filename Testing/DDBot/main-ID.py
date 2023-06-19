test = False
import random
import pyautogui
import sys
import glob
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
from time import sleep
import AppOpener
from datetime import datetime
from time import ctime
import serial
import wikipedia as wiki
import os
from paho.mqtt import client as mqtt_client

start_time = "00:00:00"
broker = 'broker.mqttdashboard.com'
mqttport = 1883
topic = "deanpop/lampujarakjauh/01"
client_id = f'python-mqtt-{random.randint(1000, 9999)}'
temperature = ""
def connect_mqtt():
    client = mqtt_client.Client(client_id)

    client.connect(broker, mqttport)
    return client

def subscribe(client: mqtt_client.Client, sTopic: str):
    if sTopic == "DEAN_DEV/aplikasiSmartFarm/0/temp":
        def on_message(client, userdata, msg):
            global temperature
            temperature = msg.payload.decode()
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    else:
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(sTopic)
    client.on_message = on_message

def publish(client, state:int):
        if client != None:
            msg = f"{state}"
            client.publish(topic, msg)

bangun = False
x = open('Testing/DDbot/const.json').read()
x = json.loads(x)
wiki.set_lang('id')
question_words = x["question_words"]
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
    respond = ""
    question = question.lower()
    stemmed = stem(question)
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
                elif question.lower().split('apa ')[1] == "tema bali digifest":
                    respond = "Enabling Bali as Digital Creative Paradise"
                elif question.lower().split('apa ')[1] == "tujuan bali digifest":
                    respond = "Mengakselerasi transformasi Digital Kerthi Bali untuk mendukung terwujudnya visi Nangun Sat Kerthi Loka Bali"
                elif tokenized[1] == "itu" and question.lower().split('apa itu ')[1] == 'bali digifest':
                    respond = "Bali Digifest sedang membangun kolaborasi dengan para pemangku kepentingan yang menjadi bagian dari perkembangan ekosistem digital Bali, sebagai upaya untuk mempercepat realisasi visi Nangun Sat Kerthi Loka Bali melalui pola pengembangan universal yang direncanakan menuju era baru Bali.\nFestival Digital Bali bertujuan untuk Mengakselerasi transformasi Digital Kerthi Bali untuk mendukung terwujudnya visi Nangun Sat Kerthi Loka Bali"
            elif tokenized[0] == question_words[1]:
                if stemmed.find("adalah cerdas buat") != -1:
                    respond = "Benar sekali!"
                elif stemmed.find("kamu cerdas buat") != -1:
                    respond = "Benar sekali!"
            elif tokenized[0] == question_words[2]:
                if tokenized[1] == "namamu":
                    respond = f"Nama saya adalah {myname} versi {ver} seenggol dong!"
                elif tokenized[1] == "kamu":
                    d = datetime.now().year
                    respond = f"Namaku {myname} versi {ver}. Aku dibuat oleh seorang anak bernama Dean Putra, Sekarang umurnya {str(d-2010)} Tahun. Dia sangat suka programming, Dia berasal dari Buleleng, Bali"
                else:
                    search_term = question.split('siapa ')[1]
                    print(search_term)
                    respond = find_wiki(search_term)
            elif tokenized[0] == question_words[3]:
                if stemmed.find("gempa kini") != -1:
                    respond = earthquake()
                if tokenized[1] == "cuaca":
                    if tokenized[2] != "di":
                        weather_data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?appid={API_key}&q={city_id}&lang=id").json()
                        city = True
                    else:
                        try:
                            city = question.split("bagaimana cuaca di ")[1]
                        except:
                            city = city_id
                        weather_data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?appid={API_key}&q={city}&lang=id").json()
                    temp = weather_data['main']['temp']
            
                    wind_speed = weather_data['wind']['speed']
            
                    description = weather_data['weather'][0]['description']
                    if city == True:
                        respond = f"Cuaca di {city_id}: {description}, Suhu: {str(temp-273.15)[0:5].replace('.',',')} °C, Kecepatan Angin: {str(wind_speed).replace('.',',')} km/h"
                    else:
                        respond = f"Cuaca di {city}: {description}, Suhu: {str(temp-273.15)[0:5].replace('.',',')} °C, Kecepatan Angin: {str(wind_speed).replace('.',',')} km/h"
                elif tokenized[1] == "cara":
                    search = question.split("bagaimana ")[1]
                    print(search)
                    try:
                        webbrowser.get().open("https://id.wikihow.com/Halaman-Utama")
                        while pyautogui.pixel(983, 127) != (147, 184, 116):
                            pass
                        sleep(0.2)
                        pyautogui.click(783, 133)
                        pyautogui.write(search, 0.05)
                        pyautogui.click(912, 136)
                        while pyautogui.pixel(710, 216) == (243, 243, 243) or pyautogui.pixel(710, 216) == (230, 238, 224):
                            pass
                        sleep(0.7)
                        pyautogui.click(710, 216)
                        respond = f"Ini dia {search}"
                    except:
                        pass
            elif tokenized[0] == question_words[14]:
                if tokenized[1] == "suhu":
                    respond = temperature

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

    if test == False:
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
    else:
        print(audio_string)

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
    global start_time
    global bangun
    if bangun:
        if there_exists(['hai', 'hello', 'halo']) and not there_exists(['robot bangun']):
            speak('Selamat datang di acara bakti sosial Persatuan Perantau Kelampuak')
            t1 = datetime.strptime(start_time, "%H:%M:%S")

            t2 = datetime.strptime(ctime().split(" ")[3], "%H:%M:%S")

            delta = t2 - t1
            if delta.seconds >= 420:
                speak('Kenapa kamu baru menyapaku, aku kangen')
        
        elif there_exists(["aku baik saja", "aku baik-baik saja", "saya baik-baik saja"]):
            
            speak("Baguslah kalau begitu")
        
        elif there_exists(["bisakah anda membantu saya", "bisakah kamu membantu saya", "bisakah kamu menolong saya", "bisakah anda menolong saya", "bantu saya", "tolong saya"]):

            speak(f"Tentu saja aku bisa menolongmu")

        elif there_exists(["informasi gempa terkini", "info gempa terkini"]):

            speak(earthquake())

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
            search_term = voice_data.lower().split("putar lagu ")[1]
            if search_term != '':
                
                try:
                    speak(f"baiklah, memutar lagu {search_term}")
                    AppOpener.open('spotify')
                    while pyautogui.pixel(124, 150) != (179, 179, 179):
                        pass
                    sleep(0.5)
                    pyautogui.click(124,150)
                    sleep(0.5)
                    pyautogui.write(search_term, 0.05)
                    while pyautogui.pixel(1095, 312) == (18, 18, 18):
                        pass
                    pyautogui.moveTo(1095, 312)
                    sleep(0.6)
                    pyautogui.click(1095, 312)
                except:
                    pass

        elif there_exists(["hadiahnya mana", "mana hadiahnya"]):
            speak(f"baiklah {username}")
            webbrowser.get().open("https://youtu.be/NCzdcy4lnXk?t=24")
            speak("Ini hadiahnya")

        elif there_exists(["buka aplikasi"]):
            app = voice_data.lower().split("buka aplikasi")[-1].replace(' ', '')
            speak(f"membuka {app}")
            AppOpener.open(app, match_closest=True)

        elif there_exists(["hidupkan lampu"]):
            speak("menghidupkan lampu")
            publish(mqttclient, 1)

        elif there_exists(["matikan lampu"]):
            speak("mematikan lampu")
            publish(mqttclient, 0)
            
        elif there_exists(["kamu bodoh"]):
            speak("kamu tidak boleh bicara seperti itu, itu tidak baik")

        elif there_exists(["keluar", "selamat tinggal", "matikan sistem", "matikan system", "sampai jumpa"]):
            speak("mematikan sistem...")
            
            try:
                port.write(b'#') #type: ignore
            except:
                pass
            bangun = False

        else:
            answer_question(voice_data)

    elif there_exists(['robot bangun', 'hai robot bangun', 'hai robot aktifkan']):
        start_time = ctime().split(" ")[3]
        bangun = True
        try:
            port.write(b'%') # type: ignore
        except:
            pass
        speak('Selamat datang di acara bakti sosial Persatuan Perantau Kelampuak')

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

try:
    os.remove('ttstmp.mp3')
except:
    pass

print('Port COM yang tersedia:', serial_ports())
comport = input('Masukkan Nama Port Dari Robot: ')
#comport = 'COM6'
try:
    mqttclient = connect_mqtt()
    subscribe(mqttclient, "DEAN_DEV/aplikasiSmartFarm/0/temp")
    subscribe(mqttclient, "DEAN_DEV/aplikasiSmartFarm/0/hum")
    subscribe(mqttclient, "DEAN_DEV/aplikasiSmartFarm/0/pump")
    mqttclient.loop_start()
except:
    mqttclient = None
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
        try:
            respond(res["transcription"])
        except:
            pass
    else:
        print(res["error"])
