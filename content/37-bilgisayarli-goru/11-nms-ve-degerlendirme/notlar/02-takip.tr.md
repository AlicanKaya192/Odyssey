Videoda bir kişiyi kareden kareye **takip** etmek (aynı kişiye hep aynı
numarayı vermek) de bir eşleştirme problemi: bu karedeki kutuları önceki
karedekilerle eşleştir. Burada her kutu en fazla bir kez eşleşmeli ve toplam
en iyi olmalı: Macar algoritmasının tam işi.

```python
import torch
from scipy.optimize import linear_sum_assignment
from torchvision.ops import box_iou

previous = {7: [10.0, 10, 20, 30], 8: [40, 12, 50, 32]}
current = torch.tensor([[42.0, 13, 52, 33], [12, 11, 22, 31], [70, 10, 80, 30]])
ids = list(previous)
ious = box_iou(current, torch.tensor(list(previous.values())))
rows, cols = linear_sum_assignment(-ious.numpy())
next_id = max(ids) + 1
assigned = {}
for r, c in zip(rows, cols):
    if ious[r, c] >= 0.3:
        assigned[int(r)] = ids[c]
for r in range(len(current)):
    if r not in assigned:
        assigned[r] = next_id
        next_id += 1
print([assigned[r] for r in range(len(current))])
```

```text
[8, 7, 9]
```

- Bu karedeki ilk kutu önceki karedeki 8 numaralı kişiye, ikincisi 7'ye
  yakın: numaralar korunuyor (sıra değişse bile).
- Üçüncü kutu hiçbir eski kutuyla örtüşmüyor: yeni bir kişi, yeni numara
  (9).
- Takipte eşik genellikle algılamadakinden düşüktür (burada 0,3): kişi iki
  kare arasında biraz yer değiştiriyor.

Gerçek takip sistemleri buna hareket tahmini (kişinin bir sonraki karede
nerede olacağı) ve görünüş benzerliği (önceki bölümdeki gömmeler) ekler;
eşleştirmenin kalbi yine aynı atama problemidir.
