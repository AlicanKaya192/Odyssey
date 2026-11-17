# Contrastive Learning

Labels are expensive; unlabelled images are plentiful. In **self-supervised
learning** the label is derived from the data itself. The autoencoder was one
example: the target is the input itself. **Contrastive learning** takes
another route: it trains an encoder so that two differently corrupted
versions of the same image (two **views**) land close together and those of
different images far apart. No label is used; still, the encoder learns
things like "a shifted square is still a square".

<figure class="fig">
<div class="flow">
<span class="node">image</span><span class="arrow">→</span>
<span class="node">two views</span><span class="arrow">→</span>
<span class="node acc">encoder</span><span class="arrow">→</span>
<span class="node">two vectors</span><span class="arrow">→</span>
<span class="node ok">make them close</span>
</div>
<figcaption>Two views of the same image are a positive pair; every other view in the batch is a negative. The loss pulls the positives together and pushes the negatives apart.</figcaption>
</figure>

## The data and two views

`make_shapes` gives circle, square and triangle images. We use the labels
only at the very end, to measure what the encoder has learned. One view:
shift the image by up to 2 pixels, flip it horizontally with probability one
half, change the brightness and add noise.

```python
import torch
import torch.nn.functional as F
from torch import nn
from dl_data import make_shapes

x_np, y_np = make_shapes(600, seed=7)
x, y = torch.tensor(x_np), torch.tensor(y_np)
x_train, y_train, x_test, y_test = x[:500], y[:500], x[500:], y[500:]


def augment(batch, gen):
    n = len(batch)
    shifts = torch.randint(-2, 3, (n, 2), generator=gen)
    out = torch.stack([torch.roll(img, (int(a), int(b)), dims=(1, 2))
                       for img, (a, b) in zip(batch, shifts)])
    flip = torch.rand(n, generator=gen) < 0.5
    out[flip] = out[flip].flip(-1)
    out = out * (0.7 + 0.6 * torch.rand(n, 1, 1, 1, generator=gen))
    return (out + 0.1 * torch.randn(out.shape, generator=gen)).clamp(0, 1)


gen = torch.Generator().manual_seed(1)
v1, v2 = augment(x_train[:8], gen), augment(x_train[:8], gen)
print(v1.shape, bool((v1 != v2).any()))
```

```text
torch.Size([8, 1, 16, 16]) True
```

- Two separate groups of views came from the same 8 images; they differ.
- Which corruptions you choose decides what the encoder becomes
  **insensitive** to. Here we want it insensitive to position, direction and
  brightness; the shape information survives in every view.

## The loss: InfoNCE / NT-Xent

The batch has `n` images, two views of each: `2n` vectors. For every vector
the question is: among the other `2n − 1` vectors, can it find **its own
partner**? This is a classification problem: the similarities are the
logits, the correct class is the partner's position. The loss is called
InfoNCE; when the similarity is the cosine divided by a **temperature**
(`tau`) it is NT-Xent (normalised temperature-scaled cross-entropy).

```python
def nt_xent(z1, z2, tau=0.1):
    z = F.normalize(torch.cat([z1, z2]), dim=1)
    sim = z @ z.T / tau
    sim.fill_diagonal_(float("-inf"))
    n = len(z1)
    target = torch.cat([torch.arange(n, 2 * n), torch.arange(0, n)])
    return F.cross_entropy(sim, target)


eye = torch.eye(4)
print(round(nt_xent(eye, eye, tau=0.2).item(), 3))
same = torch.ones(4, 4)
collapsed = nt_xent(same, same, tau=0.2).item()
print(round(collapsed, 3), round(torch.log(torch.tensor(7.0)).item(), 3))
```

```text
0.04
1.946 1.946
```

- `F.normalize` brings every vector to unit length; `z @ z.T` is now a table
  of cosine similarities.
- `fill_diagonal_(-inf)`: a vector's similarity with itself is always the
  largest; we remove it from the candidates.
- `target`: the partner of `i` in the first half is `n + i`, the partner of
  one in the second half is `i`.
- **The perfect case** (`eye`): every partner is identical, the others are
  orthogonal; the loss is close to zero.
- **Collapse** (`same`): every vector is the same. The partner cannot be told
  from the others; the loss is `log(2n − 1) = log 7`. Unlike an autoencoder,
  giving everything the same vector **does not pay off** here: the negatives
  forbid it.

## Training without labels

```python
torch.manual_seed(0)
encoder = nn.Sequential(nn.Conv2d(1, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
                        nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(),
                        nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(32, 16))


def knn_accuracy(enc, queries):
    with torch.no_grad():
        a = F.normalize(enc(x_train), dim=1)
        b = F.normalize(enc(queries), dim=1)
    return (y_train[(b @ a.T).argmax(dim=1)] == y_test).float().mean().item()


queries = augment(x_test, torch.Generator().manual_seed(6))
before = knn_accuracy(encoder, queries)
opt = torch.optim.Adam(encoder.parameters(), lr=0.003)
gen = torch.Generator().manual_seed(1)
for epoch in range(20):
    perm = torch.randperm(500, generator=gen)
    for i in range(0, 500, 100):
        xb = x_train[perm[i:i + 100]]
        loss = nt_xent(encoder(augment(xb, gen)), encoder(augment(xb, gen)))
        opt.zero_grad()
        loss.backward()
        opt.step()
after = knn_accuracy(encoder, queries)
print(round(before, 1), after > before + 0.15)
```

```text
0.5 True
```

- `y_train` never appears in the loop: the encoder was trained only with the
  information "these two views come from the same image".
- The measure is **nearest-neighbour accuracy**: turn a corrupted view of a
  test image into a vector, find the most similar training image, and count
  its label as the prediction. The labels are used only here.
- With a random encoder the accuracy is about 0.5; after training without
  labels it is clearly higher (above 0.8 on this computer). The encoder
  learned, without seeing a label, that a shifted or flipped shape is the
  same shape.

In real use this pretraining is done with millions of unlabelled images;
afterwards the encoder becomes a ready feature extractor for fine-tuning with
few labels or for a linear classifier (similar to feature extraction in the
Computer Vision module).

## Summary

- Contrastive learning: two views of the same example close, those of
  different examples far apart.
- NT-Xent: the similarity table of normalised vectors / `tau`, diagonal
  `-inf`, target the partner's position, `cross_entropy`.
- Negatives prevent collapse: the same vector for everything costs
  `log(2n − 1)`.
- Whatever corruptions you choose, the encoder becomes insensitive to them.
- Labels only in evaluation (nearest-neighbour accuracy).
