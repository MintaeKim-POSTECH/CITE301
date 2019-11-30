# Reference by...
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
import numpy as np
import cv2
import time

# ------ Configuration ------
RESOLUTION_WIDTH = 640
RESOLUTION_HEIGHT = 480

# Frame to process (time)
PROCESS_FRAME_INTERVAL = 25
# ------ Configuration ------

# Open the device at the ID 0
cap = cv2.VideoCapture(0)
if not (cap.isOpened()):
    print("Could not open video device")
    exit()

# Reset Resolution
ret = cap.set(3, RESOLUTION_WIDTH)
ret = cap.set(4, RESOLUTION_HEIGHT)
    
# Image Number
frame_num = 0

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Fetching failed?
    if (ret != True):
        break
    
    if (frame_num % PROCESS_FRAME_INTERVAL == 0 and frame_num > 0) :

        # Display the resulting frame
        cv2.imshow('frame', frame)

        cv2.imwrite('./Images/' + str(int (frame_num / PROCESS_FRAME_INTERVAL)) + '.jpg', frame)

    frame_num = frame_num + 1
    
    # Get Keyboard Interruptions (Exit Condition)
    key = cv2.waitKey(1)
    if (key & 0xFF) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
