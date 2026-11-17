Sıradan bir ağda kayıp düştükçe sevinirsin. GAN'da öyle değil: iki ağın
kaybı birbirinin tersine çekiyor ve iyi giden bir eğitimde ikisi de sıfıra
gitmiyor, bir **denge** değerinin çevresinde salınıyor. O değeri bilmek,
kayıp eğrisini okumayı sağlar.

## Dengede kayıplar

Dengede ayırt edici her örneğe 0,5 der. Logit olarak bu 0'dır (`sigmoid(0)
= 0,5`). O zaman iki kaybı tam hesaplayabiliriz:

```python
import math
import torch
from torch import nn

loss_fn = nn.BCEWithLogitsLoss()
half = torch.zeros(64, 1)
ones, zeros = torch.ones(64, 1), torch.zeros(64, 1)
d_loss = loss_fn(half, ones) + loss_fn(half, zeros)
g_loss = loss_fn(half, ones)
print(round(d_loss.item(), 3), round(g_loss.item(), 3))
print(round(2 * math.log(2), 3), round(math.log(2), 3))
```

```text
1.386 0.693
1.386 0.693
```

- Ayırt edicinin kaybı iki terimin toplamı, dengede `2 · ln 2 ≈ 1,386`;
  üreticininki `ln 2 ≈ 0,693`.
- Eğitim boyunca kayıplar bu değerlerin çevresinde dolaşıyorsa oyun
  sürüyor demektir.

## Kötü işaretler

- **Ayırt edicinin kaybı sıfıra iniyor:** ayırt edici kazandı. Sahtelere
  çok emin biçimde "0" diyor; üreticinin kaybı büyüyor ama türevi işe yarar
  bir yön göstermiyor. Çoğu zaman ayırt edici üreticiden çok hızlı öğreniyor
  demektir (öğrenme oranını küçült, ayırt ediciyi küçült).
- **Üreticinin kaybı sıfıra iniyor:** üretici ayırt ediciyi tek bir hileyle
  kandırıyor olabilir; örneklere bakmadan iyi sanma. Sonraki not bunun en
  bilinen hâlini anlatıyor.

## Etiket yumuşatma

Ayırt edicinin aşırı emin olmasını önlemenin basit bir yolu, gerçek
örneklere 1 yerine 0,9 hedefi vermektir (label smoothing). Çok emin bir
ayırt ediciyi (logit 6, olasılık ≈ 0,998) iki hedefle karşılaştıralım:

```python
sure = torch.full((64, 1), 6.0)
print(round(loss_fn(sure, ones).item(), 3))
print(round(loss_fn(sure, torch.full((64, 1), 0.9)).item(), 3))
```

```text
0.002
0.602
```

Hedef 1 iken aşırı güven neredeyse hiç cezalanmıyor; hedef 0,9 iken kayıp
belirgin biçimde büyüyor ve ayırt edici kendinden bu kadar emin olmamaya
itiliyor. Yalnızca gerçek örneklerin hedefi yumuşatılır; sahtelerinki 0
kalır.
