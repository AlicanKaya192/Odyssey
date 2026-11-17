import torch
import torch.nn.functional as F


def cosine_matrix(vectors):
    unit = F.normalize(torch.tensor(vectors), dim=1)
    return [[round(v, 3) for v in row] for row in (unit @ unit.T).tolist()]

for row in cosine_matrix([[1.0, 0.0], [1.0, 1.0], [0.0, 2.0]]):
    print(row)
