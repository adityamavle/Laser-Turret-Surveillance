import cv2
import time
import os
import random
# create directory to save photos if it doesn't already exist
if not os.path.exists('photos'):
    os.makedirs('photos')

# initialize the camera
cap = cv2.VideoCapture(0)

# set resolution of the camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# set project name and detection number
project_name = "laser"
test_dir = "test"
detection_num = 0
while True:
    # Capture a photo
    ret, frame = cap.read()
    #detection_num = random.randint(10, 99)
    # Save the photo to a directory with a name based on the detection number
    detection_dir = os.path.join(project_name, f"detections{detection_num}")
    #os.makedirs(detection_dir, exist_ok=True)
    photo_path = os.path.join(test_dir, f"{int(time.time())}.jpg")
    cv2.imwrite(photo_path, frame)

    # Run YOLO on the photo

    yolo_command = f"python yolov5/detect.py --source {photo_path} --weights trained/last.pt --img 416 --save-txt --save-conf --conf-thres 0.50 --project {project_name} --name detections{detection_num}"
    os.system(yolo_command)
    print(yolo_command)
    # Run laser_pointer.py on the photo
    print(detection_dir)
    laser_ptr_cmd = f"python -u c:\\Users\\adity\\Laser-Intrusion-Detection\\laser_pointer.py {detection_dir}"

    os.system(laser_ptr_cmd)

    # Increment the detection number
    detection_num += 1
    time.sleep(10)
    # Wait for 10 seconds before capturing the next photo
# release the camera and close the window
# cap.release()
# cv2.destroyAllWindows()
