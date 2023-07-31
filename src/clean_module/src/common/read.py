import cv2
from loguru import logger
from PIL import Image

from manga_ocr import MangaOcr


def draw(img):
    cv2.imshow('Bubble', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# TODO: fix the outer symbols problem
def read_text(images) -> list:
    mocr = MangaOcr()
    texts = []

    i = 1
    for image in images:
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)

        text = mocr(im_pil)
        texts.append(text)

        with open(f'bubble-text/output{i}.txt', 'w+', encoding='utf-8') as file:
            file.write(text)

        # draw(image)
        i += 1


    return texts
