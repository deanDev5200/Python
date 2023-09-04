from pynput import mouse
from time import sleep

sleep(5)
ms = mouse.Controller()
def move_smooth(xm, ym, t):
    for i in range(t):
        if i < t/2:
            h = i
        else:
            h = t - i
        ms.move(h*xm, h*ym)
        sleep(1/60)

while True:
    move_smooth(0, 2, 20)
    ms.click(mouse.Button.left)
    sleep(0.3)
    move_smooth(0, -2, 20)
    ms.click(mouse.Button.left)
    sleep(0.3)