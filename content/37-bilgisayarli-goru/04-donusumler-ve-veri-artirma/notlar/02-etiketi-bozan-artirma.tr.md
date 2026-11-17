Bir artırma ancak resmin **etiketini değiştirmiyorsa** işe yarar. Rakamlarda
180 derece döndürmek bunu bozar: bir 6, ters çevrilince 9'a benzer. Bunu
basit bir sınıflandırıcıyla ölçelim: her rakamın ortalama resmini çıkarıp
her resmi en yakın ortalamanın sınıfına koyuyoruz.

```python
import torch
from sklearn.datasets import load_digits

digits = load_digits()
x = torch.tensor(digits.images, dtype=torch.float32)
y = torch.tensor(digits.target)
means = torch.stack([x[y == d].mean(dim=0) for d in range(10)])


def nearest(images):
    distances = ((images[:, None] - means[None]) ** 2).sum(dim=(2, 3))
    return distances.argmin(dim=1)


sixes = x[y == 6]
print(len(sixes))
print(torch.bincount(nearest(sixes), minlength=10).tolist())
turned = torch.rot90(sixes, k=2, dims=(1, 2))
print(torch.bincount(nearest(turned), minlength=10).tolist())
```

```text
181
[1, 4, 0, 0, 0, 0, 175, 0, 1, 0]
[0, 16, 1, 6, 2, 2, 0, 4, 2, 148]
```

- 181 tane 6'nın 175'i doğru sınıfa (6) gidiyor.
- Aynı resimler 180 derece döndürülünce 148'i 9 sınıfına gidiyor; hiçbiri
  6'da kalmıyor. "Döndürülmüş 6" etiketiyle eğitmek ağa yanlış bir şey
  öğretirdi.

Hangi artırma güvenli, işe ve veriye göre değişir:

| Veri | Güvenli | Etiketi bozabilir |
|---|---|---|
| Rakam, harf | Küçük kaydırma, küçük döndürme | Aynalama, 180° döndürme (6 ↔ 9, b ↔ d) |
| Bu modüldeki şekiller | Yatay aynalama, kaydırma | Dikey aynalama (üçgen ters döner) |
| Doğal fotoğraf (kedi, köpek) | Yatay aynalama, kırpma, renk oynatma | Dikey aynalama (ters köpek gerçekte yok) |
| Nesne algılama | Kutuyla birlikte uygulanan dönüşümler | Kutuyu güncellemeden kırpmak |

Kural: artırılmış resme bakıp "bu hâlâ aynı etiketi hak ediyor mu?" diye sor.
