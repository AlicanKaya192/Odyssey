# Metin ve Kategorik Veri

Elle girilmiş metin sütunları dağınıktır: " Izmir", "izmir" ve "IZMIR" üç ayrı
şehir sayılır, kodların içinde parçalanması gereken bilgiler durur. Öte yandan
milyon satırlık bir tabloda yalnızca üç farklı değer alan bir sütun, her satırda
aynı metni tekrar tekrar saklar. Bu bölümün iki konusu bunlar: `.str` ile metni
toplu temizlemek ve parçalamak, `category` türüyle tekrarlayan değerleri az
bellekle ve doğru sırayla tutmak.

## .str: bütün sütunu bir kerede

```python
import pandas as pd

names = pd.Series(["  Izmir", "izmir ", "IZMIR", "Ankara", None])
print(names.dtype, names.nunique())
clean = names.str.strip().str.title()
print(clean.tolist(), clean.nunique())
print(clean.str.len().tolist())
```

```text
str 4
['Izmir', 'Izmir', 'Izmir', 'Ankara', nan] 2
[5.0, 5.0, 5.0, 6.0, nan]
```

- Python'un metin metotları (`strip`, `lower`, `title`, `replace`, `split`)
  sütunda `.str` üzerinden çalışır; döngü gerekmez.
- Temizlemeden önce 4 farklı şehir vardı, sonra 2. Gruplamadan önce bu
  temizlik yapılmazsa İzmir'in satışları üç parçaya bölünür.
- Eksik değer (`None`) hata vermez, eksik kalır. `str.len()` bu yüzden
  ondalık döner: `NaN` tam sayıda tutulamaz.
- pandas 3'te metin sütununun türü `str`.

## contains ve eksik değer

```python
import pandas as pd

notes = pd.Series(["late delivery", "Delivery OK", None, "broken box"])
print(notes.str.contains("delivery").tolist())
print(notes.str.contains("delivery", case=False).tolist())
print(notes.str.contains("late|broken").tolist())
old = notes.astype(object)
try:
    old[old.str.contains("delivery")]
except ValueError as error:
    print("ValueError:", error)
print(len(old[old.str.contains("delivery", na=False)]))
```

```text
[True, False, False, False]
[True, True, False, False]
[True, False, False, True]
ValueError: Cannot mask with non-boolean array containing NA / NaN values
1
```

- `contains` büyük/küçük harfe duyarlıdır; `case=False` ikisini de bulur.
- Desen varsayılan olarak **düzenli ifadedir**: `"late|broken"` "late ya da
  broken". Nokta, parantez gibi işaretleri düz aramak için `regex=False`.
- pandas 3'ün `str` türünde eksik değer `False` döner. Eski türde (`object`,
  eski pandas ya da başka yerden gelen sütun) sonuç `None` içerir ve filtre
  olarak kullanılamaz: "Cannot mask with non-boolean array". `na=False` iki
  durumda da güvenli.

## extract: düzenli ifadeyle parçalamak

```python
import pandas as pd

codes = pd.Series(["TR-34-0012", "TR-06-0450", "DE-11-0007", "bad"])
pattern = r"(?P<country>[A-Z]{2})-(?P<region>\d{2})-(?P<num>\d{4})"
parts = codes.str.extract(pattern)
print(parts)
print(parts["num"].astype("Int64").tolist())
print(codes.str.split("-", expand=True).shape)
print(codes.str.replace(r"\d", "#", regex=True).tolist())
```

```text
  country region   num
0      TR     34  0012
1      TR     06  0450
2      DE     11  0007
3     NaN    NaN   NaN
[12, 450, 7, <NA>]
(4, 3)
['TR-##-####', 'TR-##-####', 'DE-##-####', 'bad']
```

- `str.extract` düzenli ifadenin her **grubunu** bir sütun yapar; `?P<ad>`
  sütuna ad verir. Kalıba uymayan satır (`bad`) bütün sütunlarda `NaN`.
- Çıkan parçalar metindir; `0012` sayı olacaksa `astype("Int64")` (büyük I:
  eksik değeri `<NA>` olarak tutabilen tam sayı).
- `split("-", expand=True)` parçaları sütunlara açar; yapı düzenliyse
  extract'ten kısa.
- `replace(..., regex=True)` desene uyan her yeri değiştirir.

## category: tekrarlayan değerler

```python
import pandas as pd

cities = pd.Series(["Izmir", "Ankara", "Izmir", "Bursa"] * 250_000)
as_cat = cities.astype("category")
print(len(cities), as_cat.cat.categories.tolist())
print(as_cat.cat.codes[:4].tolist(), as_cat.cat.codes.dtype)
before = cities.memory_usage(deep=True) / 1e6
after = as_cat.memory_usage(deep=True) / 1e6
print(round(before, 1), round(after, 1), after < before / 5)
```

```text
1000000 ['Ankara', 'Bursa', 'Izmir']
[2, 0, 2, 1] int8
13.3 1.0 True
```

- `category` her farklı değeri **bir kez** saklar (`categories`) ve her
  satırda yalnızca küçük bir **kod** tutar: Ankara 0, Bursa 1, İzmir 2.
  Kodun türü `int8`, yani satır başına 1 bayt.
- Bir milyon satırda bellek MB cinsinden 13,3'ten 1,0'a indi. Kazanç, farklı
  değer sayısı satır sayısına göre **az** olduğunda büyük; her satırı farklı
  olan bir sütunu (ad, e-posta) kategoriye çevirmek kazandırmaz.
- Gruplama ve sıralama da kodlar üzerinden yapıldığı için hızlanır.

## Sıralı kategori

```python
import pandas as pd

sizes = pd.Series(["M", "S", "XL", "M", "L"])
print(sorted(sizes.unique()))
size_type = pd.CategoricalDtype(["S", "M", "L", "XL"], ordered=True)
sized = sizes.astype(size_type)
print(sized.sort_values().tolist())
print((sized >= "L").tolist(), sized.max())
print(sizes.astype(size_type).value_counts(sort=False).to_dict())
```

```text
['L', 'M', 'S', 'XL']
['S', 'M', 'M', 'L', 'XL']
[False, False, True, False, True] XL
{'S': 1, 'M': 2, 'L': 1, 'XL': 1}
```

- Metin alfabetik sıralanır: `L, M, S, XL`. Beden için anlamsız.
- `CategoricalDtype(..., ordered=True)` sırayı **sen** verirsin: S < M < L <
  XL. Artık sıralama, `>=` karşılaştırması ve `max()` bedene göre çalışır.
- `value_counts(sort=False)` kategorileri kendi sırasıyla verir; rapor ve
  grafikte eksenin doğru sırada çıkması için.
- Memnuniyet anketi ("kötü < orta < iyi"), eğitim düzeyi, öncelik gibi her
  sıralı sınıf için aynı kalıp.

## cut ve qcut: sayıyı sınıfa çevirmek

```python
import pandas as pd

ages = pd.Series([15, 22, 37, 45, 61, 70])
bins = [0, 18, 40, 65, 120]
groups = pd.cut(ages, bins=bins, labels=["child", "young", "middle", "senior"])
print(groups.tolist())
print(groups.value_counts(sort=False).to_dict())
print(pd.cut(ages, bins=[0, 18, 40]).isna().sum())
quart = pd.qcut(ages, q=3, labels=["low", "mid", "high"])
print(quart.tolist())
```

```text
['child', 'young', 'young', 'middle', 'middle', 'senior']
{'child': 1, 'young': 2, 'middle': 2, 'senior': 1}
3
['low', 'low', 'mid', 'mid', 'high', 'high']
```

- `cut` sayıları **senin verdiğin sınırlara** göre gruplar. Aralıklar sağdan
  kapalı: `(18, 40]` 18'i almaz, 40'ı alır. Sonuç sıralı bir kategori.
- Sınırların dışında kalan değer `NaN` olur: 45, 61 ve 70 için sınır yoktu,
  3 değer kayboldu. Son sınırı geniş tut.
- `qcut` sınırları **verinin kendisinden** seçer: her grupta yaklaşık eşit
  sayıda kişi olacak şekilde (burada 2'şer).

## Özet

- `.str` metin metotlarını bütün sütuna uygular; gruplamadan önce `strip`,
  `lower` / `title` ile temizle.
- `contains` düzenli ifade kullanır; eski türdeki eksik değer için `na=False`.
- `str.extract` grupları sütunlara açar.
- `category`: az sayıda farklı değer için az bellek; sıralı kategori sırayı
  senin vermeni sağlar.
- `cut` senin sınırlarınla, `qcut` eşit sayıda grup olacak şekilde.
