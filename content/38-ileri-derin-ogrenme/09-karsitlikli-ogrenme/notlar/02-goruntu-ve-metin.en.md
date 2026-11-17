The same loss is also used to put two **different kinds** of data into the
same space. In image–text matching models an image encoder and a text encoder
are trained together: a photo and its caption are a positive pair, the other
captions in the batch are negatives. This time the similarity table is built
with images as rows and texts as columns, and the loss is taken in both
directions.

```python
import torch
import torch.nn.functional as F


def pair_loss(img, txt, tau=0.1):
    img, txt = F.normalize(img, dim=1), F.normalize(txt, dim=1)
    logits = img @ txt.T / tau
    target = torch.arange(len(img))
    return (F.cross_entropy(logits, target) + F.cross_entropy(logits.T, target)) / 2


gen = torch.Generator().manual_seed(0)
img = torch.randn(6, 16, generator=gen)
txt = img + 0.3 * torch.randn(6, 16, generator=gen)
print(pair_loss(img, txt).item() < pair_loss(img, txt.roll(1, dims=0)).item())
logits = F.normalize(img, dim=1) @ F.normalize(txt, dim=1).T
print(logits.argmax(dim=1).tolist())
```

```text
True
[0, 1, 2, 3, 4, 5]
```

- `logits` is `(6, 6)`: rows are images, columns are texts. `cross_entropy`
  along the rows asks "which caption belongs to this image", along the
  columns (`logits.T`) "which image belongs to this caption".
- The loss of correctly matched pairs is smaller than that of pairs whose
  texts were shifted by one (`roll`).
- Every image's most similar text is its own caption: `[0, 1, 2, 3, 4, 5]`.

Once this arrangement is trained, **classification without labels**
(zero-shot) becomes possible: compare an image with the vectors of texts
such as "a square", "a circle", "a triangle" and pick the most similar. The
classes may never have been seen in training, as long as they can be
described in text.
