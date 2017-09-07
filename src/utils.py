import numpy as np
import cv2
import os

import sys

dir_path, current_file = os.path.split(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(dir_path)

major, minor, _ = cv2.__version__.split(".")

"""
Helper functions to save, process and retrieve image
"""


def load_image(path):
    img = cv2.imread(path, 4)
    return img


def filter_image(image):
    blurred = cv2.pyrMeanShiftFiltering(image, 31, 51)
    return blurred


def hsv_mask(image, color="Yellow"):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([25, 50, 50])
    upper_yellow = np.array([32, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    return mask


def find_contours(mask):
    ret, threshold = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # print threshold
    if major is "3":
        _, contours, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        return contours
    elif major is "2":
        contours, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        # print contours
        return contours


def center(contours):
    M = cv2.moments(contours)
    cX = int(M['m10'] / M['m00'])
    cY = int(M['m01'] / M['m00'])
    return [cX, cY]


def draw_contours(image, contours, width=2):
    cv2.drawContours(image, contours, -1, (0, 255, 0), width)
    cv2.imshow("Conts", cv2.resize(image, (960, 540)))
    cv2.waitKey(0)
    # cv2.destroyAllWindows()


def save_image(image, path, contours=None, width=3):
    if contours is not None:
        cv2.drawContours(image, contours, -1, (0, 255, 0), width)
    cv2.imwrite(path, image)


def contour_avg_area(contours):
    area = [cv2.contourArea(cnt) for cnt in contours]
    length = len(area)
    area_sum = 0
    for a in area:
        area_sum += a
    area_avg = area_sum / length
    return area_avg


def contour_avg_perimeter(contours):
    perimeter = [cv2.arcLength(cnt, closed=True) for cnt in contours]
    length = len(perimeter)
    peri_sum = 0
    for a in perimeter:
        peri_sum += a
    peri_avg = peri_sum / length
    return peri_avg
