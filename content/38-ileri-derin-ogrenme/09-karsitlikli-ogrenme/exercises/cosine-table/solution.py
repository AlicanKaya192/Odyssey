import torch
import torch.nn.functional as F


def cosine_table(vectors):
    z = F.normalize(torch.tensor(vectors), dim=1)
    return [[round(v, 2) for v in row] for row in (z @ z.T).tolist()]

print(cosine_table([[1.0, 0.0], [1.0, 1.0]]))
