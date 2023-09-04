import requests, socket, qrcode, cv2, socket, random, threading

HOST = "127.0.0.1"
PORT = 60000 + random.randrange(1, 5534)

def show_ip_qr():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0] + ':' + str(PORT)
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
        while True:
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

t = threading.Thread(target=show_ip_qr)
t.start()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            print(data.decode())
            break
myobj = {'un': '', 'pw': 'deanpop5200'}

x = requests.post('http://localhost/increase.php', data=myobj)

if x.text != "Wrong" and x.text != "Invalid" and x.text != "Error":
    if x.text == "Success":
        print("Operation Succeded")
        y = requests.post('http://localhost', data=myobj)
        try:
            print("Points:" + int(y.text))
        except:
            print(y.text)
    else:
        try:
            print("Points:" + int(x.text))
        except:
            print(x.text)
else:
    print("Operation Not Completed:\n" + x.text)