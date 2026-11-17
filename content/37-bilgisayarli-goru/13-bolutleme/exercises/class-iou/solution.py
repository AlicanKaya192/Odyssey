import torch


def class_iou(predicted, truth, num_classes):
    p = torch.tensor(predicted)
    t = torch.tensor(truth)
    result = []
    for c in range(num_classes):
        union = ((p == c) | (t == c)).sum().item()
        if union == 0:
            result.append(-1)
            continue
        common = ((p == c) & (t == c)).sum().item()
        result.append(round(common / union, 3))
    return result

truth = [[0, 0, 1, 1], [0, 0, 1, 1], [2, 2, 0, 0], [2, 2, 0, 0]]
predicted = [[0, 0, 1, 1], [0, 1, 1, 1], [2, 0, 0, 0], [0, 0, 0, 0]]
print(class_iou(predicted, truth, 3))
print(class_iou(predicted, truth, 4))
