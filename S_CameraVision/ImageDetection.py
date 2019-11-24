# Reference by...
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
import cv2
import yaml
import time
from ImageManager import ImageManager

# Configurations
config = yaml.load(open("../Config.yaml", 'r'), Loader=yaml.FullLoader)

def saveImages(imageManager):
    while (True):
        imageManager.update()
        time.sleep(1)

def updatePosition(imageManager):
    ### TODO : FAILURE ?
    # Step 0 : Get the most recent image from directory Images
    frame_cal = cv2.imread(imageManager.getRecentImageDir())

    # Step 1 : Detect Points with Particular Color

    # Step 2 : Indicate the Center Point of Robot Arms with infos from Step 1

    ### TODO : Correspondance between images and conn

    # Step 3 : Drawing Squares or Rectangles

    ### TODO : How about Directions?

    # Step 4 : Calculation of Trajectories
    # Assumptions that two robot arm trajectories don't have ant conflicts!
    # Elaboration in CITD IV

    pass