print("Hello IoT Python")
import sys
from Adafruit_IO import MQTTClient
import random
import time
from simple_ai import *
from uart import *

AIO_FEED_ID = ["nutnhan1", "nutnhan2"]
AIO_USERNAME = "EmChes"
AIO_KEY = "aio_hZRZ47DHfsk67ZGpT99gIkWoHyPA"

def connected(client):
    print("Ket noi thanh cong ...")
    # client.publish("signal", "1")
    for id in AIO_FEED_ID:
        client.subscribe(id)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    # client.publish("signal", "0")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Data is from: " + feed_id + ", Payload: " + payload)
    uart_write(payload)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
counter_sensor = 30
counter_ai = 10
counter_signal = 5
while True:
    counter_signal = counter_signal - 1
    if counter_signal <= 0:
        counter_signal = 5
        if client.is_connected():
            client.publish("signal", "1")
        else:
            client.publish("signal", "0")

    time.sleep(1)
    readSerial()            
    counter_sensor = counter_sensor - 1
    if counter_sensor <=0:
        counter_sensor = 30
        lux = getLux()
        client.publish("cambien3", lux)
    if counter_sensor == 20:
        humi = getHumi()
        client.publish("cambien2", humi)
    if counter_sensor == 10:
        temp = getTemp()
        client.publish("cambien1", temp)

    counter_ai = counter_ai - 1
    if counter_ai <=0:
        counter_ai = 15
        image_capture()
        ai_result = image_detector()
        client.publish("AI", ai_result)

    # readSerial()
    pass
