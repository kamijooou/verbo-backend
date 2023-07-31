from raven import Client
import numpy as np
import cv2
from loguru import logger
from .src import yolo, extract_images, read_text, clean_bubbles, insert_bubbles

from src.core.celery_app import celery_app
from src.core.config import settings


@celery_app.task()
def run_clean() -> str:
    path: str = "K:/PyProj/verbo-clean/test_images/10.jpg"
    results = yolo(path)
    original_bubbles, cut_bubbles = extract_images(path, results[0])

    # text_list = read_text(cut_bubbles)
    # logger.debug(f'Text of bubbles: {text_list}')

    new_bubbles = clean_bubbles(original_bubbles)

    new_image_path = insert_bubbles(path, results[0].boxes, new_bubbles)
    logger.debug(f'Cleaned image was saved to: {new_image_path}')

# celery -A src.clean_module.worker:celery_app worker --loglevel=INFO --pool=solo