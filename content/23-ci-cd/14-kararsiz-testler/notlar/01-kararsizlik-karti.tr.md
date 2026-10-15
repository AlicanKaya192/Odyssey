**Neden önemli?**

Her biri %98 geçen `n` kararsız testle hattın yeşil olma olasılığı
`0.98 ** n`: 1 testte %98, 5 testte %90, 20 testte %67.

**Kaynak, belirti, düzeltme**

| Kaynak | Belirti | Düzeltme |
|---|---|---|
| Sıra bağımlılığı | Tek başına geçiyor, birlikte düşüyor | Fixture ile her test kendi verisi |
| Zaman | Hafta sonu, ay sonu, gece yarısı düşüyor | Saati parametre olarak ver |
| Rastgelelik | Her seferinde başka değer | `random.Random(42)` |
| Küme sırası | Bilgisayardan bilgisayara değişiyor | `sorted(...)` ya da küme karşılaştır |
| Bekleme | Yavaş makinede düşüyor | Koşulu bekle (sınırlı deneme) |
| Ağ | İnternet yavaşken düşüyor | Sahte sunucu, kayıtlı cevap |
| Ondalık sayı | `0.1 + 0.2 == 0.3` yanlış | `pytest.approx` |

**Düzeltme kalıpları**

```python
import random
from datetime import datetime


def pick(items, rng):
    return rng.choice(items)


def is_weekend(now=None):
    now = now or datetime.now()
    return now.weekday() >= 5


print(pick(["a", "b", "c"], random.Random(42)))
print(is_weekend(datetime(2026, 10, 17)))
print(sorted({"web", "api", "db"}))
```

- Rastgele üreteci de saati de fonksiyon **dışarıdan alır**; testte sabit
  değer verilir.
- Kümeyi listeye çevirip sırasına güvenmek yerine `sorted`.

**Kararsız testi bulmak**

- Aynı commit'te hem geçip hem düşen test kararsızdır.
- Şüpheli testi tek başına ve dosyanın tamamıyla çalıştır; sonuçlar
  farklıysa sıra bağımlılığı.
- Seyrek düşen testi yakalamak için çok çalıştırma gerekir: %2 düşen bir
  testi %95 olasılıkla en az bir kez düşmüş görmek için 149 çalıştırma.
