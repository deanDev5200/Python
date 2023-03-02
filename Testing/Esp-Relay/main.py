from PyQt6.QtWidgets import (
      QApplication, QVBoxLayout, QWidget, QLabel, QPushButton
)
from PyQt6.QtCore import Qt
import sys
import requests
import keyboard
 
class Window(QWidget):
    ip = input("Enter Esp IP: ")
    def __init__(self):
        super().__init__()
        self.resize(300, 250)
        self.setWindowTitle("Esp Relay")
 
        layout = QVBoxLayout()
        self.setLayout(layout)
 
        self.label = QLabel("Control Esp01 Relay Module")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.resize(30, 30)
        layout.addWidget(self.label)
 
        button = QPushButton("ON")
        button.clicked.connect(self.on)
        layout.addWidget(button)
 
        button = QPushButton("OFF")
        button.clicked.connect(self.off)
        layout.addWidget(button)
 
    def on(self):
        requests.get('http://' + self.ip + '/set?a=0')
     
    def off(self):
        requests.get('http://' + self.ip + '/set?a=1')
         
show = True
app = QApplication(sys.argv)
window = Window()

print("ok\n\n\nEsp01 Relay Controller\nPress Q To Turn On Relay\nPress W To Turn Off Relay\nPress U To Use UI\nPress E To Exit")
while True:
    if keyboard.is_pressed("q"):
        requests.get('http://' + window.ip + '/set?a=0')
    elif keyboard.is_pressed("w"):
        requests.get('http://' + window.ip + '/set?a=1')
    elif keyboard.is_pressed("u"):
        break
    elif keyboard.is_pressed("e"):
        show = False
        break

if show:
    window.show()
    sys.exit(app.exec())