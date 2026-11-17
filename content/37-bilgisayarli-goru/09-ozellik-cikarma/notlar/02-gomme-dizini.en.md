In image search, each picture's embedding is computed once and stored; during
a search only the query picture's embedding is computed. A simple index:

```python
import torch
import torch.nn.functional as F

torch.manual_seed(0)
vectors = F.normalize(torch.randn(1000, 64), dim=1)
names = [f"img{i}.png" for i in range(1000)]
torch.save({"vectors": vectors, "names": names}, "index.pt")

index = torch.load("index.pt", weights_only=True)
query = index["vectors"][42] + 0.01 * torch.randn(64)
scores = index["vectors"] @ F.normalize(query, dim=0)
best = scores.topk(3).indices.tolist()
print(best[0], index["names"][best[0]])
print(index["vectors"].shape, len(best))
```

```text
42 img42.png
torch.Size([1000, 64]) 3
```

- Here the embeddings are random; in practice they come from the network's
  body. The query is a slightly damaged copy of picture 42: the nearest
  result is 42.
- `weights_only=True` also reads plain types such as dictionaries, lists and
  strings.
- A thousand pictures need one matrix product. With millions of pictures
  looking at every vector gets slow; at that scale special libraries that
  search for **approximate nearest neighbours** and vector databases are used.
  The idea is the same: the largest cosine between normalised embeddings.
- If the network changes (is retrained), the old embeddings become invalid;
  the index is recomputed.
