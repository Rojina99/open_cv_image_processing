import numpy as np
import cv2
import os

import sys

dir_path, current_file = os.path.split(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(dir_path)

from src.utils import center


class convex_Hull():
    """
    class that returns the convex hull of countors in nearby format
    """

    def find_if_close(self, cnt1, cnt2):
        '''
        :return: true if two contours falls within same distance range i.e 20
        '''

        def distance(x, y):
            return np.sqrt(np.sum((x - y) ** 2))

        row1, row2 = cnt1.shape[0], cnt2.shape[0]
        # print("Shape",row1,row2)
        for i in range(row1):
            for j in range(row2):
                # dist = np.linalg.norm(cnt1[i]-cnt2[j])
                dist = distance(cnt1[i], cnt2[j])
                if abs(dist) < 20:
                    return True
                elif i == row1 - 1 and j == row2 - 1:
                    return False

    def contours_status(self, contours):
        '''
        :return: array of contours index within same distance
        '''
        LENG = len(contours)
        status = np.zeros((LENG, 1))
        for i, cnt1 in enumerate(contours):
            x = i
            if i != LENG - 1:
                for j, cnt2 in enumerate(contours[i + 1:]):
                    # print(cnt2)
                    # print("\n")
                    x = x + 1
                    dist = self.find_if_close(cnt1, cnt2)
                    if dist == True:
                        val = min(status[i], status[x])
                        status[x] = status[i] = val
                    else:
                        if status[x] == status[i]:
                            status[x] = i + 1
        return status

    def contour_array(self, status):
        '''
        :return: array of contours within same distance
        '''
        maximum = int(status.max()) + 1
        contour_list = []
        for i in range(maximum):
            pos = np.where(status == i)[0]
            if pos is not None:
                for j in pos:
                    contour_list.append(j)
        contour_list = np.array(contour_list, dtype=np.int32)
        return contour_list

    def convex_hull(self, contour_list, contours):
        '''
        :param contour_list: rearranged contour list according to distance
        :param contours: contours
        :return: convex hull of given counters
        '''
        contour_op = []
        for i in contour_list:
            # print(contours[i])
            cent = center(contours[i])
            contour_op.append([cent])
        cont = np.vstack([contour_op])
        hull = cv2.convexHull(cont)
        return hull
