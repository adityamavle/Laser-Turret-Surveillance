import time
import json
import serial
from pprint import pprint
import random

if __name__ == "__main__":
    print("Ready...")
    ser = serial.Serial("COM5", baudrate=9600,
                        timeout=2.5,
                        parity=serial.PARITY_NONE,
                        bytesize=serial.EIGHTBITS,
                        stopbits=serial.STOPBITS_ONE
                        )
    data = {'angle_x': 50}
    #data["operation"] = "sequence"

    data = json.dumps(data)
    print(data)
    if ser.isOpen():
        ser.write(data.encode('ascii'))
        ser.flush()
        try:
            while True:
                incoming = ser.readline().decode("utf-8")
                if incoming:
                    print("Incoming",incoming.strip())
                    response = json.loads(incoming)
                    # if "confirmed" in response:
                    #     confirmed = response["confirmed"]
                    #     break
        except Exception as e:
            print(e)
            pass
        ser.close()
    else:
        print("opening error")
