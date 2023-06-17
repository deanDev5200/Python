import mouse
from time import sleep

sleep(1)
while True:
    for i in range(0, 10):
        mouse.click('left')
    sleep(0.01)