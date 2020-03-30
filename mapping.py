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
import constants
import utils
import numpy as np
import cv2
# class Map:
#     def __init__(self, image):
#         image_corners = detect_corners(image)

#         warped_corners = np.array(
#             [
#                 [0 ,0],
#                 [HEIGHT_IN_CELLS, 0],
#                 [HEIGHT_IN_CELLS, WIDTH_IN_CELLS],
#                 [0, WIDTH_IN_CELLS]
#             ]
#         )
#         homography = fit_homography(image_corners, map_corners)
#         warped_image = apply_homography(image, homography)
#         self.map = np.zeros((HEIGHT_IN_CELLS, WIDTH_IN_CELLS))
#         self.detect_walls(warped_image)
#         self.detect_holes(warped_image)
        
   



#     def fit_homography(image_corners, map_corners):
#         pass
    
#     def apply_homography(image, homography):
#         pass

def detect_corners(img):
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv_image)

    th, threshed = cv2.threshold(s, 100, 255, cv2.THRESH_OTSU|cv2.THRESH_BINARY)
    print("saving result")
    cv2.imwrite("result.png", threshed)
    print("saved")
    

def main():
    print("in main")
    img = cv2.imread("test_image.png")
    detect_corners(img)

if __name__ == "__main__":
    main()


