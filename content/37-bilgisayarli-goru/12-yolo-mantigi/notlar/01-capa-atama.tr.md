Çapalı bir YOLO'da her hücrede birkaç çapa var; bir nesneyi hangi çapa
öğrenecek? Genellikle **şekli en çok benzeyen**: nesnenin genişlik ve
yüksekliği ile çapanınki arasında, iki kutu aynı merkeze konmuş gibi
hesaplanan IoU.

```python
import torch

anchors = torch.tensor([[8.0, 8.0], [8.0, 16.0], [16.0, 8.0]])
objects = torch.tensor([[7.0, 15.0], [14.0, 9.0], [9.0, 9.0]])


def shape_iou(a, b):
    inter = torch.minimum(a[:, None], b[None]).prod(dim=2)
    union = a.prod(dim=1)[:, None] + b.prod(dim=1)[None] - inter
    return inter / union


iou = shape_iou(objects, anchors)
print([[round(v, 2) for v in row] for row in iou.tolist()])
print(iou.argmax(dim=1).tolist())
```

```text
[[0.5, 0.82, 0.32], [0.51, 0.4, 0.79], [0.79, 0.53, 0.53]]
[1, 2, 0]
```

- Uzun ve dar nesne (7 × 15) dik çapaya (8 × 16), geniş ve alçak nesne
  (14 × 9) yatık çapaya (16 × 8), kareye yakın nesne (9 × 9) kare çapaya
  (8 × 8) gidiyor.
- `torch.minimum(a[:, None], b[None])` yayınlama ile her nesne–çapa çifti
  için ortak genişliği ve yüksekliği buluyor; aynı merkezde ortak alan
  bunların çarpımı.
- Çapaların boyları çoğu zaman eğitim verisindeki kutuların genişlik ve
  yüksekliklerinin kümelenmesiyle (k-means) seçilir.

Aynı hücreye düşen iki nesne farklı çapalara giderse ikisi de öğrenilebilir;
çapanın bir faydası da bu.
