import os
from collections import namedtuple
import argparse

from PIL import Image
import pytesseract
import cv2


Box = namedtuple("Box", "l t r b")


def extract_boxes(image_path, config=r''):
    " Probably returns one box per character, not text as an entire line. "

    result = pytesseract.image_to_boxes(
            Image.open(image_path),
            output_type=pytesseract.Output.DICT
            )
    print(result)

    # Parse out bounding boxes of characters
    # Inspired by https://stackoverflow.com/a/49941471/2096369
    boxes = []
    for i in range(len(result['char'])):
        boxes.append(Box(
                int(result['left'][i]),
                int(result['top'][i]),
                int(result['right'][i]),
                int(result['bottom'][i]),
            ))

    return boxes


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="extract bounding boxes of all characters")
    parser.add_argument("input_image")
    parser.add_argument("--output", help="optional file to output with bounding boxes annotated")
    args = parser.parse_args()

    boxes = extract_boxes(args.input_image)
    if not boxes:
        print("No boxes found")
        raise SystemExit

    print("Boxes found:")
    print(boxes)

    if args.output:
        # Inspired by https://stackoverflow.com/a/49941471/2096369
        img = cv2.imread(args.input_image)
        h, w, _ = img.shape
        for b in boxes:
            img = cv2.rectangle(img, (b.l, h - b.t), (b.r, h - b.b), (255, 0, 0), 2)
        cv2.imwrite(args.output, img)
        print("Boxes printed on image at", args.output)

