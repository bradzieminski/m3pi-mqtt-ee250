import sys
import paho.mqtt.client as mqtt
import time
import serial
import re
from threading import Thread

ser = serial.Serial("/dev/ttyACM0", 19200)
client = mqtt.Client()

last_received = ''
sensors = []
radius = 20
patroling = False
kludge = [True, True, True]

def receiving():
	global ser
	global last_received

	while True:
		last_received = ser.readline().decode("utf-8", "replace")

def toggleBack(client, userdata, message):
	global patroling
	global kludge
	if kludge[0]:
		kludge[0] = False
		return

	patroling = ~patroling
	if patroling:
		client.publish("ee250zc/rpi_radius", str(radius))
		patrol()

def radiusIncBack(client, userdata, message):
	global kludge
	if kludge[1]:
		kludge[1] = False
		return

	radius = min(radius + 5, 20)
	client.publish("ee250zc/rpi_radius", str(radius))
	client.publish("ee250zc", "\x01\x01")

def radiusDecBack(client, userdata, message):
	global kludge
	if kludge[2]:
		kludge[2] = False
		return
	
	radius = max(radius - 5, 20)
	client.publish("ee250zc/rpi_radius", str(radius))
	client.publish("ee250zc", "\x01\x02")

def on_connect(client, userdata, flags, rc):
	print("Connected to server (i.e., broker) with result code "+str(rc))
	client.subscribe("ee250zc/rpi_toggle")
	client.subscribe("ee250zc/rpi_radius_inc")
	client.subscribe("ee250zc/rpi_radius_dec")
	client.message_callback_add("ee250zc/rpi_toggle", toggleBack)
	client.message_callback_add("ee250zc/rpi_radius_inc", radiusIncBack)
	client.message_callback_add("ee250zc/rpi_radius_dec", radiusDecBack)

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

def rotate90CW():
	client.publish("ee250zc", "\x01\x05")
	time.sleep(2)

def rotate90CCW():
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
				if abs(sensors[n] - radius) > 2:
					reRadius(n)
				time.sleep(.5)
def patrol():
	global sensors
	global patroling

	start()
	while patroling:
		sensors = readSensors()
		alg()
	stop()

if __name__ == '__main__':
	Thread(target=receiving).start()
	client.on_message = on_message
	client.on_connect = on_connect
	client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
	client.loop_start()

	while True:
		pass
