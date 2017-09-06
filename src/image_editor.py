import numpy as np
import cv2
import argparse
import os

import sys
dir_path, current_file = os.path.split(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(dir_path)


from src.detect_shape import ShapeDetector
from src.utils import load_image, hsv_mask, find_contours, draw_contours, filter_image, save_image
from src.utils import contour_avg_area
from src.convex_hull import convex_Hull

major, minor, _ = cv2.__version__.split(".")
# print major, minor

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--data_path', type=str, default=dir_path+'/data/images/inputs/green_circle.jpg',
                        help='data path for specific image')
    parser.add_argument('--save_dir', type=str, default=None,
                        help='directory to save output  images')
    parser.add_argument('--save_image', type=str, default='/image.jpg',
                        help='image name to be saved')

    args = parser.parse_args()
    image_edit(args)

def image_edit(args):
    image_path = args.data_path
    # args.save_dir = "D:/Pycharm PRoject/open_cv/data/save/images"

    ch = convex_Hull()
    sd = ShapeDetector()
    unified = []

    image = load_image(image_path)
    blurred = filter_image(image)
    mask = hsv_mask(blurred)
    contours = find_contours(mask)
    status = ch.contours_status(contours)
    contour_list = ch.contour_array(status)
    hull = ch.convex_hull(contour_list, contours)

    unified.append(hull)
    unified = np.array(unified, dtype=np.int32)

    shape = sd.detect(hull)
    sd.print_shape_parameters(shape)
    # print("Shape", shape)

    area = contour_avg_area(contours)
    if area>=15:
        width = 5
    elif area<15:
        width = 1
    draw_contours(image, unified, width=width)
    if args.save_dir is not None:
        if not os.path.exists(args.save_dir):
            print("The directory: %s doesnot exist,........ making directory: %s" %(args.save_dir, args.save_dir))
            os.makedirs(args.save_dir)
        save_image(image, args.save_dir+"/"+args.save_image,unified, width=width)

if __name__=='__main__':
    main()










