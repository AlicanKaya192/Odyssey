Benzerliğin ikinci yaygın kullanımı **yinelenen** (duplicate) belgeleri
bulmak: aynı talebi iki kez gönderen müşteri, aynı ürünün iki ilanı.
300 talebin her birini her biriyle karşılaştıralım:

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from text_data import make_tickets

texts = [t["text"] for t in make_tickets(300)]
X = TfidfVectorizer().fit_transform(texts)
S = (X @ X.T).toarray()
np.fill_diagonal(S, 0)
i, j = np.unravel_index(S.argmax(), S.shape)
print(round(float(S[i, j]), 3))
print(texts[i][:60])
print(texts[j][:60])
pairs = int((np.triu(S) > 0.8).sum())
print(pairs)
```

```text
1.0
The app does not load my order history.
The app does not load my order history.
35
```

- `np.fill_diagonal(S, 0)` her belgenin kendisiyle benzerliğini (1) siliyor;
  yoksa en büyük değer hep köşegen olurdu.
- `np.unravel_index` düz dizideki en büyük değerin yerini (satır, sütun)
  çiftine çeviriyor.
- En benzer çift birebir aynı metin: benzerlik 1. `np.triu` tablonun üst
  üçgenini alıyor (her çift bir kez sayılsın); 0,8'in üstünde **35 çift**
  var.

## Sınır ve ölçek

- **Eşik** (0,8 gibi) göreve göre seçilir: düşük eşik farklı talepleri de
  yineleme sanar, yüksek eşik yalnızca birebir kopyaları bulur. Birkaç
  çifte elle bakarak seç.
- Her belgeyi her belgeyle karşılaştırmak **n²** iş: 300 talep 90 bin
  karşılaştırma, 1 milyon talep 10¹² karşılaştırma. Büyük derlemde
  yinelenenleri bulmak için MinHash gibi yaklaşık yöntemler gerekir; 13.
  bölümün konusu.
