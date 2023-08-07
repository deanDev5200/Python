import threading
from time import sleep
import random

f = True
def a(string='p'):
    global f
    count = False
    while f:
        
        if count:
            luck = random.random()
            if luck < 0.7:
                print(string, count)
            else:
                print('anjay')
            count = False
        else:
            print(string, count)
            count = True
        sleep(0.3)

d = threading.Thread(target=a, args=('A',), daemon=True)
d.start()
for i in range(10):
    print(i, "second(s)")
    sleep(1)
f = False
sleep(2)
f = True
d = threading.Thread(target=a, args=('B',), daemon=True)
d.start()
for i in range(10):
    print(i, "second(s)")
    sleep(1)
f = False