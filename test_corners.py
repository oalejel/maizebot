from mapping import *
from constants import *
import utils
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

for filename in os.listdir("../sample_frames"):
    img = cv2.imread("../sample_frames/"+filename)

    lower = np.array([100, 60, 150], dtype = "uint8") # 131, 49, 72
    upper = np.array([170, 100, 200], dtype = "uint8") # 169, 87, 145

    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(img, lower, upper)
    mask = cv2.blur(mask, (5,5))

    contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:4]

    i = 0
    for c in contours:
        M = cv2.moments(c)
        if M["m00"] == 0: 
            continue
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        i += 1

        cv2.circle(img, (cX, cY), 5, (255, 255, 255), -1)
        cv2.putText(img, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.imshow("Image", mask)
    cv2.waitKey(0)