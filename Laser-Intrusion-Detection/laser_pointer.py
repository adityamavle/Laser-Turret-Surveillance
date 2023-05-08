import cv2
import math
import os
import pandas as pd
import time
import json
import serial
from pprint import pprint
import random
import warnings
import time
import sys


def angle_map(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


ser = serial.Serial("COM5", baudrate=9600,
                    timeout=5.0,
                    parity=serial.PARITY_NONE,
                    bytesize=serial.EIGHTBITS,
                    stopbits=serial.STOPBITS_ONE
                    )
warnings.filterwarnings('ignore', category=DeprecationWarning)
# Create an empty DataFrame to store laser pointer angles
#df = pd.DataFrame(data)
# cols = ['idx', 'time', 'person', 'angle_x', 'angle_y']
# df = pd.DataFrame(columns=cols)
df = pd.DataFrame({'idx': [0], 'time': [0.0], 'person': [
                  'person_1'], 'angle_x': [0.0], 'angle_y': [0.0]})
prev_angle_x = None  # Store previous angle_x
prev_angle_y = None  # Store previous angle_y
# Iterate through all image files in the directory
detection_dir = sys.argv[1]
#detection_dir = r'laser\detections8'
print('Laser Pointer.py has this dir', detection_dir)
# loop through the detection images in the directory
for image_file in os.listdir(detection_dir):
    if image_file.endswith('.jpg'):
        image_path = os.path.join(detection_dir, image_file)
        # process the image and update laser pointer position
        label_file = os.path.join(
            detection_dir, 'labels', os.path.splitext(image_file)[0] + '.txt')

        if not os.path.exists(label_file):
            # Skip iteration if label file does not exist
            continue

        # Read image and label file
        img = cv2.imread(image_path)
        with open(label_file, 'r') as f:
            lines = f.readlines()

        # Iterate through all the detections
        for line in lines:
            data = line.split(' ')
            print('The data is given as', data)
            if data[0] == '0':  # Object is a person
                x_center = float(data[1]) * img.shape[1]
                y_center = float(data[2]) * img.shape[0]
                width = float(data[3]) * img.shape[1]
                height = float(data[4]) * img.shape[0]

                # Calculate the change in angle of the laser pointer
                x_diff = x_center - img.shape[1] / 2
                y_diff = y_center - img.shape[0] / 2
                angle_x = math.degrees(math.atan2(x_diff, img.shape[1] / 2))
                angle_y = math.degrees(math.atan2(y_diff, img.shape[0] / 2))

                # angle_x = int(map(angle_x, -90, 90, 0, 180))
                # angle_y = int(map(angle_y, -90, 90, 0, 180))
                angle_x = angle_map(angle_x, -90, 90, 0, 180)

                if prev_angle_x is not None and prev_angle_y is not None:
                    angle_x_diff = angle_x - prev_angle_x
                    angle_y_diff = angle_y - prev_angle_y
                else:
                    angle_x_diff = angle_x
                    angle_y_diff = angle_y

                # Update laser pointer position and previous angle
                person = 'person_' + str(len(df) + 1)
                df = df.append({'idx': os.path.splitext(image_file)[0], 'time': '', 'person': person,
                                'angle_x': angle_x, 'angle_y': angle_y, 'angle_x_diff': angle_x_diff,
                                'angle_y_diff': angle_y_diff}, ignore_index=True)
                prev_angle_x = angle_x
                prev_angle_y = angle_y
                # data = {'angle_x': 50}
                #data = {"angle_x": angle_x}
                angle_x = 180.0 - angle_x
                print(type(angle_x))
                angle_x = int(angle_x)
                angle_x = str(angle_x)
                print('The angle rn', angle_x)
                # print(angle_x)
                print(type(angle_x))
                #data["operation"] = "sequence"
                #data = json.dumps(data)
                # ser.write(angle_x)
                # ser.flush()
                print(data)
                # if ser.isOpen():
                #print('Ascii encoded angle_x', angle_x.encode('ascii'))
                #angle_x_write = angle_x + '/n'
                #print('Angle x being written is',angle_x_write.encode('ascii'))
                ser.write(angle_x.encode('ascii'))
                # ser.flush()
                # try:
                incoming = ser.readline().decode('utf-8')
                print("Incoming value from arduino", incoming)
                print(incoming)
                #response = json.loads(incoming)
                # if "confirmed" in response:
                #confirmed = response["confirmed"]
                #myJson = json.loads(incoming)
                # print(type(myJson))
                # except Exception as e:
                #        print(e)
                #        pass
                # ser.close()
                # else:
                #    print("opening error")
                # Update laser pointer position
                # Add red dot at laser pointer position
                cv2.circle(img, (int(x_center), int(y_center)),
                           5, (0, 0, 255), -1)
        #cv2.namedWindow('My Image', cv2.WINDOW_NORMAL)
        #cv2.imshow('My Image', img)
        # cv2.imshow(img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

# Print the DataFrame with laser pointer angles
print(df)
ser.close()
