from constants import *
import utils
import numpy as np
import cv2
import matplotlib.pyplot as plt
from operator import itemgetter, attrgetter 
import time
class Maze:

    def warp_map(self, image):
        image_corners = self.detect_corners(image)

        hcrop = 10
        wcrop = 19

        precrop_height = HEIGHT_IN_CELLS + 2 * hcrop
        precrop_width = WIDTH_IN_CELLS + 2 * wcrop

        warped_corners = np.array(
            [
                [0 ,precrop_height], # bottom-left
                [precrop_width, precrop_height], # bottom-right
                [precrop_width, 0], # top-right
                [0, 0], #top-left
            ],
            dtype="float32")

        transform = cv2.getPerspectiveTransform(image_corners, warped_corners)
        warped = cv2.warpPerspective(image, transform, (precrop_width, precrop_height))

        cropped = warped[hcrop: hcrop+HEIGHT_IN_CELLS, wcrop:wcrop+WIDTH_IN_CELLS]
        return cropped

    def __init__(self, image):
        cropped = self.warp_map(image)
        self.map = np.zeros((HEIGHT_IN_CELLS, WIDTH_IN_CELLS), dtype="uint8")
        self.detect_holes(cropped)
        self.detect_walls(np.copy(cropped))

        self.time = 0
        self.ball_x = 0
        self.ball_y = 0
        self.ball_vx = 0
        self.ball_vy = 0

        self.goal_x = 0
        self.goal_y = 0

        self.detect_goal(image)
        self.writer = cv2.VideoWriter('outpy2.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (700,500))
        
    def detect_corners(self, img):

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([7, 130, 130], dtype = "uint8") # 131, 49, 72
        upper = np.array([15, 200, 170], dtype = "uint8")

        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.blur(mask, (5,5))

        im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)[:4]

        corners = []
    


        i = 0
        for c in contours:
            M = cv2.moments(c)
            if M["m00"] == 0: 
                continue
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            corners.append((cX, cY))
            i += 1
        
        corners = sorted(corners, key=itemgetter(1), reverse=True)
        corners[0:2] = sorted(corners[0:2], key=itemgetter(0))
        corners[2:4] = sorted(corners[2:4], key=itemgetter(0), reverse=True)

        corners_arr = np.zeros((4 ,2), dtype="float32")
        if len(corners) < 4:
            cv2.imshow("img.png", img)
            cv2.imshow("hsv.png", hsv)
            cv2.imshow("mask.png", mask)
            cv2.waitKey(0)
        for i in range(4):

            cX = corners[i][0]
            cY = corners[i][1]
            corners_arr[i,0] = cX
            corners_arr[i,1] = cY

        return corners_arr # bottom-left, bottom-right, top-right, top-left

    def detect_walls(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        img[self.map == 2] = 255

        bw_threshold = 60
        
        img[img> bw_threshold] = 255
        img[img< bw_threshold] = 0
        img = 255 - img

        ero0 = 2
        kernel = np.ones((ero0, ero0), np.uint8) 
        img = cv2.erode(img, kernel)

        dil1 = 10  
        kernel = np.ones((dil1, dil1), np.uint8) 
        img = cv2.dilate(img, kernel)

        ero1 = 16
        kernel = np.ones((ero1, ero1), np.uint8) 
        img = cv2.erode(img, kernel)
        dil2 = 9
        kernel = np.ones((dil2, dil2), np.uint8) 
        img = cv2.dilate(img, kernel)

        self.map[img > 10] = 1

    def detect_holes(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower = np.array([90, 160, 80], dtype = "uint8")
        upper = np.array([110, 255, 150], dtype = "uint8")

        mask = cv2.inRange(hsv, lower, upper)

        dil1 = 12
        kernel = np.ones((dil1, dil1), np.uint8) 
        mask = cv2.dilate(mask, kernel)

        threshold = 10

        self.map[mask > 10] = 2

    def detect_ball(self, image, time):

        image = self.warp_map(image)
        self.writer.write(image)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = np.array([19, 53, 86], dtype = "uint8")
        upper = np.array([29, 176, 161], dtype = "uint8")

        mask = cv2.inRange(hsv, lower, upper)

        dil1 = 3  
        kernel = np.ones((dil1, dil1), np.uint8) 
        mask = cv2.dilate(mask, kernel)

        mask = cv2.blur(mask, (5,5))

        im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            cv2.imshow("hHv", hsv)
            cv2.imshow("mMsk", mask)
            cv2.waitKey(0)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)[:1]
        M = cv2.moments(contours[0])
        
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])

        self.ball_vx =  (x - self.ball_x)/(time - self.time)
        self.ball_vy =  (y - self.ball_y)/(time - self.time)

        self.time = time
        self.ball_x = x
        self.ball_y = y

        cv2.circle(image, (self.ball_x, self.ball_y), 3, (255, 255, 255), -1)

        return self.ball_y, self.ball_x, self.ball_vy, self.ball_vx


    def detect_goal(self, image):

        image = self.warp_map(image)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = np.array([150, 100, 100], dtype = "uint8")
        upper = np.array([180, 210, 195], dtype = "uint8")

        mask = cv2.inRange(hsv, lower, upper)

        dil1 = 3  
        kernel = np.ones((dil1, dil1), np.uint8) 
        mask = cv2.dilate(mask, kernel)

        mask = cv2.blur(mask, (5,5))

        im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        M = cv2.moments(contours[0])
        
        self.goal_x = int(M["m10"] / M["m00"])
        self.goal_y = int(M["m01"] / M["m00"])

        cv2.circle(image, (self.goal_x, self.goal_y), 3, (255, 255, 255), -1)

        return self.goal_x, self.goal_y


