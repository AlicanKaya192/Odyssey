import torch


def anchor_match(objects, anchors):
    a = torch.tensor(objects, dtype=torch.float32)
    b = torch.tensor(anchors, dtype=torch.float32)
    inter = torch.minimum(a[:, None], b[None]).prod(dim=2)
    union = a.prod(dim=1)[:, None] + b.prod(dim=1)[None] - inter
    return (inter / union).argmax(dim=1).tolist()

anchors = [[8, 8], [8, 16], [16, 8]]
print(anchor_match([[6, 14], [15, 7], [10, 10], [4, 4]], anchors))
