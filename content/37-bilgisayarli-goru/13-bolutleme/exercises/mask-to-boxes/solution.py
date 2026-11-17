import torch


def mask_boxes(mask):
    m = torch.tensor(mask)
    result = []
    for c in range(1, int(m.max().item()) + 1):
        ys, xs = torch.nonzero(m == c, as_tuple=True)
        if len(xs) == 0:
            continue
        x1, y1 = xs.min().item(), ys.min().item()
        x2, y2 = xs.max().item() + 1, ys.max().item() + 1
        result.append([x1, y1, x2, y2, c])
    return result

mask = [[0, 0, 0, 0, 0],
        [0, 2, 2, 0, 0],
        [0, 2, 2, 0, 3],
        [1, 0, 0, 0, 3],
        [0, 0, 0, 0, 0]]
for box in mask_boxes(mask):
    print(box)
