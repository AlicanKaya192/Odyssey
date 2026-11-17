import torch
from torchvision.ops import box_iou


def best_matches(predicted, truth):
    matrix = box_iou(torch.tensor(predicted, dtype=torch.float32), torch.tensor(truth, dtype=torch.float32))
    values, indices = matrix.max(dim=1)
    result = []
    for value, index in zip(values.tolist(), indices.tolist()):
        result.append([index if value > 0 else -1, round(value, 2)])
    return result

truth = [[10, 10, 20, 20], [0, 0, 6, 6]]
predicted = [[11, 10, 21, 20], [1, 1, 6, 7], [25, 25, 30, 30]]
for row in best_matches(predicted, truth):
    print(row)
