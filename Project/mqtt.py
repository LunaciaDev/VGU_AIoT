print("MQTT with Adafruit IO")
import time
import random
import sys
from Adafruit_IO import MQTTClient
import requests

AIO_USERNAME = ""
AIO_KEY = ""

##Dummy equation
##global_equation = "    "

# def init_global_equation():
#     global global_equation
#     headers = {}
#     aio_url = ""
#     x = requests.get(url=aio_url, headers=headers, verify=False)
#     data = x.json()
#     global_equation = data["last_value"]
#     print("Get lastest value:", global_equation)

# def modify_value(x1, x2, x3):
#     global  global_equation
#     print("Equation: ", global_equation)
#     result = eval(global_equation)
#     return result

# def message(client , feed_id , payload):
#     print("Received: " + payload)
#     if(feed_id == "equation"):
#         global  global_equation
#         global_equation = payload
#         print(global_equation)
      
def connected(client):
    client.subscribe("lightsensor")
    client.subscribe("moistsensor")
    client.subscribe("on/off")
    client.subscribe("rainsensor")
    client.subscribe("reservoir")
    client.subscribe("tempsensor")
    client.subscribe("wateramount")
    print("Server connected ...")

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribed!")

def disconnected(client):
    print("Disconnected from the server!")
    sys.exit (1)

client = MQTTClient(AIO_USERNAME , AIO_KEY)

client.on_connect = connected  #callback
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

client.connect()
client.loop_background()

while True:
    reservoir = 100
    # Whether it's day or night/ raining or not.
    sun = random.randint(0,1) # Day (5am - 7pm)/Night (7pm - 5am).
    rain = random.randint(0,1) # Rain
    client.publish("lightsensor", sun)
    client.publish("rainsensor", rain)

    # Daytime  
    if sun == 1:  
        temp = random.randint(30, 35)
    # Nighttime
    else:
        temp = random.randint(25,29)
    
    # Rain
    if rain == 1:
        client.publish("tempsensor", temp-2)
        client.publish("moistsensor", 100)
        client.publish("on/off", 0)
    # No rain
    else:
        client.publish("tempsensor", temp)   
        moisture = random.randint(50,99)
        client.publish("on/off", 1)
        if moisture >= 85: 
            reservoir -= 5
            client.publish("wateramount",5)           
        elif moisture <= 60: 
            reservoir -= 15
            client.publish("wateramount",15)
        else: 
            reservoir -= 10
            client.publish("wateramount",5)
        client.publish("reservoir", reservoir)
        time.sleep(10)
    pass
