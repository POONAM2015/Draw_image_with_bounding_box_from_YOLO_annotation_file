import os, glob
import cv2
from typing import List
import sys

print(os.getcwd())

def write_image(image: List[float], image_dest_path: str) -> None:
    """
    takes the image and writes to the destination path
    :param image: numpy array of image
    :param image_dest_path: destination path of image where it is to be written
    """
    cv2.imwrite(image_dest_path, image)


def show_image_annotation(image: List[float], bboxes: List[List[float]]) -> List[float]:
    """
    draws bounding boxes on the image and returns the image with bounding box on it
    :param image: numpy array of the image
    :param bboxes: List[List[float]] -- list of bounding boxes
    :return: numpy array of image with bounding boxes drawn on it
    """
    dh, dw, _ = image.shape
    
    for dt in bboxes:
        x, y, w, h = dt
        l = int((x - w / 2) * dw)
        r = int((x + w / 2) * dw)
        t = int((y - h / 2) * dh)
        b = int((y + h / 2) * dh)
        
        if l < 0:
            l = 0
        if r > dw - 1:
            r = dw - 1
        if t < 0:
            t = 0
        if b > dh - 1:
            b = dh - 1

        cv2.rectangle(image, (l, t), (r, b), (0, 0, 255), 1)
    return image


def bounding_box_class_labels(image_path: str, label_path: str) -> List[float]:
    """
    extracts details of all bounding boxes from the label path and returns its list
    :param image_path: str, is the path of image
    :param label_path: str, is the path of label (annotation)
    :return: List[List[float]] which is the list of all bounding boxes,
    where, each bounding box is a list of [x, y, w, h] in the normalised form as is in the yolo format
    """
    img = cv2.imread(image_path)
    dh, dw, _ = img.shape

    fl = open(label_path, 'r')
    data = fl.readlines()
    fl.close()

    bounding_boxes = []

    for dt in data:
        _, x, y, w, h = map(float, dt.split(' '))
        bounding_boxes.append([x,y,w,h])
    
    return bounding_boxes


def make_image_with_bb(image_path: str, label_path: str, image_dest_path: str) -> None:
    """
    creates bounding boxes on the image and writes it to the destination path
    :param image_path: str, is the path of the image without bounding boxes on it (from source)
    :param label_path: str, is the path of the label(annotation) (from source)
    :param image_dest_path: str, is the destination path of the image with bb (to destination)
    """
    image = cv2.imread(image_path)
    bounding_boxes = bounding_box_class_labels(image_path, label_path)
    image_with_bb = show_image_annotation(image, bounding_boxes)
    write_image(image_with_bb, image_dest_path)


def main(SRC, DEST):
    for image_path in glob.glob(os.path.join(SRC, '*.*g')):
        # print(image_path)
        basename, image_ext = image_path.split('\\')[-1].split('.')
        label_path = os.path.join(SRC, basename + '.txt')
        image_dest_path = os.path.join(DEST, 'bb_' + basename + '.' + image_ext)
        # print(basename, '\n', label_path, '\n', image_dest_path)
        try:
            make_image_with_bb(image_path, label_path, image_dest_path)
        except Exception:
            print(image_path)


if __name__ == '__main__':
    # main(SRC, DEST)
    print(sys.argv)
    if len(sys.argv) == 1:
        main(r'source_folder', r'destination_folder')
    elif len(sys.argv) == 2:
        os.mkdir('_destination_folder')
        main(sys.argv[1], r'_destination_folder')
    else:
        main(sys.argv[1], sys.argv[2])
