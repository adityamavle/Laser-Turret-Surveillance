import serial
import time

arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.1)
def write_read(x):
    if x == '1':
        arduino.write(b'1')
        time.sleep(0.05)
        data = arduino.readline()
        return data
    if x == '0':
        arduino.write(b'0')
        time.sleep(0.05)
        data = arduino.readline()
        return data
while True:
    num = input("Enter a number: ") # Taking input from user
value = write_read(num)
print(value) # printing the value