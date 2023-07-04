print("MQTT with Adafruit IO")
import time
import random
import sys
from Adafruit_IO import MQTTClient
import requests

AIO_USERNAME = "Afihu"
AIO_KEY = ""

global_equation = "x1 + x2 + x3"

def init_global_equation():
    global global_equation
    headers = {}
    aio_url = "https://io.adafruit.com/api/v2/Afihu/feeds/sensor.equation"
    x = requests.get(url=aio_url, headers=headers, verify=False)
    data = x.json()
    global_equation = data["last_value"]
    print("Get lastest value:", global_equation)

def modify_value(x1, x2, x3):
    global  global_equation
    print("Equation: ", global_equation)
    result = eval(global_equation)
    return result

def connected(client):
    print("Server connected ...")
    client.subscribe("button1")
    client.subscribe("button2")
    client.subscribe("equation")

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribed!")

def disconnected(client):
    print("Disconnected from the server!")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Received: " + payload)
    if(feed_id == "equation"):
        global  global_equation
        global_equation = payload
        print(global_equation)

client = MQTTClient(AIO_USERNAME , AIO_KEY)

client.on_connect = connected  #callback
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

client.connect()
client.loop_background()
init_global_equation()

while True:
    usage = random.randint(0,100)
    if usage >= 80: 
        time.sleep(20)
        temp = random.randint(70, 90)
        client.publish("sensor.sensor1", temp)
        client.publish("sensor.sensor2", usage)
        clock = random.randint(1400,1805)
        client.publish("sensor.sensor3", clock)
        print('Result:',modify_value(temp, usage, clock ))
        
    elif (usage < 80) and (usage >= 60): 
        time.sleep(15)
        temp = random.randint(40, 68)
        client.publish("sensor.sensor1", temp)
        client.publish("sensor.sensor2", usage)
        clock = random.randint(1000,1400)
        client.publish("sensor.sensor3", clock)
        print('Result:',modify_value(temp, usage, clock ))

    else: 
        time.sleep(10)
        temp = random.randint(30, 40)
        client.publish("sensor.sensor1", temp)
        client.publish("sensor.sensor2", usage)
        clock = random.randint(300,1000)
        client.publish("sensor.sensor3", clock)
        print('Result:',modify_value(temp, usage, clock ))
        
    pass
