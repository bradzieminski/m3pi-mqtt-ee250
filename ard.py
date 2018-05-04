import sys
import paho.mqtt.client as mqtt
import time
import serial
import re
from threading import Thread

ser = serial.Serial("/dev/ttyACM0", 19200)
radius = 20
moving = False
sensors = []

last_received = ''

def receiving():
	global ser
	global last_received

	while True:
		last_received = ser.readline().decode("utf-8", "replace")

def allBack(client, userdata, message):
	global radius;
	dec = str(message.payload, "utf-8")
	if dec == "\x01\01":
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
	global sensors
	while True:
		line = last_received
		sensors = [int(re.sub('[^0-9]', '', s)) for s in line.split()]
		if (len(sensors) != 4):
			continue
		print(sensors)
		return sensors

def stop():
	client.publish("ee250zc", "\x01\x03")

def start():
	client.publish("ee250zc", "\x01\x00")

def moveForward():
	client.publish("ee250zc", "\x01\x04")

def rotate90CW:
	client.publish("ee250zc", "\x01\x05")
	time.sleep(2)

def rotate90CCW:
	client.publish("ee250zc", "\x01\x06")
	time.sleep(2)

def reRadius(n):
	if sensors[n] > radius:
		rotate90CCW()
		moveForward()
		while sensors[n] > radius:
			readSensors()
		stop()
		rotate90CW()
	else:
		rotate90CW()
		moveForward()
		while sensors[n] < radius:
			readSensors()
		stop()
		rotate90CCW()
	start()


def checkRobot(n):
	global sensors
	stop()
	prev = sensors[n]

	for n in range(3):
		time.sleep(1)
		sensors = readSensors()
		if sensors[n] != prev:
			start()
			return False
	return True

def alg():
	global sensors
	for n in range(4):
		if sensors[n] < 70:
			if checkRobot(n):
				if abs(sensors[n] - radius) > 2
					reRadius(n)

if __name__ == '__main__':
	Thread(target=receiving).start()

	client = mqtt.Client()
	client.on_message = on_message
	client.on_connect = on_connect
	client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
	client.loop_start()

	start()
	while True:
		sensors = readSensors()
		alg()

