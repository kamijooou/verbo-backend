import cv2
import torch
import numpy as np
from torchvision.transforms import Resize


def _pre_process_mask(mask, size):
    mask = Resize(size=size, antialias=True)(mask)
    mask = mask.flip(dims=[0])
    mask = mask.permute(1, 2, 0).contiguous()
    mask = mask * 255
    return mask


def _crop(img, mask, bbox, size):
    mask = _pre_process_mask(mask, size)
    mask = mask[int(bbox[0][1]):int(bbox[0][3]), int(bbox[0][0]):int(bbox[0][2])]
    mask = mask.cpu().numpy()
    mask = mask.astype(np.int8)
###################################
    cropped = cv2.bitwise_and(img, img, mask=mask)
    # cv2.imwrite('kek.png', cropped)
###################################
    return cropped


def extract_images(path, results) -> tuple[list, list]:
    image = cv2.imread(path)
    result_pairs = zip(results.boxes, results.masks)

    original_bubbles = []
    cut_bubbles = []
    for box, mask in result_pairs:
        box = box.xyxy
        original = image[int(box[0][1]):int(box[0][3]), int(box[0][0]):int(box[0][2])]
        original_bubbles.append(original)

        cut = _crop(original.copy(), mask.data, box, image.shape[:2])
        cut_bubbles.append(cut)

    return original_bubbles, cut_bubbles
