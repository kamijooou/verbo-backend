import cv2
from PIL import Image


def insert_bubbles(image_path, bound_boxes, bubbles_list):
    image = cv2.imread(image_path)
    insert_pairs = zip(bound_boxes, bubbles_list)

    for box, bubble in insert_pairs:
        box = box.xyxy
        image[int(box[0][1]):int(box[0][3]), int(box[0][0]):int(box[0][2])] = bubble

    # cv2.imwrite('K:/PyProj/verbo-clean/result/page.png', image)
    img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    img.save("K:/PyProj/verbo-clean/result/page.png")
    return 'result/page.png'
