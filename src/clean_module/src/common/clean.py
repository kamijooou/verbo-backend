import math
import cv2
import numpy as np
from PIL import Image

import easyocr
reader = easyocr.Reader(['ja', 'en'])

from .utils import border_std_deviation


def _midpoint(x1, y1, x2, y2):
    x_mid = int((x1 + x2) / 2)
    y_mid = int((y1 + y2) / 2)
    return x_mid, y_mid


def _clean(image, bboxes):
    mask = np.zeros(image.shape[:2], dtype="uint8")

    for box in bboxes:
        x0, y0 = box[0], box[2]
        x1, y1 = box[1], box[2]
        x2, y2 = box[1], box[3]
        x3, y3 = box[0], box[3]
###################################
        mask = np.zeros(image.shape[:2], dtype="uint8")
        x_mid0, y_mid0 = _midpoint(x1, y1, x2, y2)
        x_mid1, y_mi1 = _midpoint(x0, y0, x3, y3)

        # For the line thickness, we will calculate the length of the line between
        # the top-left corner and the bottom-left corner.
        thickness = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))

        # Define the line and inpaint
        cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mi1), 255,
                 thickness)
####################################        
        _, median_value = border_std_deviation(
            Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)),
            Image.fromarray(cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)),
        )

        print(median_value)
        if median_value == None:
            color = (255, 255, 255)

        color = (median_value, median_value, median_value)
        image = cv2.rectangle(image, (x0, y0), (x2, y2), color, -1)

    # cv2.imshow('img', image)
    # cv2.waitKey(0)

    return image


def clean_bubbles(bubbles_list):
    new_bubbles = []

    for bubble in bubbles_list:
        bboxes = reader.detect(bubble)[0][0]
        bubble = _clean(bubble, bboxes)
        new_bubbles.append(bubble)

    return new_bubbles
