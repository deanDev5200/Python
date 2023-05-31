import pyautogui
import webbrowser
from time import sleep

search = "membuat nasi goreng"
webbrowser.get().open("https://id.wikihow.com/Halaman-Utama")
while pyautogui.pixel(983, 127) != (147, 184, 116):
    pass
sleep(0.2)
pyautogui.click(783, 133)
pyautogui.write(search, 0.05)
pyautogui.click(912, 136)
while pyautogui.pixel(710, 216) == (243, 243, 243) or pyautogui.pixel(710, 216) == (230, 238, 224):
    pass
sleep(0.7)
pyautogui.click(710, 216)
# x87 y117