import pyautogui
from time import sleep

while True:
    print(pyautogui.position()) # x902 y249
    print(pyautogui.pixel(int(pyautogui.position()[0]), int(pyautogui.position()[1]))) # 147, 184, 116
    #print(pyautogui.pixel(119, 115))
    sleep(0.3)