from pynput.mouse import Controller
from time import sleep

mouse = Controller()
sleep(2)

mouse.scroll(0, -1)