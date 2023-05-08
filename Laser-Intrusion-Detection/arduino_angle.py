import serial

connection = serial.Serial("COM5",9600)
while True:
    num = input("Enter Number")
    connection.write(num.encode())