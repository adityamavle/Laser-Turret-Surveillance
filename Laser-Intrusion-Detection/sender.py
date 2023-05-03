import serial
import json

# Open the serial port
ser = serial.Serial('COM5', 9600)

# Create a sample dictionary
data = {'person': 1, 'angle_x': -17, 'angle_y': 33}

# Encode the dictionary as a JSON string
json_str = json.dumps(data)
# Send the JSON string through the serial port

ser.write(json_str.encode())
# Close the serial port

ser.close()
