import socket

HOST = "192.168.43.72"
PORT = 7718

sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sc.settimeout(0)
try:
    sc.connect(('10.254.254.254', 1))
    HOST = sc.getsockname()[0]
except Exception:
    IP = '127.0.0.1:' + str(PORT)
finally:
    sc.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
