import serial
import re

ser = serial.Serial("/dev/ttyACM0", 19200)

while True:
	line = ser.readline().decode("utf-8", "replace")
	sensors = [int(re.sub('[^0-9]', '', s)) for s in line.split()]
	if (len(sensors) != 4):
		continue
	print(sensors)
	
