import cv2
import numpy as np

class Readers:
    def __init__(self, input, isVideo):
        if isVideo:
            print("Input mode: video")
        else:
            print("Input mode: camera stream")
        self.capture = cv2.VideoCapture