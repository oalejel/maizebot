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
        image_corners = detect_corners(image)
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
        
        cv2.imshow("Warped", warped)
        cv2.waitKey(0)
        print("Warped", warped.shape)

        cropped = warped[hcrop: hcrop+HEIGHT_IN_CELLS, wcrop:wcrop+WIDTH_IN_CELLS]
        
        cv2.imshow("Cropped", cropped)
        cv2.waitKey(0)
        print("cropped: ", cropped.shape)

        # self.map = np.zeros((HEIGHT_IN_CELLS, WIDTH_IN_CELLS))
        # self.detect_walls(warped_image)
        # self.detect_holes(warped_image)
        
   



    def fit_homography(image_corners, map_corners):
        pass
    
    def apply_homography(image, homography):
        pass


    
def detect_corners(img):

    # create NumPy arrays from the boundaries
    lower = np.array([100, 60, 150], dtype = "uint8") # 131, 49, 72
    upper = np.array([170, 100, 200], dtype = "uint8") # 169, 87, 145

    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(img, lower, upper)
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
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    return corners # bottom-left, bottom-right, top-left, top-right

    
def main():
    img = cv2.imread("test_image.png")
    # detect_corners(img)
    map = Map(img)

if __name__ == "__main__":
    main()


