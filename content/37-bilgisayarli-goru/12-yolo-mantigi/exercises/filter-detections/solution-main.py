import torch
from torchvision.ops import nms


def filter_detections(xyxy, conf, cls, wanted, min_conf, iou):
    boxes = torch.tensor(xyxy, dtype=torch.float32)
    scores = torch.tensor(conf)
    keep = (torch.tensor(cls) == wanted) & (scores >= min_conf)
    boxes, scores = boxes[keep], scores[keep]
    return boxes[nms(boxes, scores, iou)].tolist()

xyxy = [[10, 10, 30, 60], [12, 11, 31, 62], [50, 20, 90, 45], [100, 5, 120, 55]]
conf = [0.91, 0.62, 0.88, 0.35]
cls = [0, 0, 2, 0]
for wanted, min_conf in ((0, 0.5), (0, 0.3), (2, 0.5)):
    kept = filter_detections(xyxy, conf, cls, wanted, min_conf, 0.5)
    print(wanted, min_conf, len(kept))
    for box in kept:
        print(box)
