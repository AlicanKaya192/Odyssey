import torch


def predict_all(weight, rows):
    with torch.inference_mode():
        logits = torch.tensor(rows) @ torch.tensor(weight).T
        return logits.argmax(dim=1).tolist()

weight = [[1.0, 0.0], [0.0, 1.0], [-1.0, -1.0]]
print(predict_all(weight, [[2.0, 1.0], [0.0, 3.0], [-2.0, -1.0]]))
