import time
import random
import sys
from Adafruit_IO import MQTTClient
import requests

AIO_USERNAME = "Afihu"
temp = open("key")
AIO_KEY = temp.read()
temp.close()

def connected(client):
    client.subscribe("lightsensor")
    client.subscribe("moistsensor")
    client.subscribe("on-slash-off")
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

reservoir = 100

while True:  
    # Whether it's day or night/ raining or not.
    sun = random.randint(0,1) # Day (5am - 7pm)/Night (7pm - 5am).
    rain = random.randint(0,1) # Rain
    client.publish("lightsensor", sun)
    client.publish("rainsensor", rain)
    time.sleep(3)
    
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
        client.publish("on-slash-off", 0)
    # No rain
    else:
        client.publish("tempsensor", temp)   
        moisture = random.randint(50,99)
        client.publish("on-slash-off", 1)
        time.sleep(1)
        client.publish("moistsensor", moisture)
        time.sleep(3)
        
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
    
    if reservoir == 0: reservoir = 100
    time.sleep(10)
    
    pass