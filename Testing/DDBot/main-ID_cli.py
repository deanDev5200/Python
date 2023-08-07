test = False
talkFlag = False

from pydub import AudioSegment
import sounddevice as sd
import soundfile as sf
import random
from lxml import etree
import speech_recognition as sr
from gtts import gTTS
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import requests
import json
from time import ctime, sleep
from datetime import datetime
import wikipedia as wiki
import os
from paho.mqtt import client as mqtt_client
from adafruit_servokit import ServoKit
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
import threading
sd.default.device = 2
sd.default.samplerate = 48000

broker = 'broker.emqx.io'
mqttport = 1883
topic = 'deanpop/lampujarakjauh/01'
topic2 = 'DEAN_DEV/aplikasiSmartFarm/0/set'
client_id = f'python-mqtt-{random.randint(1000, 9999)}'
temperature = ''
humidity = ''
pump_status = ''
def connect_mqtt():
    client = mqtt_client.Client(client_id)

    client.connect(broker, mqttport)
    return client

def subscribe(client: mqtt_client.Client, sTopic: str):
    def on_message(client, userdata, msg):
        global temperature
        global humidity
        global pump_status
        data = json.loads(msg.payload.decode())
        temperature = '{:.2f}'.format(float(data['Temperature'])).replace('.', ',')

        humidity = '{:.2f}'.format(float(data['Humidity'])).replace('.', ',')
        pump_status = data['WaterPump']

    client.subscribe(sTopic)
    client.on_message = on_message

def publish(client, state:int, farm:bool):
        if client != None:
            msg = f'{state}'
            if farm:
                client.publish(topic2, msg)
            else:
                client.publish(topic, msg)

bangun = False
x = open('const.json').read()
x = json.loads(x)
wiki.set_lang('id')
question_words = x['question_words']
API_key = x['weather_key']
city_id = x['city']
username = x['username']
myname = x['myname']
ver = x['version']
r = sr.Recognizer()
mic = sr.Microphone(0)


def find_wiki(q:str):
    p = 'Aku tidak menemukan apapun'

    try:
        p = wiki.page(q)
        m = p.content.split('\n')[0]
        p = m.split(m.split('(')[1].split(')')[0])
        p = p[0] + p[1]
        return p
    except:
        return p

def stem(text:str):
    fact = StemmerFactory()
    stemmer = fact.create_stemmer()
    return stemmer.stem(text)

def answer_question(question:str):
    global temperature
    global humidity
    global pump_status
    respond = ''
    question = question.lower()
    stemmed = stem(question)
    tokenized = word_tokenize(question)
    if question != '':
        if stemmed == 'info gempa kini' or stemmed == 'informasi gempa kini':
            respond = earthquake()
        elif any(x in tokenized[0] for x in question_words):
            if tokenized[0] == question_words[0]:
                if stemmed.find('kabar') != -1:
                    mon = ctime().split(' ')[1]
                    day = ctime().split(' ')[2]
                    if mon == 'May' and day == '12':
                        respond = f'Aku sangat baik terimakasih telah bertanya, Oh ya {username} hari ini ulang tahunmu. Selamat ulang tahun ya'
                    else:
                        respond = f'Aku sangat baik terimakasih telah bertanya, bagaimana denganmu {username}'
                elif question.lower().split('apa ')[1] == 'tema bali digifest':
                    pass
                elif question.lower().split('apa ')[1] == 'tujuan bali digifest':
                    pass
                elif tokenized[1] == 'itu' and question.lower().split('apa itu ')[1] == 'bali digifest':
                    pass
            elif tokenized[0] == question_words[1]:
                if stemmed.find('kamu tahu sekarang adalah ulang tahun pak jokowi'):
                    d = datetime.now().year
                    respond = f"oh ya, sekarang adalah ulang tahun bapak presiden joko widodo yang ke-{d-1961}, untung kamu mengingatkan."
            elif tokenized[0] == question_words[2]:
                if tokenized[1] == 'namamu':
                    respond = f'Nama saya adalah {myname} versi {ver} seenggol dong!'
                elif tokenized[1] == 'kamu':
                    d = datetime.now().year
                    respond = f'Namaku {myname} versi {ver}. Aku dibuat oleh seorang anak bernama Dean Putra, Sekarang umurnya {d-2010} Tahun. Dia sangat suka programming, Dia berasal dari Buleleng, Bali'
                elif tokenized[1] == 'calon' and tokenized[2] == 'presiden':
                    URL = "https://poltracking.com/rilis-temuan-survei-nasional-poltracking-indonesia-tendensi-peta-politik-pilpres-2024/"

                    HEADERS = ({'User-Agent':
                                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                                (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
                                'Accept-Language': 'en-US, en;q=0.5'})

                    webpage = requests.get(URL, headers=HEADERS)
                    soup = BeautifulSoup(webpage.content, "html.parser")
                    dom = etree.HTML(str(soup)) # type: ignore
                    respond = dom.xpath('//*[@id="post-29188"]/div/div[3]/div[1]/p[2]/text()[2]')[0]
                else:
                    search_term = question.split('siapa ')[1]
                    print(search_term)
                    respond = find_wiki(search_term)
            elif tokenized[0] == question_words[3]:
                if stemmed.find('gempa kini') != -1:
                    respond = earthquake()
                elif tokenized[1] == 'cuaca':
                    if tokenized[2] != 'di':
                        weather_data = requests.get(f'http://api.openweathermap.org/data/2.5/weather?appid={API_key}&q={city_id}&lang=id').json()
                        city = True
                    else:
                        try:
                            city = question.split('bagaimana cuaca di ')[1]
                        except:
                            city = city_id
                        weather_data = requests.get(f'http://api.openweathermap.org/data/2.5/weather?appid={API_key}&q={city}&lang=id').json()
                    temp = weather_data['main']['temp']

                    wind_speed = weather_data['wind']['speed']

                    description = weather_data['weather'][0]['description']
                    if city == True:
                        respond = f"Cuaca di {city_id}: {description}, Suhu: {str(temp-273.15)[0:5].replace('.',',')} °C, Kecepatan Angin: {str(wind_speed).replace('.',',')} km/h"
                    else:
                        respond = f"Cuaca di {city}: {description}, Suhu: {str(temp-273.15)[0:5].replace('.',',')} °C, Kecepatan Angin: {str(wind_speed).replace('.',',')} km/h"
                elif tokenized[1] == 'status' and tokenized[2] == 'pompa':
                    respond = f'Status pompa smart farm saat ini {pump_status}'
                elif tokenized[1] == 'status' and tokenized[2] == 'smart' and tokenized[3] == 'farm':
                    respond = f'Status smart farm saat ini adalah suhu: {temperature} derajat celcius, kelembaban: {humidity} persen, pompa {pump_status}'
            elif tokenized[0] == question_words[4]:
                print(tokenized[1])
                if tokenized[1] == 'suhu':
                    respond = f'Suhu di smart farm saat ini adalah {temperature} derajat celcius'
                elif tokenized[1] == 'kelembaban':
                    respond = f'Kelembaban di smart farm saat ini adalah {humidity} persen'
        speak(respond)

def record_audio(recognizer:sr.Recognizer, microphone:sr.Microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        'success': True,
        'error': None,
        'transcription': None
    }

    try:
        response['transcription'] = recognizer.recognize_google(audio, None, 'id-ID')
    except sr.RequestError:
        # API was unreachable or unresponsive
        response['success'] = False
        response['error'] = 'API unavailable'
    except sr.UnknownValueError:
        # speech was unintelligible
        response['error'] = 'Unable to recognize speech'

    return response

def speak(audio_string):
    global talkFlag
    try:
        tts = gTTS(text=audio_string, lang='id')
        tts.save('ttstmp.mp3')
        audio = AudioSegment.from_file('ttstmp.mp3')
        conv = audio.set_frame_rate(48000)
        conv.export('ttstmp2.mp3', format='mp3', bitrate='48000')
        talkFlag = True
        d = threading.Thread(target=startTalk, daemon=True)
        data, fs = sf.read('ttstmp2.mp3')
        d.start()
        sd.play(data)
        sd.wait()
        talkFlag = False
        stopTalk()
    except:
        pass

def stopTalk():
    kit.servo[0].angle = 90
    kit.servo[1].angle = 90
    kit.servo[2].angle = 135

def eye():
    nice = random.randrange(0, 2)
    if nice == 0:
        kit.servo[1].angle = 0
    elif nice == 1:
        kit.servo[1].angle = 90
    elif nice == 2:
        kit.servo[1].angle = 180

def startTalk():
    global talkFlag
    count = False
    while talkFlag:
        if count:
            luck = random.random()
            if luck > 0.7:
                eye()
            kit.servo[0].angle = 90
            count = False
        else:
            kit.servo[0].angle = 135
            count = True
        sleep(0.3)

def there_exists(terms):
    for term in terms:
        if term in res['transcription'].lower():
            return True

def earthquake():
    content = 'https://www.bmkg.go.id/'
    req = requests.get(content)
    soup = BeautifulSoup(req.text, 'html.parser')
    date = soup.find('span', {'class': 'waktu'}).string.split(', ') #type: ignore

    nondate = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
    nondate = nondate.findChildren('li') #type: ignore

    magnitude = '0'
    depth = '99 km'
    loc = 'laut'

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
    global temperature
    if bangun:
        if there_exists(['hai', 'hello', 'halo']) and not there_exists(['robot bangun']):
            speak('Selamat datang di channel youtube dean dev, jangan lupa like dan subscribe ya')


        elif there_exists(['aku baik saja', 'aku baik-baik saja', 'saya baik-baik saja']):

            speak('Baguslah kalau begitu')

        elif there_exists(['bisakah anda membantu saya', 'bisakah kamu membantu saya', 'bisakah kamu menolong saya', 'bisakah anda menolong saya', 'bantu saya', 'tolong saya']):

            speak(f'Tentu saja aku bisa menolongmu')

        elif there_exists(['jam berapa sekarang', 'katakan jam berapa sekarang', 'sekarang jam berapa']):
            time = ctime().split(' ')[3].split(':')[0:2]
            if time[0] == '00':
                hours = '12'
            else:
                hours = time[0]
            minutes = time[1]
            time = f'Sekarang jam {hours}.{minutes}'
            speak(time)

        elif there_exists(['ucapkan', 'kalau begitu ucapkan']):
            word = voice_data.split('ucapkan')[-1]
            if word.find('selamat hari raya nyepi') != -1:
                speak(word + 'tahun saka 1945, semoga bahagia')
            if word.find('sesuatu untuk bapak presiden') != -1:
                speak('selamat ulang tahun pak presiden jokowi, semoga panjang umur dan sehat selalu')
            elif word.find('selamat ulang tahun untuk kota singaraja') != -1:
                speak(word + ' yang ke 419, kuat dan bangkit bersama')
            else:
                speak(word)

        elif there_exists(['hidupkan lampu']):
            speak('menghidupkan lampu')
            publish(mqttclient, 1, False)

        elif there_exists(['matikan lampu']):
            speak('mematikan lampu')
            publish(mqttclient, 0, False)

        elif there_exists(['hidupkan pompa']):
            if pump_status == 'Hidup':
                speak('Pompa sudah hidup')
            else:
                speak('menghidupkan pompa air')
                publish(mqttclient, 0, True)

        elif there_exists(['matikan pompa']):
            if pump_status == 'Mati':
                speak('Pompa sudah mati')
            else:
                speak('mematikan pompa air')
                publish(mqttclient, 1, True)

        elif there_exists(['kamu bodoh']):
            speak('kamu tidak boleh bicara seperti itu, itu tidak baik')

        elif there_exists(['keluar', 'selamat tinggal', 'matikan sistem', 'matikan system', 'sampai jumpa']):
            speak('mematikan sistem...')

            bangun = False

        else:
            answer_question(voice_data)

    elif there_exists(['robot bangun', 'hai robot bangun', 'hai robot aktifkan']):
        start_time = ctime().split(' ')[3]
        bangun = True

        speak('Selamat datang di channel youtube dean dev, jangan lupa like dan subscribe ya')

try:
    os.remove('ttstmp.mp3')
except:
    pass

i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50
kit = ServoKit(channels=16)
kit.servo[0].angle = 90
kit.servo[1].angle = 90
kit.servo[2].angle = 135
try:
    mqttclient = connect_mqtt()
    subscribe(mqttclient, 'DEAN_DEV/aplikasiSmartFarm/0/')
    mqttclient.loop_start()
except:
    mqttclient = None

while (1):
	if test == False:
		pca.channels[3].duty_cycle = 0xFFFF
		sleep(0.1)
		pca.channels[3].duty_cycle = 0x0000
		res = record_audio(r, mic)
	else:
		res = {
			'success': True,
			'error': None,
			'transcription': input('Enter: ')
		}

	if res['success'] and res['transcription'] != None:
		pca.channels[3].duty_cycle = 0xFFFF
		sleep(0.1)
		pca.channels[3].duty_cycle = 0x0000
		sleep(0.1)
		pca.channels[3].duty_cycle = 0xFFFF
		sleep(0.1)
		pca.channels[3].duty_cycle = 0x0000
		respond(res['transcription'])
	else:
		pca.channels[3].duty_cycle = 0xFFFF
		sleep(0.25)
		pca.channels[3].duty_cycle = 0x0000
		sleep(0.1)
		print(res['error'])
