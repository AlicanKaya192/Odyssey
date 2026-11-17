Dolgu bedava değil: her dolgu konumu ağda gerçek bir kelime gibi hesaplanır
ve sonra maskeyle atılır. Uzunlukları çok farklı dizileri rastgele
gruplarsak bir grupta 3 kelimelik bir cümle 29 kelimelik bir cümlenin boyuna
doldurulur. Dizileri **uzunluğa göre sıralayıp** gruplamak bu boşa giden
hesabı azaltır.

```python
import numpy as np

rng = np.random.default_rng(0)
lengths = rng.integers(3, 30, 64).tolist()


def padding(lengths, size):
    total = 0
    for i in range(0, len(lengths), size):
        group = lengths[i:i + size]
        total += max(group) * len(group) - sum(group)
    return total


print(sum(lengths))
print(padding(lengths, 8), padding(sorted(lengths), 8))
```

```text
1042
654 78
```

64 dizide toplam 1042 gerçek kelime var. Geldiği sırayla
gruplanınca 654 dolgu konumu hesaplanıyor; sıralı gruplarda
yalnızca 78. Eğitimde her epoch'ta grupların sırası yine
karıştırılır; yalnızca bir grubun içindekiler benzer uzunlukta seçilir
(uzunluğa göre kovalama, bucketing).

## Dolgusuz bir yol: `nn.EmbeddingBag`

Yalnızca dizinin gömmelerinin ortalamasını istiyorsan dolguya hiç gerek
yok. `nn.EmbeddingBag` bütün kimlikleri tek uzun listede alır;
`offsets` her dizinin nerede başladığını söyler.

```python
import torch
from torch import nn

torch.manual_seed(0)
bag = nn.EmbeddingBag(10, 4, mode="mean")
ids = torch.tensor([3, 5, 7, 2, 2])
offsets = torch.tensor([0, 3])
out = bag(ids, offsets)
print(out.shape)
print(torch.allclose(out[0], bag.weight[[3, 5, 7]].mean(dim=0)))
```

```text
torch.Size([2, 4])
True
```

İki dizi var: `[3, 5, 7]` ve `[2, 2]`. Sonuç her dizi için bir vektör;
ilki üç satırın ortalamasının aynısı. Kelime sırası önemli değilse (kelime
torbası modelleri) maskeli ortalamanın kısa ve hızlı yolu budur. Sıranın
önemli olduğu ağlar (LSTM, Transformer) ise dolgulu `(B, T, D)` tensörü
ister.
