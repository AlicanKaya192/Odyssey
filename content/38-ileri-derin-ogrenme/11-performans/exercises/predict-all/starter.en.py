import torch


def predict_all(weight, rows):
    # Not row by row, with one product: logits = rows . W^T, then argmax
    w = torch.tensor(weight)
    preds = []
    for row in rows:
        preds.append(int((torch.tensor(row) @ w.T).argmax()))
    return preds

weight = [[1.0, 0.0], [0.0, 1.0], [-1.0, -1.0]]
print(predict_all(weight, [[2.0, 1.0], [0.0, 3.0], [-2.0, -1.0]]))
