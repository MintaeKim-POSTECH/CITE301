# Referenced by...
# https://webnautes.tistory.com/1259
# https://www.youtube.com/watch?time_continue=422&v=zVuPIBW4Ri8&feature=emb_logo
# https://webnautes.tistory.com/1257
# https://stackoverflow.com/questions/30331944/finding-red-color-in-image-using-python-opencv
#
import cv2
import yaml
import time
from ImageManager import ImageManager

import numpy as np

# --- Import S_RoboticArmControl/RobotControl.py ---
import os
import sys
path_for_roboAC = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
path_for_roboAC = os.path.join(path_for_roboAC, 'S_RoboticArmControl')
sys.path.append(path_for_roboAC)

from RobotControl import Robot
# --- Import S_RoboticArmControl/RobotControl.py ---

# Configurations
config = yaml.load(open("./Config.yaml", 'r'), Loader=yaml.FullLoader)

def saveImages(imageManager):
    while (True):
        imageManager.update()
        time.sleep(0.1)

def updatePosition(robot_obj, imageManager):
    image_name = imageManager.getRecentImageName()

    ## Step 0 : Get the most recent image from directory Images
    frame_bgr = None
    # Reason for while loop is to ensure that we've successfully fetched image file.
    # Without the while loop, there was a chance for a case where fetching image failed
    # because cv2.imwrite was in progress.
    while True:
        frame_bgr = cv2.imread('./S_CameraVision/Images/' + image_name)
        if (frame_bgr == None):
            continue
        else :
            break
    print(image_name)

    ## Step 1 : Detect Points with Particular Color
    # Converting RGB to HSV - Robot
    robot_color_rgb = robot_obj.getColorRGB()
    robot_color_rgb_pixel = np.uint8([[robot_color_rgb]])
    robot_color_hsv = cv2.cvtColor(robot_color_rgb_pixel, cv2.COLOR_RGB2HSV)
    robot_color_hsv = robot_color_hsv[0][0]

    # Converting BGR to HSV - Image
    frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

    # Masking - Color
    mask = None
    if (robot_color_hsv[2] <= 50) : # Black (Useless)
        mask_l = np.array([0, 0, 0])
        mask_u = np.array([180, 255, 50])
        mask = cv2.inRange(frame_hsv, mask_l, mask_u)
    elif (robot_color_hsv[2] >= 205) : # White (Useless)
        mask_l = np.array([0, 0, 205])
        mask_u = np.array([180, 255, 255])
        mask = cv2.inRange(frame_hsv, mask_l, mask_u)
    if (robot_color_hsv[0] < config["COLOR_SENSITIVITY"]) :
        mask0_l = np.array([0, 30, 30])
        mask0_u = np.array([robot_color_hsv[0] + config["COLOR_SENSITIVITY"], 255, 255])
        mask0 = cv2.inRange(frame_hsv, mask0_l, mask0_u)

        mask1_l = np.array([robot_color_hsv[0] + 180 - config["COLOR_SENSITIVITY"], 30, 30])
        mask1_u = np.array([180, 255, 255])
        mask1 = cv2.inRange(frame_hsv, mask1_l, mask1_u)

        mask = mask0 + mask1
    elif (180 - robot_color_hsv[0] < config["COLOR_SENSITIVITY"]):
        mask0_l = np.array([robot_color_hsv[0] - config["COLOR_SENSITIVITY"], 30, 30])
        mask0_u = np.array([180, 255, 255])
        mask0 = cv2.inRange(frame_hsv, mask0_l, mask0_u)

        mask1_l = np.array([0, 30, 30])
        mask1_u = np.array([robot_color_hsv[0] + config["COLOR_SENSITIVITY"] - 180, 255, 255])
        mask1 = cv2.inRange(frame_hsv, mask1_l, mask1_u)

        mask = mask0 + mask1
    else :
        mask_l = np.array([robot_color_hsv[0] - config["COLOR_SENSITIVITY"], 30, 30])
        mask_u = np.array([robot_color_hsv[0] + config["COLOR_SENSITIVITY"], 255, 255])
        mask = cv2.inRange(frame_hsv, mask_l, mask_u)

    # Masking - Morphology (Clustering)
    kernel = np.ones((11, 11), np.uint8)
    mask_morph_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask_morph = cv2.morphologyEx(mask_morph_open, cv2.MORPH_CLOSE, kernel)

    # Filtered Image Frame
    frame_filtered = cv2.bitwise_and(frame_bgr, frame_bgr, mask=mask_morph)
    cv2.imwrite("./S_CameraVision/Images_Box/Filtered/" + image_name, frame_filtered)

    # Labeling - Clustering
    numOfLabels, img_label, stats, centroids = cv2.connectedComponentsWithStats(mask_morph)

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

        cv2.rectangle(frame_bgr, (x, y), (x + width, y + height), (0, 0, 255))

    # TODO: Delete (Testing Purpose Only)
    sticker_indices = [[250, 250], [400, 400], [400, 150]]

    cv2.imwrite('./S_CameraVision/Images_Box/Sticker/' + image_name, frame_bgr)

    # Calculation of Direction Vector & Position
    # assert (len(sticker_indices) == 3) # 3 Stickers!

    ### TODO : FAILURE ?
    # TODO: While Loop until passes assert condition

    ## Step 2 : Indicate the Center Point of Robot Arms with infos from Step 1

    d0_1 = np.sum((np.array(sticker_indices[0:1])) ** 2)
    d1_2 = np.sum((np.array(sticker_indices[1:2])) ** 2)
    d0_2 = np.sum((np.array([sticker_indices[0], sticker_indices[2]])) ** 2)
    dist = [d0_1, d0_2, d1_2]

    print ("sticker_indices : " + str(sticker_indices))
    print ("dist : " + str(dist))

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

    print ("point_head : " + str(point_head))
    print ("point_shoulder : " + str(point_shoulder))

    # Calculation of Direction Vector & Center
    # Direction Vector
    mid_point = np.array(point_shoulder[0]) + np.array(point_shoulder[1])
    mid_point = mid_point / 2
    dir_vector = np.array(point_head) - mid_point
    dir_vector_size = np.sum(dir_vector ** 2) ** 0.5
    dir_vector_unit = dir_vector / dir_vector_size

    print ("mid_point : " + str(mid_point))
    print ("dir_vector : " + str(dir_vector))
    print ("dir_vector_size : " + str(dir_vector_size))
    print ("dir_vector_unit : " + str(dir_vector_unit))

    # Center Position Data
    robot_cent_XY_pixel_np = np.array(point_head) + dir_vector_unit * config["CENTER_DIST_FROM_STICKER_MM"] / config["MM_PER_PIXEL"]
    robot_cent_XY_pixel = np.ndarray.tolist(robot_cent_XY_pixel_np)

    print ("Center : " + str(robot_cent_XY_pixel))

    # TODO: Convert pixel into mm
    # TODO: Delete (Testing Purpose Only)
    robot_cent_XY_mm = [50, 50]

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