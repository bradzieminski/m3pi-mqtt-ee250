import sys
import paho.mqtt.client as mqtt
import time
import serial
import re

ser = serial.Serial("/dev/ttyACM0", 19200)
radius = 20
moving = False

def allBack(client, userdata, message):
	global radius;
	dec = str(message.payload, "utf-8")
	elif dec == "\x01\01":
		radius = min(radius + 5, 50)
		print("r =", radius)
	elif dec == "\x01\02":
		radius = max(radius - 5, 20)
		print("r=", radius)

def on_connect(client, userdata, flags, rc):
	print("Connected to server (i.e., broker) with result code "+str(rc))
	client.subscribe("ee250zc")
	client.message_callback_add("ee250zc", allBack)

def on_message(client, userdata, msg):
	print("on_message: " + msg.topic + " " + str(msg.payload))

def readSensors():
	

def stop():
	client.publish("ee250zc", "\x01\x03")

def start():
	client.publish("ee250zc", "\x01\x04")

def checkGlitch():
	stop()

def alg(sensors):
	for s in sensors:
		if (98 - s) < 10:

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

		#print(sensors)

