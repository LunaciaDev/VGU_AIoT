import sys
from Adafruit_IO import MQTTClient
import random as r
import time
import aitest

AIO_USERNAME = "student_104"
temp = open("key")
AIO_KEY = temp.read()
temp.close()

def connected(client):
    print("Successfully connected")
    client.subscribe("button1")
    client.subscribe("button2")

def subscribe(client , userdata , mid , granted_qos):
    print("Successfully subscribed")

def disconnected(client):
    print("Disconecting...")
    sys.exit (1)

def message(client , feed_id , payload):
    print(f"Received payload from {feed_id}: {payload}")

client = MQTTClient(AIO_USERNAME , AIO_KEY)

client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

client.connect()
client.loop_background()

while True:
    client.publish("sensor1", r.randint(0, 80))
    time.sleep(5)
    client.publish("sensor2", r.randint(0, 100))
    time.sleep(5)
    client.publish("sensor3", r.randint(0, 10))
    time.sleep(5)
    client.publish("ai", aitest.imageDetector()) #Homework: Output AI data to Adafruit
    time.sleep(15)