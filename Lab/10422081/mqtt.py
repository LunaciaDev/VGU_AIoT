import sys
from Adafruit_IO import MQTTClient
import random as r
import time
#import aitest
import sensor
import requests

AIO_USERNAME = "student_104"
EQUATION_API = "https://io.adafruit.com/api/v2/student_104/feeds/equation"
temp = open("key")
AIO_KEY = temp.read()
temp.close()
global_equation = ""

def connected(client):
    print("Successfully connected")
    client.subscribe("button1")
    client.subscribe("button2")
    client.subscribe("equation")

def subscribe(client , userdata , mid , granted_qos):
    print("Successfully subscribed")

def disconnected(client):
    print("Disconecting...")
    sys.exit (1)

def message(client , feed_id , payload):
    global global_equation
    print(f"Received payload from \"{feed_id}\": {payload}")

    if (feed_id == "equation"):
        global_equation = payload
        return

    if (feed_id == "button1"):
        if payload == "ON":
            print("Turning the light on...")
            sensor.sendCommand("2")
            return
        
        if payload == "OFF":
            print("Turning the light off...")
            sensor.sendCommand("3")
            return

def init_global_equation():
    global global_equation
    headers = {}
    temp = requests.get(url = EQUATION_API, headers = headers, verify = False)
    temp = temp.json()
    global_equation = temp["last_value"]
    print(f"Latest equation value: {global_equation}")

def evaluate(sensor1, sensor2, sensor3):
    result = eval(global_equation)
    print(f"Evaluation result of {global_equation}: {result}")
    return result

def requestData(command):
    sensor.sendCommand(command)
    time.sleep(3)
    returnData = sensor.readSerial()
    if returnData == []: return 0
    return returnData[2]

client = MQTTClient(AIO_USERNAME , AIO_KEY)

client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

init_global_equation()
client.connect()
client.loop_background()

while True:
    sensorOneValue = float(requestData("0"))
    sensorTwoValue = float(requestData("1"))
    sensorThreeValue = r.randint(0, 10)
    client.publish("sensor1", sensorOneValue)
    time.sleep(4)
    client.publish("sensor2", sensorTwoValue)
    time.sleep(4)
    client.publish("sensor3", sensorThreeValue)
    time.sleep(4)
    #client.publish("ai", aitest.imageDetector()) #Homework: Output AI data to Adafruit
    #time.sleep(4)
    client.publish("testfeed", evaluate(sensorOneValue, sensorTwoValue, sensorThreeValue))
    time.sleep(10)