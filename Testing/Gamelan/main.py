import serial
import subprocess

ser = serial.Serial("COM6", 115200)

while True:
    i = ser.read()
    if i == b'1':
        subprocess.Popen(["start", "cmd", "/k", "python playmusic.py 1"], shell = True)
        print('1')
    elif i == b'2':
        subprocess.Popen(["start", "cmd", "/k", "python playmusic.py 2"], shell = True)
        print('2')
    elif i == b'3':
        subprocess.Popen(["start", "cmd", "/k", "python playmusic.py 3"], shell = True)
        print('3')
    elif i == b'4':
        subprocess.Popen(["start", "cmd", "/k", "python playmusic.py 4"], shell = True)
        print('4')
    elif i == b'5':
        subprocess.Popen(["start", "cmd", "/k", "python playmusic.py 5"], shell = True)
        print('5')
    elif i == b'6':
        subprocess.Popen(["start", "cmd", "/k", "python playmusic.py 6"], shell = True)
        print('6')
    elif i == b'7':
        subprocess.Popen(["start", "cmd", "/k", "python playmusic.py 7"], shell = True)
        print('7')
    elif i == b'8':
        subprocess.Popen(["start", "cmd", "/k", "python playmusic.py 8"], shell = True)  
        print('8')
    elif i == b'9':
        subprocess.Popen(["start", "cmd", "/k", "python playmusic.py 9"], shell = True)
        print('9')
    elif i == b'10':
        subprocess.Popen(["start", "cmd", "/k", "python playmusic.py 10"], shell = True)
        print('10')
