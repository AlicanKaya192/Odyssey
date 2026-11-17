Aynı kayıp iki **farklı tür** veriyi aynı uzaya koymak için de kullanılır.
Görüntü–metin eşleştirme modellerinde bir görüntü kodlayıcısı ve bir metin
kodlayıcısı birlikte eğitilir: bir fotoğraf ile onun açıklaması pozitif
çift, gruptaki öbür açıklamalar negatif. Bu kez benzerlik tablosu
görüntülerin satırları ve metinlerin sütunlarıyla kurulur ve kayıp iki
yönde alınır.

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

- `logits` `(6, 6)`: satır görüntü, sütun metin. Satır boyunca
  `cross_entropy` "bu görüntünün açıklaması hangisi", sütun boyunca
  (`logits.T`) "bu açıklamanın görüntüsü hangisi" sorusu.
- Doğru eşleşmiş çiftlerin kaybı, metinleri bir kaydırılmış (`roll`)
  çiftlerinkinden küçük.
- Her görüntünün en benzer metni kendi açıklaması: `[0, 1, 2, 3, 4, 5]`.

Bu düzen eğitildikten sonra **etiketsiz sınıflandırma** (zero-shot) mümkün
olur: bir görüntüyü "bir kare", "bir daire", "bir üçgen" gibi metinlerin
vektörleriyle karşılaştırıp en benzerini seçmek. Sınıflar eğitimde hiç
görülmemiş olabilir; yeter ki metinle anlatılabilsin.
