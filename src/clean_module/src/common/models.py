from collections import OrderedDict
import torch
from ultralytics import YOLO
from loguru import logger


try:
    yolo = YOLO('src/clean_module/src/core/yolov8.pt')
    logger.info('Extracting YOLO-model was successful')
except Exception as exc:
    logger.error(exc)
    exit()
