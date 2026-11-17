import numpy as np
import torch


def prepare(rows, labels):
    x = torch.from_numpy(np.array(rows))
    y = torch.tensor(labels)
    return [str(x.dtype), str(y.dtype), list(x.shape)]

print(prepare([[0.5, 1.0], [2.0, 4.0], [1.5, 0.0]], [0, 1, 1]))
