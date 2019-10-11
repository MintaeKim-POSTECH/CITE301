# Reference by...
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
import numpy as np
import cv2
import time

# Open the device at the ID 0
cap = cv2.VideoCapture(0)
if not (cap.isOpened()):
    printf("Could not open video device")
    exit()

# Reset Resolution
ret = cap.set(3, 640)
ret = cap.set(4, 480)
    
# Image Number
frame_num = 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Fetching failed?
    if (ret != True):
        break
    
    if (frame_num % 25 == 0) :
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame',gray)
        
        cv2.imwrite('./Images/' + str(frame_num / 25) + '.jpg', gray)
    
    frame_num = frame_num + 1
    
    # Get Keyboard Interruptions (Exit Condition)
    key = cv2.waitKey(1)
    if (key & 0xFF) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()