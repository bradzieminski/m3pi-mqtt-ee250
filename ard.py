import sys
import paho.mqtt.client as mqtt
import time
import serial
import re

ser = serial.Serial("/dev/ttyACM0", 19200)
radius = 20
moving = False

def allBack(client, userdata, message):
	if message == "\x01\x01":
		print("WORKS")

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("ee250zc")
    client.message_callback_add("ee250zc", allBack)
    
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload))

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()
          
	while True:
		line = ser.readline().decode("utf-8", "replace")
		sensors = [int(re.sub('[^0-9]', '', s)) for s in line.split()]
		if (len(sensors) != 4):
			continue

		print(sensors)
	
