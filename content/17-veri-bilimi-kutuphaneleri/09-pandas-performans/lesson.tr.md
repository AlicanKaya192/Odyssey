# pandas Performansı

Aynı sonucu veren iki pandas kodu arasında yüzlerce kat hız farkı olabilir.
Fark neredeyse her zaman aynı yerden gelir: satır satır Python döngüsü mü,
yoksa bütün sütun üzerinde tek bir işlem mi? Bu bölüm o farkı ölçüyor,
döngüsüz koşul yazmayı, pandas 3'ün kopyala-yazarken (Copy-on-Write)
kuralını, bellek için tür seçmeyi ve okunaklı zincir yazımını anlatıyor. Çok
büyük dosyaları parça parça okumak **Büyük Veri** patikasının konusu.

## Döngü, apply ve vektörel işlem

```python
import time
import numpy as np
import pandas as pd

rng = np.random.default_rng(0)
df = pd.DataFrame({"price": rng.uniform(1, 100, 20_000),
                   "qty": rng.integers(1, 10, 20_000)})

start = time.perf_counter()
total = [row["price"] * row["qty"] for _, row in df.iterrows()]
t_iter = time.perf_counter() - start

start = time.perf_counter()
total2 = df.apply(lambda row: row["price"] * row["qty"], axis=1)
t_apply = time.perf_counter() - start

start = time.perf_counter()
total3 = df["price"] * df["qty"]
t_vec = time.perf_counter() - start

print(np.allclose(total, total3), np.allclose(total2, total3))
print(t_iter > 50 * t_vec, t_apply > 20 * t_vec)
```

```text
True True
True True
```

- Üç yol da aynı sonucu veriyor. Süreler bu bilgisayarda: `iterrows` yaklaşık
  0,2 saniye, `apply(axis=1)` yaklaşık 0,06 saniye, vektörel çarpım binde
  birin altında. Kesin sayı makineden makineye değişir; **yüzlerce katlık**
  oran değişmez.
- `iterrows` her satır için yeni bir Series nesnesi kurar; asıl maliyet bu.
- `apply(axis=1)` daha kısa yazılır ama içeride yine satır satır Python
  fonksiyonu çağırır. "pandas'ta yazdım, hızlıdır" yanılgısının kaynağı.
- `df["price"] * df["qty"]` işi NumPy'ye verir: döngü C'de döner. Kural: önce
  **sütunla** yazmayı dene.

## Koşul: np.where ve np.select

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({"qty": [1, 12, 5, 30], "price": [10.0, 8.0, 9.0, 7.5]})
df["size"] = np.where(df["qty"] >= 10, "bulk", "single")
rules = [df["qty"] >= 25, df["qty"] >= 10]
df["discount"] = np.select(rules, [0.2, 0.1], default=0.0)
df["total"] = df["qty"] * df["price"] * (1 - df["discount"])
print(df)
```

```text
   qty  price    size  discount  total
0    1   10.0  single       0.0   10.0
1   12    8.0    bulk       0.1   86.4
2    5    9.0  single       0.0   45.0
3   30    7.5    bulk       0.2  180.0
```

- `apply` ile yazılan "eğer şöyleyse şu" kodlarının çoğu döngüsüz yazılabilir.
- `np.where(koşul, doğruysa, yanlışsa)`: iki seçenek.
- `np.select(koşullar, değerler, default=...)`: ikiden fazla seçenek.
  Koşullar **sırayla** denenir, ilk tutan kazanır: 30 adet hem `>= 25` hem
  `>= 10`, ama `0.2` aldı. Bu yüzden en dar koşul önce yazılır.

## Copy-on-Write: zincirli atama işe yaramaz

```python
import warnings
import pandas as pd

df = pd.DataFrame({"city": ["Izmir", "Ankara", "Bursa"], "stock": [5, 0, 3]})
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    df[df["stock"] == 0]["stock"] = 10
print(df["stock"].tolist(), type(caught[0].message).__name__)
part = df[df["stock"] > 0]
part["stock"] = 99
print(df["stock"].tolist(), part["stock"].tolist())
df.loc[df["stock"] == 0, "stock"] = 10
print(df["stock"].tolist())
```

```text
[5, 0, 3] ChainedAssignmentError
[5, 0, 3] [99, 99]
[5, 10, 3]
```

- pandas 3'te **Copy-on-Write** geçerli: bir tablodan türetilen her tablo
  (filtre, sütun seçimi) davranış olarak **ayrı bir kopyadır**. Gerçek kopya
  ancak biri değiştirilince yapılır; o yüzden adı "yazarken kopyala".
- `df[filtre]["stock"] = 10` iki adımdır: önce filtre yeni bir tablo üretir,
  atama o tabloya gider. `df` değişmez; pandas `ChainedAssignmentError`
  uyarısı verir.
- `part = df[...]` sonra `part[...] = 99`: yalnızca `part` değişir, `df`
  olduğu gibi kalır. Eski pandas'taki `SettingWithCopyWarning` karmaşası
  bitti; kural basit.
- Asıl tabloyu değiştirmek için **tek adımda** `df.loc[satır_koşulu, "sütun"] =
  değer`.

## Bellek için tür seçmek

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(1)
n = 1_000_000
df = pd.DataFrame({
    "store": rng.choice(["Izmir", "Ankara", "Bursa"], n),
    "qty": rng.integers(0, 100, n),
    "price": rng.uniform(1, 50, n),
})
before = df.memory_usage(deep=True).sum() / 1e6
small = df.assign(store=df["store"].astype("category"),
                  qty=pd.to_numeric(df["qty"], downcast="unsigned"),
                  price=df["price"].astype("float32"))
after = small.memory_usage(deep=True).sum() / 1e6
print(small.dtypes.astype(str).tolist())
print(round(before, 1), round(after, 1))
print(abs(small["price"].sum() - df["price"].sum()) / df["price"].sum() < 1e-6)
```

```text
['category', 'uint8', 'float32']
29.3 6.0
True
```

- Varsayılanlar cömerttir: tam sayı `int64` (8 bayt), ondalık `float64`.
  0–99 arası bir adet için 1 bayt (`uint8`) yeter.
- `pd.to_numeric(..., downcast="unsigned")` değerlere bakıp sığan en küçük
  türü seçer. Üç farklı mağaza adı `category` ile kodlanır.
- Bir milyon satırda 29,3 MB 6,0 MB'a indi. Daha küçük tablo daha hızlı da
  işlenir: belleğe sığmayan iş sığar hâle gelir.
- `float32` yaklaşık 7 basamak kesinlik tutar; toplamdaki göreli fark
  milyonda birin altında kaldı. Para hesabı gibi kuruşun önemli olduğu yerde
  `float64` kalır.

## query ve zincir yazım

```python
import pandas as pd

df = pd.DataFrame({"city": ["Izmir", "Ankara", "Bursa", "Izmir"],
                   "qty": [5, 12, 3, 20], "price": [10.0, 8.0, 9.0, 7.5]})
limit = 4
a = df[(df["qty"] > limit) & (df["city"] == "Izmir")]
b = df.query("qty > @limit and city == 'Izmir'")
print(a.equals(b), b.index.tolist())
result = (
    df.assign(total=lambda d: d["qty"] * d["price"])
      .query("total > 40")
      .groupby("city")["total"].sum()
      .sort_values(ascending=False)
)
print(result.to_dict())
```

```text
True [0, 3]
{'Izmir': 200.0, 'Ankara': 96.0}
```

- `query` filtreyi metin olarak yazar: parantez ve `&` kalabalığı yerine
  `and`. Python değişkeni `@` ile çağrılır. Sonuç köşeli parantezli filtreyle
  birebir aynı.
- `assign(total=lambda d: ...)` yeni sütunu **zincirin içinde** ekler; `d`
  o adımdaki tablo. Ara değişken (`df2`, `df3`) gerekmez ve asıl `df`
  değişmez.
- Parantez içindeki zincir her adımı ayrı satırda okutur: "toplam ekle →
  40'tan büyükleri al → şehre göre topla → sırala". Hata ayıklarken bir
  satırı yoruma almak yeter.

## Özet

- Önce sütunla yaz; `iterrows` ve `apply(axis=1)` satır satır Python'dur ve
  yüzlerce kat yavaştır.
- Koşullar `np.where` (iki seçenek) ve `np.select` (çok seçenek, ilk tutan
  kazanır).
- pandas 3: türetilen tablo ayrı kopya gibi davranır. Değiştirmek için tek
  adımda `df.loc[koşul, sütun] = değer`.
- `downcast`, `category`, `float32` belleği küçültür; kesinliği unutma.
- `query` ve `assign` ile zincir: okunaklı, ara değişkensiz.
