import requests, qrcode, cv2, random, threading, serial, time
from ultralytics import YOLO
from paho.mqtt import client as mqtt_client
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

broker = 'broker.mqttdashboard.com'
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
data = ''
lastTime = 0
spam = False
lastDetect = []
_un = ""
block = True
dataT = ""
_pw = ""
c = 0
done = False
model = YOLO("yolov8m.pt")
mqttclient = connect_mqtt()
mqttclient.loop_start()
try:
    ser = serial.Serial('COM6', 9600)
except:
    pass
cap = cv2.VideoCapture(2)

def increase(un:str, pw:str):
    myobj = {'un': un, 'pw': pw}

    x = requests.post('http://localhost/increase.php', data=myobj)

    if x.text != "Wrong" and x.text != "Invalid" and x.text != "Error" and x.text.find("<br") == -1:
        if x.text == "Success":
            print("Operation Succeded")
            y = requests.post('http://localhost', data=myobj)
            try:
                print("Points:" + int(y.text))
            except:
                print(y.text)
            return y.text
        else:
            try:
                print("Points:" + int(x.text))
            except:
                print(x.text)
    else:
        print("Operation Not Completed:\n" + x.text)
    return False

def decrease(un:str, pw:str):
    myobj = {'un': un, 'pw': pw}

    x = requests.post('http://localhost/decrease.php', data=myobj)

    if x.text != "Wrong" and x.text != "Invalid" and x.text != "Error" and x.text.find("<br") == -1:
        if x.text == "Success":
            print("Operation Succeded")
            y = requests.post('http://localhost', data=myobj)
            try:
                print("Points:" + int(y.text))
            except:
                print(y.text)
            return y.text
        else:
            try:
                print("Points:" + int(x.text))
            except:
                print(x.text)
    else:
        print("Operation Not Completed:\n" + x.text)
    return False

def show_ip_qr():
        global HOST, done, topic
        id = random.randint(10000, 99999)
        topic = str(id)
        mqttclient.subscribe(topic+'/up')
        mqttclient.on_message = handler
        qr = qrcode.QRCode(version = 1,
                   box_size = 10,
                   border = 5)
 
        qr.add_data(id)
        
        qr.make(fit = True)
        img = qr.make_image(fill_color = 'black',
                            back_color = 'white')
        img.save('Testing/PET/qr.png')
        img = cv2.imread('Testing/PET/qr.png')
        cv2.imshow('QR Code', img)
        done = True
        while True:
            if cv2.waitKey(10) & 0xFF == ord('-'):
                break

def get(un:str, pw:str):
    myobj = {'un': un, 'pw': pw}

    x = requests.post('http://localhost/', data=myobj)

    if x.text != "Wrong" and x.text != "Invalid" and x.text != "Error" and x.text.find("<br") == -1:
        return x.text
    return False

def handler(client, userdata, msg):
    global dataT, block
    data = msg.payload.decode()
    dataT = data
    reply = get(data.split(':')[0], data.split(':')[1])
    if reply:
        mqttclient.publish(topic+'/pts', reply)
        try:
            p = data.split(':')[2]
        except:
            block = False

t = threading.Thread(target=show_ip_qr)
t.start()

while not done:
    pass

while True:
    while block:
        pass
    lastTime = time.time()
    try:
        ser.write(b'1')
        time.sleep(0.05)
        ser.write(b'4')
        time.sleep(0.05)
        ser.write(b'+')
        time.sleep(0.05)
    except:
        pass
    data = dataT
    _un = data.split(':')[0]
    _pw = data.split(':')[1]
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        detections = []
        results = model(source=frame)
        try:
            ser.write(b'1')
            time.sleep(0.05)
        except:
            pass

        for detection in results[0].boxes:
            class_index = detection.cls
            detections.append(int(class_index[0]))

        if detections == [39] or detections == [40]:
            if lastDetect == detections:
                c = c + 1
            elif c > 0:
                c = c - 1
            
            try:
                try:
                    ser.write(b'2')
                    time.sleep(0.05)
                    ser.write(b'3')
                    time.sleep(0.05)
                except:
                    pass
                if c > 1:
                    stat = decrease(un=_un, pw=_pw)
                else:
                    stat = increase(un=_un, pw=_pw)
                mqttclient.publish(topic+'/pts', stat)
                time.sleep(0.05)
                try:
                    time.sleep(2)
                    ser.write(b'1')
                    time.sleep(0.05)
                    ser.write(b'4')
                    time.sleep(0.05)
                except:
                    pass
            except:
                pass
            lastTime = time.time()
        if time.time() > lastTime+24:
            break
        lastDetect = detections
    block = True
    mqttclient.publish(topic+'/pts', 'end')
    try:
        ser.write(b'3')
        time.sleep(0.05)
        ser.write(b'1')
        time.sleep(0.05)
        ser.write(b'-')
        time.sleep(0.05)
    except:
        pass
    c = 0
