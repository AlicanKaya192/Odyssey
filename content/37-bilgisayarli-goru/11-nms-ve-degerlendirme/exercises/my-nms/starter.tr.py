import torch
from torchvision.ops import box_iou


def my_nms(boxes, scores, threshold):
    return []

boxes = [[10, 10, 20, 20], [11, 11, 21, 21], [9, 10, 19, 21], [30, 30, 40, 40], [31, 29, 41, 39]]
print(my_nms(boxes, [0.9, 0.8, 0.7, 0.85, 0.6], 0.5))
print(my_nms(boxes, [0.5, 0.8, 0.7, 0.85, 0.9], 0.5))
print(my_nms(boxes, [0.9, 0.8, 0.7, 0.85, 0.6], 0.7))
