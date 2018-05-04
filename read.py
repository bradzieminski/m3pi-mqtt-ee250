import sys
import paho.mqtt.client as mqtt
import time
import serial
import re

ser = serial.Serial("/dev/ttyACM0", 19200)

def readSensors():
	#ser = serial.Serial("/dev/ttyACM0", 19200)
	while True:
		line = ser.readline().decode("utf-8", "replace")
		sensors = [int(re.sub('[^0-9]', '', s)) for s in line.split()]
		if (len(sensors) != 4):
			continue
		return sensors

if __name__ == '__main__':
	while True:
		sensors = readSensors()
		print(sensors)

