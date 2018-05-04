import sys
import paho.mqtt.client as mqtt
import time
import serial
import re
from threading import Thread

ser = serial.Serial("/dev/ttyACM0", 19200)
client = mqtt.Client()

last_received = ""
status = ""
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
	global radius

	if kludge[0] == True:
		kludge[0] = False
		return
	else:
		print("toggle")
		if patroling == True:
			patroling = False
		else:
			patroling = True
			client.publish("ee250zc/rpi_radius", str(radius))
			Thread(target=patrol).start()

def radiusIncBack(client, userdata, message):
	global kludge
	global radius
	
	if kludge[1] == True:
		kludge[1] = False
		return

	radius = min(radius + 5, 50)
	print("inc r =", str(radius))
	client.publish("ee250zc/rpi_radius", str(radius))
	client.publish("ee250zc", "\x01\x01")

def radiusDecBack(client, userdata, message):
	global kludge
	global radius

	if kludge[2] == True:
		kludge[2] = False
		return

	print("dec radius")
	radius = max(radius - 5, 20)
	client.publish("ee250zc/rpi_radius", str(radius))
	client.publish("ee250zc", "\x01\x02")

def on_connect(client, userdata, flags, rc):
	print("Connected to server (i.e., broker) with result code "+str(rc))
	client.subscribe("ee250zc/rpi_toggle")
	client.subscribe("ee250zc/rpi_inc_radius")
	client.subscribe("ee250zc/rpi_dec_radius")
	client.message_callback_add("ee250zc/rpi_toggle", toggleBack)
	client.message_callback_add("ee250zc/rpi_inc_radius", radiusIncBack)
	client.message_callback_add("ee250zc/rpi_dec_radius", radiusDecBack)

def on_message(client, userdata, msg):
	print("on_message: " + msg.topic + " " + str(msg.payload))

def readSensors():
	global status
	global sensors
	global last_received

	while True:
		line = last_received
		sensors = [int(re.sub('[^0-9]', '', s)) for s in line.split()]
		if (len(sensors) == 4):
			print(sensors, status)
			break

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
	global sensors
	global status
	status = "reRadius s="+str(n)

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
	global status
	status = "checkRobot s="+str(n)

	stop()
	prev = sensors[n]

	for n in range(1):
		#time.sleep(1)
		readSensors()
		if sensors[n] != prev:
			start()
			status = ""
			return False
	status = ""
	return True

def alg():
	global sensors
	global status

	for n in range(4):
		if sensors[n] < 70:
			if checkRobot(n):
				if abs(sensors[n] - radius) > 2:
					reRadius(n)
				time.sleep(2)
def patrol():
	global sensors
	global patroling

	start()
	while patroling:
		readSensors()
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
