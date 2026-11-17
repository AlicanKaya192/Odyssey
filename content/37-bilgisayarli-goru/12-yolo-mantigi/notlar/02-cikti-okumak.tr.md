Hazır bir algılama kütüphanesinin sonucu genellikle tensörlerden oluşan bir
nesnedir. Onu kendi kodunun anladığı sade bir biçime (sözlük listesi)
çevirmek, sonraki her adımı (süzme, sayma, kaydetme) kolaylaştırır. Gerçek
kütüphaneyi çalıştırmadan aynı yapıyı taklit edelim:

```python
from types import SimpleNamespace

import torch

boxes = SimpleNamespace(
    xyxy=torch.tensor([[10.0, 10, 30, 60], [50, 20, 90, 45]]),
    conf=torch.tensor([0.91, 0.88]),
    cls=torch.tensor([0.0, 2.0]),
)
names = {0: "person", 2: "car"}
rows = []
for box, conf, cls in zip(boxes.xyxy.tolist(), boxes.conf.tolist(), boxes.cls.tolist()):
    rows.append({"name": names[int(cls)], "conf": round(conf, 2), "box": box})
for row in rows:
    print(row)
```

```text
{'name': 'person', 'conf': 0.91, 'box': [10.0, 10.0, 30.0, 60.0]}
{'name': 'car', 'conf': 0.88, 'box': [50.0, 20.0, 90.0, 45.0]}
```

- Sınıf numaraları ondalıklı sayı olarak gelebilir (`0.0`); sözlükte ad
  ararken `int(...)` gerekir.
- Kutular piksel koordinatı; resmi ağa vermeden önce küçültmüşsen kütüphane
  çoğu zaman koordinatları özgün resme geri çevirir. Kendi ön işlemeni
  yaptıysan bunu kendin yapmalısın (Nesne Algılamaya Giriş bölümünde kutuları
  ölçeklemek).

Ultralytics'in sonuç nesnesinde kutular `result.boxes` altında `xyxy`, `conf`
ve `cls` olarak durur; takip modunda bir de `id` gelir. Bu modülde kütüphaneyi
çalıştırmıyoruz; alan adlarını kullanmadan önce kurulu sürümün belgesine bak.
