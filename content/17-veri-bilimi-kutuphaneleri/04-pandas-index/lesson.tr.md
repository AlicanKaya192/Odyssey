# pandas Index ve MultiIndex

Bir DataFrame'in satırlarının solundaki etiketler sıradan bir sütun değil,
**Index** adında ayrı bir nesne. Satır bulmayı hızlandırır, iki tabloyu
yan yana getirirken eşleştirmeyi yapar ve yanlış anlaşıldığında sessiz
hatalara yol açar: iki seriyi toplayınca `NaN` çıkması, aynı etiketin iki
kez geçmesi, sıralanmamış çok düzeyli indekste dilimin hata vermesi. Bu
bölüm Index'in nasıl çalıştığını ve birden fazla düzeyli **MultiIndex**'i
anlatıyor.

## Hizalama: pandas etiketle toplar

```python
import pandas as pd

jan = pd.Series({"Ankara": 120, "Izmir": 80, "Bursa": 50})
feb = pd.Series({"Izmir": 90, "Ankara": 100, "Konya": 40})
print(jan + feb)
print(jan.add(feb, fill_value=0).to_dict())
print((jan.values + feb.values).tolist())
```

```text
Ankara    220.0
Bursa       NaN
Izmir     170.0
Konya       NaN
dtype: float64
{'Ankara': 220.0, 'Bursa': 50.0, 'Izmir': 170.0, 'Konya': 40.0}
[210, 180, 90]
```

- `jan + feb` elemanları **sırayla** değil **etiketle** eşleştirir: Ankara
  Ankara'yla, İzmir İzmir'le. Buna **hizalama** (alignment) denir.
- Bir tarafta olmayan etiket (Bursa yalnızca ocakta, Konya yalnızca şubatta)
  `NaN` olur; tam sayılar da bu yüzden `float64`'e döner.
- Eksik tarafı 0 saymak isteniyorsa `add(..., fill_value=0)`. Aynı
  parametre `sub`, `mul`, `div` için de var.
- `.values` ile NumPy dizisine inince etiket kaybolur ve toplama **sırayla**
  yapılır: 210 aslında Ankara + İzmir. Hata vermez; sessizce yanlıştır.

## set_index, loc ve iloc

```python
import pandas as pd

df = pd.DataFrame({"code": ["A7", "B2", "C9"], "city": ["Izmir", "Ankara", "Bursa"],
                   "stock": [14, 3, 8]})
items = df.set_index("code")
print(items.index)
print(items.loc["B2", "stock"], items.iloc[1, 1])
print(items.loc[["C9", "A7"], "city"].tolist())
print(items.reset_index().columns.tolist())
```

```text
Index(['A7', 'B2', 'C9'], dtype='str', name='code')
3 3
['Bursa', 'Izmir']
['code', 'city', 'stock']
```

- `set_index("code")` bir sütunu indekse taşır; sütunlardan çıkar. Index'in
  bir adı (`name='code'`) ve türü var (pandas 3'te metin `str`).
- `loc` **etiketle**, `iloc` **konumla** seçer. `items.iloc[1, 1]` ikinci
  satır, ikinci sütun: `code` artık sütun olmadığı için ikinci sütun `stock`.
- `loc`'a liste verilirse satırlar o sırayla gelir.
- `reset_index()` indeksi geri sütun yapar; satırlara yeniden 0, 1, 2 verir.

## Tekrarlanan etiketler

```python
import pandas as pd

raw = pd.DataFrame({"day": ["mon", "tue", "mon"], "amount": [10, 20, 30]})
sales = raw.set_index("day")
print(sales.index.is_unique, sales.index.duplicated().tolist())
one, two = sales.loc["tue", "amount"], sales.loc["mon", "amount"]
print(type(one).__name__, two.tolist())
try:
    sales.reindex(["mon", "tue", "wed"])
except ValueError as error:
    print("ValueError:", error)
print(sales.groupby(level="day")["amount"].sum().to_dict())
```

```text
False [False, False, True]
int64 [10, 30]
ValueError: cannot reindex on an axis with duplicate labels
{'mon': 40, 'tue': 20}
```

- Index **benzersiz olmak zorunda değil**. `is_unique` ve `duplicated()`
  bunu denetler.
- Tehlike şu: tek etiketle `loc` bazen **tek değer** (`tue` → `int64`),
  bazen **seri** (`mon` → iki satır) döndürür. Kod bir gün tek değer
  beklerken öteki gün seri alır.
- `reindex` tekrarlı etikette çalışmaz. Çözüm çoğunlukla tekrarları
  birleştirmektir: `groupby(level="day").sum()`.
- Benzersiz olması gereken bir anahtarda `set_index(..., verify_integrity=True)`
  tekrar varsa hemen hata verir.

## MultiIndex: iki düzeyli etiket

```python
import pandas as pd

df = pd.DataFrame({
    "city": ["Izmir", "Izmir", "Ankara", "Ankara", "Bursa", "Bursa"],
    "year": [2024, 2025, 2024, 2025, 2024, 2025],
    "sales": [80, 95, 120, 110, 50, 65],
})
m = df.set_index(["city", "year"]).sort_index()
print(m.index.names, m.index.nlevels)
print(m)
print(m.loc[("Izmir", 2025), "sales"])
print(m.loc["Ankara", "sales"].to_dict())
```

```text
['city', 'year'] 2
             sales
city   year       
Ankara 2024    120
       2025    110
Bursa  2024     50
       2025     65
Izmir  2024     80
       2025     95
95
{2024: 120, 2025: 110}
```

- `set_index` iki sütun alınca her satırın etiketi bir **demet** olur:
  `("Izmir", 2025)`. Düzeylerin adları `city` ve `year`.
- Ekranda dış düzey tekrarlanmaz; okunması kolay olsun diye boş bırakılır.
- Tam etiket demetle verilir: `loc[("Izmir", 2025)]`.
- Yalnızca dış düzey verilirse o şehrin bütün yılları gelir ve dış düzey
  düşer: `loc["Ankara"]` yıllarla etiketli bir seri.

## İç düzeyden seçmek: xs ve IndexSlice

```python
import pandas as pd

df = pd.DataFrame({
    "city": ["Izmir", "Izmir", "Ankara", "Ankara", "Bursa", "Bursa"],
    "year": [2024, 2025, 2024, 2025, 2024, 2025],
    "sales": [80, 95, 120, 110, 50, 65],
})
m = df.set_index(["city", "year"]).sort_index()
print(m.xs(2025, level="year")["sales"].to_dict())
idx = pd.IndexSlice
print(m.loc[idx["Ankara":"Bursa", 2024], "sales"].tolist())
print(m.index.get_level_values("city").unique().tolist())
print(m.swaplevel().sort_index().index[:3].tolist())
```

```text
{'Ankara': 110, 'Bursa': 65, 'Izmir': 95}
[120, 50]
['Ankara', 'Bursa', 'Izmir']
[(2024, 'Ankara'), (2024, 'Bursa'), (2024, 'Izmir')]
```

- `loc` önce dış düzeye bakar. "Bütün şehirlerin 2025'i" gibi **iç**
  düzeyden seçim için `xs(2025, level="year")`.
- İki düzeyde birden dilim için `pd.IndexSlice`: `idx["Ankara":"Bursa",
  2024]` Ankara'dan Bursa'ya (dahil) şehirlerin 2024 satırları.
- `get_level_values("city")` bir düzeyin etiketlerini satır satır verir
  (tekrarlı); `unique()` ile benzersizler.
- `swaplevel()` düzeylerin yerini değiştirir; ardından `sort_index()`
  yoksa yıllar karışık kalır.

## Sıralanmamış MultiIndex

```python
import pandas as pd

df = pd.DataFrame({
    "city": ["Izmir", "Ankara", "Izmir", "Ankara"],
    "year": [2025, 2024, 2024, 2025],
    "sales": [95, 120, 80, 110],
})
m = df.set_index(["city", "year"])
print(m.index.is_monotonic_increasing)
try:
    m.loc[("Ankara", 2024):("Izmir", 2024)]
except Exception as error:
    print(type(error).__name__ + ":", error)
s = m.sort_index()
print(s.index.is_monotonic_increasing)
print(s.loc[("Ankara", 2025):("Izmir", 2024), "sales"].tolist())
```

```text
False
UnsortedIndexError: 'Key length (2) was greater than MultiIndex lexsort depth (0)'
True
[110, 80]
```

- Bir aralığı dilimlemek için pandas'ın "nerede başlar, nerede biter"i
  bulabilmesi gerekir; bu yalnızca **sıralı** indekste mümkün.
- Sıralanmamış MultiIndex'te dilim `UnsortedIndexError` verir. Mesajdaki
  "lexsort depth (0)" "hiçbir düzey sıralı değil" demek.
- Çözüm tek satır: `sort_index()`. Sıralı indekste tek etiket aramak da
  daha hızlıdır (ikili arama), o yüzden MultiIndex kurunca hemen sıralamak
  iyi bir alışkanlık.

## groupby'dan çıkan MultiIndex

```python
import pandas as pd

df = pd.DataFrame({
    "city": ["Izmir", "Izmir", "Ankara", "Ankara", "Bursa", "Bursa"],
    "year": [2024, 2025, 2024, 2025, 2024, 2025],
    "sales": [80, 95, 120, 110, 50, 65],
})
g = df.groupby(["city", "year"])["sales"].sum()
print(type(g.index).__name__, g.index.names)
print(g.groupby(level="city").sum().to_dict())
print(g.unstack())
print(g.reset_index().head(2))
```

```text
MultiIndex ['city', 'year']
{'Ankara': 230, 'Bursa': 115, 'Izmir': 175}
year    2024  2025
city              
Ankara   120   110
Bursa     50    65
Izmir     80    95
     city  year  sales
0  Ankara  2024    120
1  Ankara  2025    110
```

- İki sütunla `groupby` yapınca sonuç **MultiIndex**'li bir seri olur. Çoğu
  kişi MultiIndex'le ilk kez burada karşılaşır.
- Bir düzey üzerinden yeniden toplamak için `groupby(level="city")`.
- `unstack()` iç düzeyi (`year`) sütunlara çevirir: uzun tablo geniş tabloya
  döner. Yeniden şekillendirme bölümünde ayrıntısıyla gelecek.
- `reset_index()` iki düzeyi de sütuna çevirir; düz bir tabloya geri dönmenin
  en kısa yolu.

## Özet

- pandas işlemleri **etikete göre hizalar**; eşleşmeyen etiket `NaN` olur.
  `.values` etiketi atar ve sıraya göre hesaplar.
- `loc` etiket, `iloc` konum. `set_index` / `reset_index` sütun ile indeks
  arasında taşır.
- Tekrarlı etiket `loc`'un dönüş türünü değiştirir; `is_unique` ile denetle.
- MultiIndex: tam etiket demetle, iç düzey `xs` ile, iki düzeyde dilim
  `IndexSlice` ile. Dilimden önce `sort_index()`.
