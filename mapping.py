#  **Gets data from** homography.py
#     - **Purpose:** processes the first camera frame to produce a discrete map of the maze
#     - **Functions** 
#       - filter_map(): filter the image 
#       - detect_corners(): detect the corners of the maze
#       - fit_homography(): find homography to transform image to uniform dimensions and flat orientation
#       - apply_homography(): transform image
#       - discretize(): discretize the image into cells
#       - detect_holes(): detect holes in the image
#       - detect_walls(): detect walls in the image
#     - **Forwards results to:** planning.py 
#     -  **Output:** path 
from constants import *
import utils
import numpy as np
import cv2
import matplotlib.pyplot as plt
class Map:
    def __init__(self, image):
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
        
        # cv2.imshow("Warped", warped)
        # cv2.waitKey(0)
        # print("Warped", warped.shape)

        cropped = warped[hcrop: hcrop+HEIGHT_IN_CELLS, wcrop:wcrop+WIDTH_IN_CELLS]
        
        # cv2.imshow("Cropped", cropped)
        # cv2.waitKey(0)
        # print("cropped: ", cropped.shape)

        self.map = np.zeros((HEIGHT_IN_CELLS, WIDTH_IN_CELLS))
        self.detect_holes(cropped)
        # self.detect_walls(np.copy(cropped))
        
   



        
    def detect_corners(self, img):


        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([155, 115, 165], dtype = "uint8") # 131, 49, 72
        upper = np.array([170, 180, 220], dtype = "uint8")

        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.blur(mask, (5,5))

        # cv2.imshow("Mask", mask)
        # cv2.waitKey(0)

        im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)[:4]

        print(len(contours))

        corners = np.zeros((4 ,2), dtype="float32")
        i = 0
        for c in contours:
            M = cv2.moments(c)
            if M["m00"] == 0: 
                continue
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            cv2.circle(img, (cX, cY), 5, (255, 255, 255), -1)
            cv2.putText(img, str(i), (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # cv2.imshow("Image", img)
            # cv2.waitKey(0)
            corners[i][0] = cX
            corners[i][1] = cY
            i += 1
        print("i: ",i)
        # cv2.imshow("Image", img)
        # cv2.waitKey(0)
        return corners # bottom-left, bottom-right, top-left, top-right


    def detect_walls(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("GRAY", img)
        # cv2.waitKey(0)

        img = cv2.blur(img, (5,5))

        low_threshold = 0
        high_threshold = 10
        
        img[img>20] = 255
        # cv2.imshow("Blurred", img)
        # cv2.waitKey(0)

        edges = cv2.Canny(img, low_threshold, high_threshold)

        cv2.imshow("Edges", edges)
        cv2.waitKey(0)


        rho = 1  # distance resolution in pixels of the Hough grid
        theta = np.pi / 180  # angular resolution in radians of the Hough grid
        threshold = 15  # minimum number of votes (intersections in Hough grid cell)
        min_line_length = 50  # minimum number of pixels making up a line
        max_line_gap = 20  # maximum gap in pixels between connectable line segments
        line_image = np.copy(img) * 0  # creating a blank to draw lines on

        # Run Hough on edge detected image
        # Output "lines" is an array containing endpoints of detected line segments
        lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)

        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)
        # Draw the lines on the  image
        lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)

        cv2.imshow("Blurred", lines_edges)
        cv2.waitKey(0)

    def detect_holes(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower = np.array([97, 204, 115], dtype = "uint8") # 131, 49, 72


        h = 203, 204, 198, 202, 214.3, 199.4, 202.5

        s = 89, 88, 100, 83, 96, 100, 88

        v = 48, 47, 64, 47, 63, 78, 68, 46

        # h = 195, 215
        # s = 80, 100
        # v = 45, 80

        upper = np.array([108, 255, 204], dtype = "uint8")

        mask = cv2.inRange(hsv, lower, upper)

        cv2.imshow("Mask", mask)
        cv2.waitKey(0)

        self.map[mask] = 2

        print("i: ",i)
        # cv2.imshow("Image", img)
        # cv2.waitKey(0)
        return holes # bottom-left, bottom-right, top-left, top-right

    
def main():
    img = cv2.imread("sample_frames/image1.png")
    # detect_corners(img)
    map = Map(img)

if __name__ == "__main__":
    main()


