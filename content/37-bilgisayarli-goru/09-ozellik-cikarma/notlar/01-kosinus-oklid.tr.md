İki vektör arasındaki yakınlık iki yolla ölçülür: **kosinüs benzerliği**
(yönler ne kadar aynı) ve **Öklid uzaklığı** (uçlar arası düz mesafe).

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

- `b`, `a`'nın iki katı: yönleri aynı (kosinüs 1) ama Öklid uzaklığı 5.
  `c` ise `a`'ya dik (kosinüs 0), uzaklığı daha büyük.
- Gömmelerde genellikle **yön** anlamlıdır, uzunluk değil (uzunluk çoğu
  zaman resmin parlaklığı gibi ilgisiz şeylerle büyür). Bu yüzden kosinüs
  tercih edilir.
- Vektörler önce birim uzunluğa getirilirse ikisi aynı sıralamayı verir:
  `uzaklık² = 2 − 2 · kosinüs`. Son satır bunu doğruluyor. Normalleştir,
  sonra hangisini istersen kullan.
