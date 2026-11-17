Deney kaydında ayarlar ve tohum varsa ama veri yoksa, kayıt eksiktir: biri
CSV dosyasındaki bir satırı düzeltirse aynı kod, aynı tohumla farklı sonuç
verir ve kayıt bunu göstermez. Çözüm verinin bir **özetini** (karma, hash)
kaydetmek: verinin baytlarından hesaplanan, veri bir bayt bile değişince
değişen kısa bir metin.

```python
import hashlib
import numpy as np
from dl_data import make_table


def data_hash(array):
    return hashlib.sha256(np.ascontiguousarray(array).tobytes()).hexdigest()


a, _ = make_table(600, seed=7)
b, _ = make_table(600, seed=7)
c, _ = make_table(600, seed=8)
print(len(data_hash(a)), data_hash(a) == data_hash(b), data_hash(a) == data_hash(c))
changed = a.copy()
changed[0, 0] += 0.001
print(data_hash(a) == data_hash(changed))
```

```text
64 True False
False
```

- SHA-256 özeti 64 onaltılık karakter. Aynı veri aynı özeti, farklı tohumla
  üretilen veri farklı özeti veriyor.
- 600 × 6'lık tabloda tek bir sayıyı binde bir değiştirmek özeti tamamen
  değiştirdi.
- `np.ascontiguousarray`: baytların bellekteki sırası dizinin nasıl
  dilimlendiğine bağlı olabilir; önce düzenli bir kopyası alınır.

Kayda genellikle özetin ilk 12 karakteri yazılır (`data_hash(a)[:12]`);
karşılaştırma için yeter. Özet yalnızca **aynı baytları** tanır: aynı sayılar
`float64` ile kaydedilirse ya da sütunların sırası değişirse özet de değişir.
Bu bir özellik: model de o farkı görecektir.

Bir kaydın tam listesi kabaca şöyle: ayarlar, tohum, verinin özeti, kodun
git sürümü (`git rev-parse HEAD`), kütüphane sürümleri, sonuçlar, tarih.
Birkaç satırlık bir JSON, aylar sonra "bu sayı nereden çıktı" sorusunu
cevaplar.
