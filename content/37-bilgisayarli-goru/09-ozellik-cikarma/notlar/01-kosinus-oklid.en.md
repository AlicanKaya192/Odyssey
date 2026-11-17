Closeness between two vectors is measured in two ways: **cosine similarity**
(how much the directions agree) and **Euclidean distance** (the straight
distance between the tips).

```python
import torch
import torch.nn.functional as F

a = torch.tensor([3.0, 4.0])
b = torch.tensor([6.0, 8.0])
c = torch.tensor([4.0, -3.0])
cos_ab = F.cosine_similarity(a, b, dim=0).item()
cos_ac = F.cosine_similarity(a, c, dim=0).item()
print(round(cos_ab, 3), round(cos_ac, 3))
print(round(torch.dist(a, b).item(), 3), round(torch.dist(a, c).item(), 3))
ua, uc = F.normalize(a, dim=0), F.normalize(c, dim=0)
print(round(torch.dist(ua, uc).item() ** 2, 3), round(2 - 2 * (ua @ uc).item(), 3))
```

```text
1.0 0.0
5.0 7.071
2.0 2.0
```

- `b` is twice `a`: same direction (cosine 1) but a Euclidean distance of 5.
  `c` is at a right angle to `a` (cosine 0), and its distance is larger.
- In embeddings the **direction** usually carries the meaning, not the length
  (the length often grows with irrelevant things such as the picture's
  brightness). That is why cosine is preferred.
- If the vectors are first brought to unit length, the two give the same
  ranking: `distance² = 2 − 2 · cosine`. The last line confirms it. Normalise,
  then use whichever you like.
