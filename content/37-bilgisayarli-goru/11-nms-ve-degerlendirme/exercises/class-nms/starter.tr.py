import torch
from torchvision.ops import batched_nms


def class_nms(boxes, scores, labels, conf, iou):
    return []

boxes = [[10, 10, 20, 20], [11, 11, 21, 21], [9, 10, 19, 21], [30, 30, 40, 40], [31, 29, 41, 39]]
scores = [0.9, 0.8, 0.7, 0.85, 0.6]
labels = [0, 0, 1, 1, 1]
print(class_nms(boxes, scores, labels, 0.65, 0.5))
print(class_nms(boxes, scores, labels, 0.5, 0.5))
