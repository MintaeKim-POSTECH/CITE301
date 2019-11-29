# Referenced by...
# http://www.gisdeveloper.co.kr/?p=6868
import numpy as np
import cv2
import glob
import os

# -- Configuration --
# CHESS_SQUARE_SIZE_MM = 30
# CHESS_GRID_HORIZONTAL = 7
# CHESS_GRID_VERTICAL = 8
#
# RESOLUTION_WIDTH = 640
# RESOLUTION_HEIGHT = 480
# # -- Configuration --
#
# # termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, CHESS_SQUARE_SIZE_MM, 0.001)
 
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((CHESS_GRID_HORIZONTAL*CHESS_GRID_VERTICAL, 3), np.float32)
objp[:, :2] = np.mgrid[0:CHESS_GRID_VERTICAL, 0:CHESS_GRID_HORIZONTAL].T.reshape(-1, 2)
 
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# Fetch Images to analyze patterns 
images = glob.glob('./Images_Data/Before/*.jpg')

for fname in images:
    fname_f = os.path.split(fname)[1]
    img = cv2.imread(fname)
    print ("Hello")

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow('img', gray)
    cv2.waitKey(500)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (CHESS_GRID_VERTICAL, CHESS_GRID_HORIZONTAL), None)
 
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        print ("findChessboardCorners Success " + fname_f)
        cv2.imwrite('./Images_Data/Candidates/' + fname_f, img) 
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)
 
        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (CHESS_GRID_VERTICAL, CHESS_GRID_HORIZONTAL), corners2, ret)
        cv2.imwrite('./Images_Data/GridDetection/' + fname_f , img)
        cv2.imshow('img',img)
        cv2.waitKey(500)

# Fetch Camera Matrix by calling cv2.getOptimalNewCameraMatrix()
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (RESOLUTION_WIDTH, RESOLUTION_HEIGHT), 1, (RESOLUTION_WIDTH, RESOLUTION_HEIGHT))

# Removal of Distortion	
img = cv2.imread('./Images_Data/Before/60.jpg')
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
 
x, y, w, h = roi
print ("h : " + str(h) + " / w : " + str(w))
dst = dst[y:y+h, x:x+w]
cv2.imwrite('./Images_Data/Result/Call_60.jpg',dst)

# Calculation of Callibration Error	
tot_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    tot_error += error
 
print("total error: ", tot_error/len(objpoints))

cv2.destroyAllWindows()
