Kategorinin değer listesi **veriden ayrı** durur. Bu yüzden hiç satırı
olmayan bir kategori (XL bedeninden hiç satılmadı) tabloda var olmaya devam
eder. Bazen istenen budur (raporda "XL: 0" görünmeli), bazen kafa karıştırır.

```python
import pandas as pd

size_type = pd.CategoricalDtype(["S", "M", "L", "XL"], ordered=True)
sizes = pd.Series(["M", "S", "M"], dtype=size_type)
df = pd.DataFrame({"size": sizes, "qty": [2, 1, 4]})
print(df.groupby("size")["qty"].sum().to_dict())
print(df.groupby("size", observed=False)["qty"].sum().to_dict())
print(df["size"].value_counts().to_dict())
small = df[df["size"] != "M"]
print(small["size"].cat.categories.tolist())
print(small["size"].cat.remove_unused_categories().cat.categories.tolist())
```

```text
{'S': 1, 'M': 6}
{'S': 1, 'M': 6, 'L': 0, 'XL': 0}
{'M': 2, 'S': 1, 'L': 0, 'XL': 0}
['S', 'M', 'L', 'XL']
['S']
```

## Ne oldu?

- pandas 3'te `groupby` varsayılan olarak yalnızca **görülen** kategorileri
  verir (`observed=True`): S ve M.
- `observed=False` bütün kategorileri verir, satırı olmayanlara 0 yazar.
  "Hiç satılmayan beden" de raporda görünsün istiyorsan bu.
- `value_counts` ise her zaman bütün kategorileri sayar; satılmayanlar 0. Aynı
  sütun iki farklı fonksiyonda iki farklı uzunlukta sonuç verebilir.
- Filtreleme kategorileri silmez: M satırları gitti ama `M` hâlâ
  kategorilerde. `remove_unused_categories()` yalnızca kullanılanları bırakır.

## Neden önemli?

Bir grafikte boş çubuklar, bir modelde hiç görülmemiş sınıf için açılmış bir
sütun (one-hot kodlamada) ya da beklenenden uzun bir sonuç listesi hep aynı
sebepten çıkar: kategori listesi verinin içindekinden fazlasını tutuyordur.
Kategorik sütunla çalışırken "listede ne var" (`cat.categories`) ile
"veride ne var" (`unique()`) ayrı sorulardır.
