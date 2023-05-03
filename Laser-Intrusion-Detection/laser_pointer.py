import cv2
import math
import os
import pandas as pd

# Create an empty DataFrame to store laser pointer angles
df = pd.DataFrame(columns=['idx', 'time', 'person', 'angle_x', 'angle_y'])
prev_angle_x = None  # Store previous angle_x
prev_angle_y = None  # Store previous angle_y
# Iterate through all image files in the directory
image_dir = r'yolov5/runs/detect/exp2'
for image_file in os.listdir(image_dir):
    if image_file.endswith('.png'):
        image_path = os.path.join(image_dir, image_file)
        label_file = os.path.join(
            image_dir, 'labels', os.path.splitext(image_file)[0] + '.txt')

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
                # Update laser pointer position
                # Add red dot at laser pointer position
                cv2.circle(img, (int(x_center), int(y_center)),
                           5, (0, 0, 255), -1)
        #cv2.namedWindow('My Image', cv2.WINDOW_NORMAL)
        #cv2.imshow('My Image', img)
        # cv2.imshow(img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Print the DataFrame with laser pointer angles
print(df)
