import argparse
import numpy as np
import cv2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('image')
    parser.add_argument('annotation')

    return parser.parse_args()


def main():
    args = parse_args()
    image = cv2.imread(args.image)

    with open(args.annotation) as f:
        content = f.readlines()
        content = [line.strip().split(',')for line in content]
        content = [[c[(i * 9):(i * 9 + 9)] for i in range(0, len(c) // 9)] for c in content]
        annotation = []
        for text in content:
            text_annotation = {}
            text_annotation['segm'] = [float(x) for x in text[0][:-1]]
            text_annotation['text'] = text[0][-1]
            text_annotation['chars'] = []
            for character in text[1:]:
                text_annotation['chars'].append({})
                text_annotation['chars'][-1]['segm'] = [float(x) for x in character[:-1]]
                text_annotation['chars'][-1]['char'] = character[-1]
            annotation.append(text_annotation)

        for ann in annotation:
            contours = np.array([int(round(x)) for x in ann['segm']])
            contours = np.array([contours.reshape(-1, 2)])
            cv2.drawContours(image, contours, -1, (255, 255, 255), 1)
            for character in ann['chars']:
                contours = np.array([int(round(x)) for x in character['segm']])
                contours = np.array([contours.reshape(-1, 2)])
                cv2.drawContours(image, contours, -1, (255, 255, 255), 1)
    cv2.imshow('image', image)
    cv2.waitKey(0)

if __name__ == '__main__':
    main()
