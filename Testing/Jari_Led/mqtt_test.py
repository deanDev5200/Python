import random
from paho.mqtt import client as mqtt_client
import time

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

client = connect_mqtt()
client.loop_start()

i = 0
while i < 15:
    client.publish(topic, "0")
    time.sleep(0.05)
    client.publish(topic, "1")
    time.sleep(0.05)
    i += 1

client.disconnect()