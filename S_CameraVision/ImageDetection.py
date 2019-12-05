# Referenced by...
# https://webnautes.tistory.com/1259
# https://www.youtube.com/watch?time_continue=422&v=zVuPIBW4Ri8&feature=emb_logo
# https://webnautes.tistory.com/1257
# https://stackoverflow.com/questions/30331944/finding-red-color-in-image-using-python-opencv
# https://stackoverflow.com/questions/33548956/detect-avoid-premature-end-of-jpeg-in-cv2-python
# https://medium.com/joelthchao/programmatically-detect-corrupted-image-8c1b2006c3d3
# https://github.com/webnautes/nudapeu/blob/master/opencv-python-006.py
import cv2
import yaml
import time
from skimage import io
import numpy as np
from PyQt5 import QtCore
import time

# from S_CameraVision.ImageManager import ImageManager
import S_CameraVision.ConvertPixel2Real as ConvertPixel2Real
from S_RoboticArmControl.RobotControl import Robot

# Configurations
config = yaml.load(open("./Config.yaml", 'r'), Loader=yaml.FullLoader)

def saveImages(imageManager):
    while (True):
        imageManager.update()
        time.sleep(0.1)

class UpdatePositionClass (QtCore.QObject) :
    updated_image_conn = QtCore.pyqtSignal(Robot, str)

    def __init__(self, parent=None):
        super(UpdatePositionClass, self).__init__(parent)

    def updatePosition(self, robot_obj, imageManager) :
        image_name = None

        ## Step 0 : Get the most recent image from directory Images
        frame_hue = None

        while True:
            # Reason for while loop is to ensure that we've successfully fetched image file.
            # Without the while loop, there was a chance for a case where fetching image failed
            # Instead of using cv2.imread, we use skimage.imread to detect corrupted jpeg files.
            while True:
                image_name = imageManager.getRecentImageName()
                try :
                    frame_rgb = io.imread('./S_CameraVision/Images/' + image_name)
                except :
                    print("Pre-mature end of JPEG File, Re-try")
                    continue
                break

            print(image_name)

            ## Step 1 : Detect Points with Particular Color
            # Get Hue value - Robot
            robot_color_h = robot_obj.getHue()

            # Converting BGR to HSV - Image
            frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
            frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

            # Masking - Color
            threshold = config["COLOR_THRESHOLD"]
            sensitivity = config["COLOR_SENSITIVITY"]

            # Red - I
            if robot_color_h < sensitivity:
                lower_blue1 = np.array([robot_color_h - sensitivity + 180, threshold, threshold])
                upper_blue1 = np.array([180, 255, 255])
                lower_blue2 = np.array([0, threshold, threshold])
                upper_blue2 = np.array([robot_color_h, 255, 255])
                lower_blue3 = np.array([robot_color_h, threshold, threshold])
                upper_blue3 = np.array([robot_color_h + sensitivity, 255, 255])
                #     print(i-10+180, 180, 0, i)
                #     print(i, i+10)

            # Red - II
            elif robot_color_h > 180 - sensitivity:
                lower_blue1 = np.array([robot_color_h, threshold, threshold])
                upper_blue1 = np.array([180, 255, 255])
                lower_blue2 = np.array([0, threshold, threshold])
                upper_blue2 = np.array([robot_color_h + sensitivity - 180, 255, 255])
                lower_blue3 = np.array([robot_color_h - sensitivity, threshold, threshold])
                upper_blue3 = np.array([robot_color_h, 255, 255])

            # Others :>
            else:
                lower_blue1 = np.array([robot_color_h, threshold, threshold])
                upper_blue1 = np.array([robot_color_h + sensitivity, 255, 255])
                lower_blue2 = np.array([robot_color_h - sensitivity, threshold, threshold])
                upper_blue2 = np.array([robot_color_h, 255, 255])
                lower_blue3 = np.array([robot_color_h - sensitivity, threshold, threshold])
                upper_blue3 = np.array([robot_color_h, 255, 255])

            img_mask1 = cv2.inRange(frame_hsv, lower_blue1, upper_blue1)
            img_mask2 = cv2.inRange(frame_hsv, lower_blue2, upper_blue2)
            img_mask3 = cv2.inRange(frame_hsv, lower_blue3, upper_blue3)
            img_mask = img_mask1 | img_mask2 | img_mask3

            # Masking - Morphology (Clustering)
            kernel_size = config["COLOR_MORPH_KERNEL_SIZE"]

            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            img_mask = cv2.morphologyEx(img_mask, cv2.MORPH_OPEN, kernel)
            img_mask = cv2.morphologyEx(img_mask, cv2.MORPH_CLOSE, kernel)

            img_result = cv2.bitwise_and(frame_hsv, frame_hsv, mask=img_mask)

            # Labeling - Clustering
            numOfLabels, img_label, stats, centroids = cv2.connectedComponentsWithStats(img_result)

            # Fetch Indices of Stickers
            sticker_indices = []
            for idx, centroid in enumerate(centroids) :
                if (stats[idx][0] == 0 and stats[idx][1] == 0) :
                    continue

                if (np.any(np.isnan(centroid))):
                    continue

                x, y, width, height, area = stats[idx]
                centerX, centerY = int(centroid[0]), int(centroid[1])

                # Adding Index in List
                sticker_indices.append((centerX, centerY))
                cv2.circle(frame_bgr, (centerX, centerY), 10, (0, 0, 255), 10)
                cv2.rectangle(frame_bgr, (x, y), (x + width, y + height), (0, 0, 255))

            if (len(sticker_indices) == 3):
                break
            else :
                # Print Stickers
                cv2.imshow(frame_bgr)
                print (len(sticker_indices))
                time.sleep(0.5)

        cv2.imwrite('./S_CameraVision/Images_Box/Sticker/' + image_name, frame_bgr)

        # Calculation of Direction Vector & Position
        assert (len(sticker_indices) == 3) # 3 Stickers!

        ## Step 2 : Indicate the Center Point of Robot Arms with infos from Step 1

        d0_1 = np.sum((np.array(sticker_indices[0:1])) ** 2)
        d1_2 = np.sum((np.array(sticker_indices[1:2])) ** 2)
        d0_2 = np.sum((np.array([sticker_indices[0], sticker_indices[2]])) ** 2)
        dist = [d0_1, d0_2, d1_2]

        # print ("sticker_indices : " + str(sticker_indices))
        # print ("dist : " + str(dist))

        point_head = None
        point_shoulder = None
        if (min(dist) == d0_1) :
            point_head = sticker_indices[2]
            point_shoulder = [sticker_indices[0], sticker_indices[1]]
        elif (min(dist) == d1_2) :
            point_head = sticker_indices[0]
            point_shoulder = [sticker_indices[1], sticker_indices[2]]
        else :
            point_head = sticker_indices[1]
            point_shoulder = [sticker_indices[0], sticker_indices[2]]

        # print ("point_head : " + str(point_head))
        # print ("point_shoulder : " + str(point_shoulder))

        # Calculation of Direction Vector & Center
        # Direction Vector
        mid_point = np.array(point_shoulder[0]) + np.array(point_shoulder[1])
        mid_point = mid_point / 2
        dir_vector = np.array(point_head) - mid_point
        dir_vector_size = np.sum(dir_vector ** 2) ** 0.5
        dir_vector_unit = dir_vector / dir_vector_size

        # print ("mid_point : " + str(mid_point))
        # print ("dir_vector : " + str(dir_vector))
        # print ("dir_vector_size : " + str(dir_vector_size))
        # print ("dir_vector_unit : " + str(dir_vector_unit))

        # Center Position Data
        robot_cent_XY_pixel_np = np.array(point_head) + dir_vector_unit * config["CENTER_DIST_FROM_STICKER_MM"] / config["MM_PER_PIXEL"]
        robot_cent_XY_pixel = np.ndarray.tolist(robot_cent_XY_pixel_np)

        # print ("Center : " + str(robot_cent_XY_pixel))

        # Convert pixel into mm
        robot_cent_XY_mm = ConvertPixel2Real.Pixel2Real(robot_cent_XY_pixel)
        # robot_cent_XY_mm = [50, 50]

        print ("Center (mm) : " + str(robot_cent_XY_mm))

        # Saving Information in Robot Object
        robot_cent_XY_mm_obj = []
        robot_cent_XY_mm_obj.extend(robot_cent_XY_mm)
        robot_cent_XY_mm_obj.append(0)
        robot_obj.setPos_position(robot_cent_XY_mm_obj)
        dir_vector_unit_obj = []
        dir_vector_unit_obj.extend(dir_vector_unit)
        dir_vector_unit_obj.append(0)
        robot_obj.setPos_angle(dir_vector_unit_obj)

        ## Step 3 : Drawing Circle
        center = (int(robot_cent_XY_pixel[0]), int(robot_cent_XY_pixel[1]))
        radian = int(config["ROBOT_BODY_SIZE_MM"] / config["MM_PER_PIXEL"])
        color = (255, 0, 0)
        thickness = 2
        cv2.circle(frame_bgr, center, radian, color, thickness)

        cv2.imwrite('./S_CameraVision/Images_Box/Robot/' + image_name, frame_bgr)

        self.updated_image_conn.emit(robot_obj, './S_CameraVision/Images_Box/Robot/' + image_name)