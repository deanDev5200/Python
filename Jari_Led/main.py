import random
from cvzone.HandTrackingModule import HandDetector
import cv2
from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "/DEAN_DEV/oiry9yr9y3r180yjegcb2t1g/setLED"
client_id = f'python-paho-mqtt-{random.randint(0, 1000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

cap = cv2.VideoCapture(3)
detector = HandDetector(detectionCon=0.8, maxHands=2)
i = 0
pwmMode = False
client = connect_mqtt()
client.loop_start()
while True:
    success, imag = cap.read()
    hands, img = detector.findHands(imag)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]

        if lmList:
            fingers = detector.fingersUp(hand)
            if fingers == [1,1,1,1,1] and not pwmMode and i != 1:
                client.publish(topic, "1")
                i = 1
            elif fingers == [0,0,0,0,0] and not pwmMode and i != 0:
                client.publish(topic, "0")
                i = 0

    cv2.imshow("Frame", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
client.disconnect()
cap.release()
cv2.destroyAllWindows()