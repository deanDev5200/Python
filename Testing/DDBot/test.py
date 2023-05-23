import serial
import pyautogui
sr = serial.Serial("com5")

while True:
    if sr.read() == b'1':
        pyautogui.rightClick(1265, 515)
