import serial

ser = serial.Serial("/dev/ttyACM0", 19200)

while True:
	line = ser.readline().decode("utf-8", "replace")
	print(line)
