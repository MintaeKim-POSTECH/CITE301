# Reference by...
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
import cv2
import yaml
import threading

# Configurations
config = yaml.load(open("../Config.yaml", 'r'), Loader=yaml.FullLoader)

## -- Shared Objects (ImageManager) --
# Shared Objects are often implemented by inner class, as an encapsulated models.
# Shared Objects are private to others.
# These shared objects must be modified by public methods in class.
# Refer to Operation System Class (CSED312)
class ImageManager:
    def __init__(self):
        # Open the device at the ID 0
        self.cap = cv2.VideoCapture(0)
        if not (self.cap.isOpened()):
            print("Could not open video device")
            exit()

        # Reset Resolution
        ret = self.cap.set(3, config["RESOLUTION_WIDTH"])
        ret = self.cap.set(4, config["RESOLUTION_HEIGHT"])

        # Latest Image Number
        self.frame_num = 0

        # Lock
        self.lock = threading.Lock()

    def update(self):
        self.lock.acquire()
        # Capture frame-by-frame
        self.ret, self.frame = self.cap.read()

        # Fetching failed?
        if (self.ret != True):
            return -1

        if (self.frame_num % config["PROCESS_FRAME_INTERVAL"] == 0):
            cv2.imwrite('./Images/' + str(int(self.frame_num / config["PROCESS_FRAME_INTERVAL"])) + '.jpg', self.frame)

            # TODO: Callibration
            self.frame_cal = None

            cv2.imwrite('./Images_C/' + str(int(self.frame_num / config["PROCESS_FRAME_INTERVAL"])) + '_C.jpg', self.frame_cal)

        self.frame_num = self.frame_num + 1
        self.lock.release()

    def getRecentImageDir(self):
        self.lock.acquire()
        img_dir = './Images_C/' + str(int(self.frame_num / config["PROCESS_FRAME_INTERVAL"])) + '_C.jpg'
        self.lock.release()
        return img_dir

    def __del__(self):
        # When everything done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()
## -- Shared Objects (ImageManager) --