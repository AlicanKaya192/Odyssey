import torch
from torchvision.ops import box_iou


def count_tp_fp_fn(pred_boxes, pred_scores, truth_boxes, threshold):
    ious = box_iou(torch.tensor(pred_boxes, dtype=torch.float32),
                   torch.tensor(truth_boxes, dtype=torch.float32))
    order = sorted(range(len(pred_scores)), key=lambda i: pred_scores[i], reverse=True)
    used = set()
    tp = 0
    for i in order:
        free = [(ious[i, j].item(), j) for j in range(len(truth_boxes)) if j not in used]
        best_iou, best_j = max(free, default=(0.0, -1))
        if best_iou >= threshold:
            used.add(best_j)
            tp += 1
    return [tp, len(pred_boxes) - tp, len(truth_boxes) - tp]

truth = [[10, 10, 20, 20], [30, 30, 40, 40], [50, 5, 60, 15]]
boxes = [[10, 10, 20, 20], [11, 11, 21, 21], [9, 10, 19, 21], [30, 30, 40, 40], [31, 29, 41, 39]]
print(count_tp_fp_fn(boxes, [0.9, 0.8, 0.7, 0.85, 0.6], truth, 0.5))
print(count_tp_fp_fn([boxes[0], boxes[3]], [0.9, 0.85], truth, 0.5))
