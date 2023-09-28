test = False
import glob, speech_recognition as sr, sys, random, requests, webbrowser, json, pyautogui, AppOpener, serial, wikipedia as wiki, os
from lxml import etree
from gtts import gTTS
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from pydub import AudioSegment
from pydub.playback import play
from time import sleep
from datetime import datetime
from time import ctime
from paho.mqtt import client as mqtt_client
start_time = '00:00:00'
broker = 'broker.emqx.io'
mqttport = 1883
topic = 'deanpop/lampujarakjauh/01'
topic2 = 'DEAN_DEV/aplikasiSmartFarm/0/set'
client_id = f'python-mqtt-{random.randint(1000, 9999)}'
temperature = ''
humidity = ''
pump_status = ''
#-----------------------------------------------------#
bangun = False
x = open('Testing/DDbot/const.json').read()
x = json.loads(x)
wiki.set_lang('id')
question_words = x['question_words']
API_key = x['weather_key']
city_id = x['city']
username = x['username']
myname = x['myname']
ver = x['version']
r = sr.Recognizer()
mic = sr.Microphone()

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
                if stemmed.find('kamu tahu sekarang adalah ulang tahun pak jokowi') != -1:
                    respond = f"oh ya, sekarang adalah ulang tahun bapak presiden joko widodo yang ke-{datetime.now().year-1961}, untung kamu mengingatkan."
            elif tokenized[0] == question_words[2]:
                if tokenized[1] == 'namamu':
                    respond = f'Nama saya adalah {myname} versi {ver}'
                elif tokenized[1] == 'kamu':
                    respond = f'Namaku {myname} versi {ver}. Aku dibuat oleh seorang anak bernama Dean Putra, Sekarang umurnya {datetime.now().year-2010} Tahun. Dia sangat suka programming, Dia berasal dari Buleleng, Bali'
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
                elif tokenized[1] == 'umur' and tokenized[2] == 'sekarang':
                    respond = f'Umurku sejak aku pertama kali dibuat adalah {datetime.now().year-2022} tahun'
                elif tokenized[1] == 'umur' and tokenized[2] == 'dean':
                    respond = f'Umur dean sekarang adalah {datetime.now().year-2010} tahun'

        print(respond)
        speak(respond)

def record_audio(recognizer:sr.Recognizer, microphone:sr.Microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)


    response = {
        'success': True,
        'error': None,
        'transcription': None
    }

    try:
        response['transcription'] = recognizer.recognize_google(audio, None, 'id-ID')
    except sr.RequestError:

        response['success'] = False
        response['error'] = 'API unavailable'
    except sr.UnknownValueError:

        response['error'] = 'Unable to recognize speech'

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
    global start_time, bangun, temperature
    if bangun:
        if there_exists(['hai', 'hello', 'halo']) and not there_exists(['robot bangun']):
            r = random.randint(0, 2)
            h = datetime.now().hour
            if r == 0:
                speak('Halo ' + username)
            elif r == 1:
                speak('Hai ' + username)
            elif r == 2:
                if h > 18:
                    speak('Selamat Malam ' + username)
                elif h > 14:
                    speak('Selamat Sore ' + username)
                elif h > 9:
                    speak('Selamat Siang ' + username)
                elif h > 5:
                    speak('Selamat Pagi ' + username)
                else:
                    speak('Selamat Malam ' + username)
            t1 = datetime.strptime(start_time, '%H:%M:%S')
            t2 = datetime.strptime(ctime().split(' ')[3], '%H:%M:%S')
            delta = t2 - t1
            if delta.seconds >= 420:
                speak('Kenapa kamu baru menyapaku, aku kangen')

        elif there_exists(['aku baik saja', 'aku baik-baik saja', 'saya baik-baik saja']):
            
            r = random.randint(0, 3)
            if r == 0:
                speak('Baguslah kalau begitu')
            elif r == 1:
                speak('Baguslah')
            elif r == 2:
                speak('Aku senang mendengarnya')
            elif r == 3:
                speak('Aku senang sekali mendengarnya')

        elif there_exists(['bisakah anda membantu saya', 'bisakah kamu membantu saya', 'bisakah kamu menolong saya', 'bisakah anda menolong saya', 'bantu saya', 'tolong saya']):

            speak(f'Tentu saja aku bisa menolongmu')

        elif there_exists(['jam berapa sekarang', 'katakan jam berapa sekarang', 'sekarang jam berapa']):
            hours = datetime.now().hour
            minutes = datetime.now().minute
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

        elif there_exists(['putar lagu']):
            search_term = voice_data.lower().split('putar lagu ')[1]
            if search_term != '':

                try:
                    speak(f'baiklah, memutar lagu {search_term}')
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

        elif there_exists(['hadiahnya mana', 'mana hadiahnya']):
            speak(f'baiklah {username}')
            webbrowser.get().open('https://youtu.be/NCzdcy4lnXk?t=24')
            speak('Ini hadiahnya')

        elif there_exists(['buka aplikasi']):
            app = voice_data.lower().split('buka aplikasi')[-1].replace(' ', '')
            speak(f'membuka {app}')
            AppOpener.open(app, match_closest=True)

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

            try:
                port.write(b'#') #type: ignore
            except:
                pass
            bangun = False

        else:
            answer_question(voice_data)

    elif there_exists(['robot bangun', 'hai robot bangun', 'hai robot aktifkan']):
        start_time = ctime().split(' ')[3]
        bangun = True
        try:
            port.write(b'%') # type: ignore
        except:
            pass
        speak('Halo' + username)

def serial_ports():
    ''' Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    '''
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal '/dev/tty'
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


print('Port COM yang tersedia:')
for port in serial_ports():
    print('-', port)
try:
    comport = 'COM5'
except:
    comport = input('Masukkan Nama Port Dari Robot: ')

try:
    mqttclient = connect_mqtt()
    subscribe(mqttclient, 'DEAN_DEV/aplikasiSmartFarm/0/')
    mqttclient.loop_start()
except:
    mqttclient = None
port = None

try:
    port = serial.Serial(port=comport, baudrate=9600)

    print('Badan Robot, Terhubung')
except:
    print('Tidak Bisa Terhubung Ke Badan Robot, Sebaiknya hubungkan untuk pengalaman yang lebih baik')

while (1):
    try:
        if test == False:
            res = record_audio(r, mic)
        else:
            res = {
                'success': True,
                'error': None,
                'transcription': input('Enter: ')
            }

        if res['error'] == None and res['transcription'] != None:
            respond(res['transcription'])
        else:
            print(res['error'])
    except:
        pass
