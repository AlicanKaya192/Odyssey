import torch


def mean_iou(predicted, truth, num_classes):
    p = torch.tensor(predicted)
    t = torch.tensor(truth)
    scores = []
    for c in range(num_classes):
        union = ((p == c) | (t == c)).sum().item()
        if union == 0:
            continue
        scores.append(((p == c) & (t == c)).sum().item() / union)
    return round(sum(scores) / len(scores), 3)

truth = [[0, 0, 1], [0, 1, 1], [2, 2, 0]]
predicted = [[0, 0, 1], [0, 0, 1], [2, 0, 0]]
print(mean_iou(predicted, truth, 3))
print(mean_iou(predicted, truth, 5))
