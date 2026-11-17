import torch


def batch_of_one(image):
    t = torch.tensor(image)
    t = t.unsqueeze(0).unsqueeze(0)
    return list(t.shape)

image = [[0.0, 1.0, 0.0], [1.0, 1.0, 1.0]]
print(batch_of_one(image))
