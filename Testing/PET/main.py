import requests, qrcode, cv2, socket, random, threading, serial, time
from ultralytics import YOLO
HOST = "127.0.0.1"
PORT = 60000 + random.randrange(1, 5534)
data = ''
lastTime = 0
spam = False
lastDetect = []
_un = ""
_pw = ""
c = 0
done = False
model = YOLO("yolov8m.pt")
ser = serial.Serial('COM6', 9600)
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
        global HOST, done
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0] + ':' + str(PORT)
            HOST = IP.split(':')[0]
        except Exception:
            IP = '127.0.0.1:' + str(PORT)
        finally:
            s.close()
        IP = IP.replace('1', 'q')
        IP = IP.replace('2', 'a')
        IP = IP.replace('3', 'z')
        IP = IP.replace('4', 'e')
        IP = IP.replace('5', 'd')
        IP = IP.replace('6', 'c')
        IP = IP.replace('7', 'w')
        IP = IP.replace('8', 's')
        IP = IP.replace('9', 'x')
        IP = IP.replace('0', 'r')
        IP = IP.replace('.', 'f')
        IP = IP.replace(':', 'v')
        qr = qrcode.QRCode(version = 1,
                   box_size = 10,
                   border = 5)
 
        qr.add_data(IP)
        
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

t = threading.Thread(target=show_ip_qr)
t.start()

while not done:
    pass

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    print(HOST, PORT)
    soc.bind((HOST, PORT))
    while True:
        soc.listen()
        conn, addr = soc.accept()
        with conn:
            dataT = conn.recv(1024)
            lastTime = time.time()
            ser.write(b'1')
            time.sleep(0.05)
            ser.write(b'4')
            data = dataT.decode()
            data = data.replace(" ", "")
            data = data.split("\r\n")
            _un = data[1].split(':')[1]
            _pw = data[2].split(':')[1]
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                detections = []
                results = model(source=frame)
                ser.write(b'1')
                time.sleep(0.05)

                for detection in results[0].boxes:
                    class_index = detection.cls
                    detections.append(int(class_index[0]))

                if detections == [39] or detections == [40]:
                    if lastDetect == detections:
                        c = c + 1
                    elif c > 0:
                        c = c - 1
                    
                    try:
                        ser.write(b'2')
                        time.sleep(0.05)
                        ser.write(b'3')
                        time.sleep(0.05)
                        if c > 1:
                            stat = decrease(un=_un, pw=_pw)
                        else:
                            stat = increase(un=_un, pw=_pw)
                        time.sleep(0.05)
                        if stat:
                            conn.sendall(stat.encode())
                        else:
                            conn.sendall(b'n')
                        time.sleep(2)
                        ser.write(b'1')
                        time.sleep(0.05)
                        ser.write(b'4')
                        time.sleep(0.05)
                    except:
                        pass
                    lastTime = time.time()
                if time.time() > lastTime+30:
                    break
                lastDetect = detections
            conn.close()
            ser.write(b'3')
            time.sleep(0.05)
            ser.write(b'1')
            time.sleep(0.05)
            c = 0
