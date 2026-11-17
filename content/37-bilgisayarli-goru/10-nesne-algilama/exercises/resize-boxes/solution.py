import torch
from torchvision.ops import clip_boxes_to_image


def resize_boxes(boxes, old_size, new_size):
    b = torch.tensor(boxes, dtype=torch.float32) * (new_size / old_size)
    return clip_boxes_to_image(b, (new_size, new_size)).tolist()

boxes = [[4, 6, 14, 12], [25, 20, 31, 30]]
for size in (64, 16):
    for box in resize_boxes(boxes, 32, size):
        print(size, box)
