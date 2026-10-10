`groupby` hızlıdır, ama yalnızca hesabı pandas'ın **kendi** fonksiyonlarına
bıraktığında. İçine bir `lambda` yazınca her grup için ayrı bir Python
çağrısı yapılır; grup sayısı arttıkça fark büyür.

```python
import time
import numpy as np
import pandas as pd

rng = np.random.default_rng(2)
df = pd.DataFrame({"store": rng.integers(0, 50_000, 500_000),
                   "sales": rng.uniform(0, 100, 500_000)})

start = time.perf_counter()
fast = df.groupby("store")["sales"].sum()
t_fast = time.perf_counter() - start
start = time.perf_counter()
slow = df.groupby("store")["sales"].agg(lambda s: s.sum())
t_slow = time.perf_counter() - start
print(len(fast), np.allclose(fast, slow), t_slow > 10 * t_fast)

totals = df.groupby("store")["sales"].transform("sum")
share = df["sales"] / totals
per_store = share.groupby(df["store"]).sum()
print(len(share) == len(df), round(float(per_store.mean()), 6))
```

```text
49998 True True
True 1.0
```

## Ne ölçüldü?

- Yarım milyon satır, yaklaşık 50 000 mağaza (çıktıda 49 998). `sum()` ile
  `agg(lambda s: s.sum())` aynı sonucu veriyor; ama `lambda` her mağaza için
  ayrı bir Python çağrısı demek. Bu bilgisayarda fark otuz katın üstünde ve
  grup sayısıyla büyüyor (5 000 mağazada birkaç kattı).
- Hesabı ad olarak ver: `"sum"`, `"mean"`, `"max"`, `"count"`, `"std"`,
  `"nunique"`, `"first"`. Bunlar içeride C'de çalışır.

## transform: grup sonucunu satırlara geri yay

- "Her satışın mağaza toplamındaki payı" için iki adım akla gelir: grup
  toplamını hesapla, sonra satırlarla birleştir (`merge`).
- `transform("sum")` bunu tek adımda yapar: sonuç **satır sayısı kadar**
  uzundur, her satıra kendi grubunun toplamı yazılır. Payların grup içindeki
  toplamı 1 çıktı.
- Grup ortalamasından sapma (`df["sales"] - g.transform("mean")`), grup
  içinde sıra (`g.rank()`), grup içinde eksik doldurma
  (`g.transform("mean")` ile `fillna`) hep aynı kalıp.

## Ne zaman lambda kaçınılmaz?

Hesap gerçekten özelse (iki sütundan özel bir oran, karmaşık bir kural)
`apply` / `lambda` kalabilir. Önce şunu dene: hesabı sütunlara böl
(`assign` ile ara sütun), sonra hazır toplama fonksiyonunu kullan. Çoğu
"özel" hesap bu şekilde ikiye ayrılır.
