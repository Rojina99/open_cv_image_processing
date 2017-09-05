import cv2
import os

import sys
dir_path, current_file = os.path.split(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(dir_path)

from src.utils import center


class ShapeDetector:
    """
    class that detects and print corresponding shape
    """
    def detect(self, c):
        # initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        if len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            cent = center(c)
            # area = cv2.contourArea(c)
            area = w*h

            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
            return shape,area,w,h

        else:
            import math
            shape = "circle"
            new_e = cv2.fitEllipse(approx)
            # print("Fit Ellipse Output", new_e)
            if abs(new_e[1][0]-new_e[1][1])<=5:
                new_e = cv2.minEnclosingCircle(approx)
                cent = center(c)
                # area = cv2.contourArea(c)
                radius = new_e[1]
                area = math.pi*math.pow(new_e[1],2)
                return shape,cent,area,radius
            else:
                shape = "ellipse"
                cent = center(c)
                # area = cv2.contourArea(c)
                major_axis = new_e[1][0]
                minor_axis = new_e[1][1]
                area = math.pi*major_axis/2*minor_axis/2
                # cent = new_e[0]
                return shape,cent,area,major_axis/2,minor_axis/2

    def print_shape_parameters(self, shape):
        shap = shape[0]
        if shap=="rectangle" or shap=="square":
            print("Shape: %s \n Area: %s \n Width: %s \n Height: %s"
                  %(shape[0], shape[1], shape[2], shape[3]))
        elif shap=="circle":
            print("Shape:%s \n Center: %s \n Area: %s \n Radius: %s"
                  %(shape[0], shape[1], shape[2], shape[3]))
        elif shap=="ellipse":
            print("Shape:%s \n Center: %s \n Area: %s \n Major Axis: %s \n Minor Axis: %s"
                  %(shape[0], shape[1], shape[2], shape[3], shape[4]))
