# Yeniden Şekillendirme

Aynı veri iki biçimde yazılabilir. **Geniş** biçimde her ay bir sütundur:
insanın okuması kolaydır, Excel raporları böyledir. **Uzun** biçimde her
ölçüm bir satırdır (şehir, ay, satış): `groupby`, grafik kütüphaneleri ve
modeller bunu ister. Veri biliminde zamanın büyük kısmı ikisi arasında gidip
gelmekle geçer. Bu bölüm `melt`, `pivot`, `pivot_table`, `stack` /
`unstack` ve `explode`'u ve her birinin sessiz tuzaklarını anlatıyor.

## melt: genişten uzuna

```python
import pandas as pd

wide = pd.DataFrame({"city": ["Izmir", "Ankara"],
                     "jan": [80, 120], "feb": [95, 110]})
long = wide.melt(id_vars="city", var_name="month", value_name="sales")
print(long)
print(wide.shape, long.shape)
```

```text
     city month  sales
0   Izmir   jan     80
1  Ankara   jan    120
2   Izmir   feb     95
3  Ankara   feb    110
(2, 3) (4, 3)
```

- `id_vars` olduğu gibi kalacak sütun(lar): her satırın kimliği.
- Geri kalan sütunlar (`jan`, `feb`) eriyip iki sütuna dönüşür: sütunun adı
  `var_name`'e, değeri `value_name`'e gider.
- 2 satır × 2 ay = 4 satır. Satır sayısı ay sayısıyla çarpılır; bu beklenen
  bir şey, hata değil.
- Yalnızca bazı sütunları eritmek için `value_vars=["jan", "feb"]`.

## pivot: uzundan genişe

```python
import pandas as pd

long = pd.DataFrame({"city": ["Izmir", "Ankara", "Izmir", "Ankara"],
                     "month": ["jan", "jan", "feb", "feb"],
                     "sales": [80, 120, 95, 110]})
wide = long.pivot(index="city", columns="month", values="sales")
print(wide)
print(wide.columns.name, wide.index.name)
flat = wide.reset_index().rename_axis(columns=None)
print(flat.columns.tolist())
```

```text
month   feb  jan
city            
Ankara  110  120
Izmir    95   80
month city
['city', 'feb', 'jan']
```

- `pivot` melt'in tersi: `index` satırlar, `columns`'un değerleri sütun
  başlıkları, `values` hücreler.
- **Sütunlar alfabetik sıralandı:** `feb`, `jan`'dan önce geldi. Ay gibi
  doğal sırası olan bir şeyde `wide[["jan", "feb"]]` ile sırayı kendin ver.
- Sonuçtaki sütun ekseninin bir adı var (`month`); ekranda sol üstte görünen
  o. Düz bir tabloya dönmek için `reset_index()` ve
  `rename_axis(columns=None)`.

## Tekrarlı çift: pivot hata verir

```python
import pandas as pd

long = pd.DataFrame({"city": ["Izmir", "Izmir", "Ankara"],
                     "month": ["jan", "jan", "jan"], "sales": [30, 50, 120]})
try:
    long.pivot(index="city", columns="month", values="sales")
except ValueError as error:
    print("ValueError:", error)
table = long.pivot_table(index="city", columns="month", values="sales",
                         aggfunc="sum")
print(table)
```

```text
ValueError: Index contains duplicate entries, cannot reshape
month   jan
city       
Ankara  120
Izmir    80
```

- İzmir'in ocak ayı iki kez var (30 ve 50). `pivot` bir hücreye iki değeri
  koyamaz ve durur: "Index contains duplicate entries".
- `pivot` **yeniden düzenler**, hesaplamaz. Tekrarlar bir hesapla
  birleştirilecekse (toplam, ortalama) doğru araç `pivot_table`:
  `aggfunc="sum"` İzmir'in ocağını 80 yaptı.
- Bu hata çoğu zaman veride beklenmedik bir tekrar olduğunu gösterir; körü
  körüne `pivot_table`'a geçmeden önce tekrarın neden olduğuna bak.

## pivot_table: özet tablo

```python
import pandas as pd

sales = pd.DataFrame({
    "city": ["Izmir", "Izmir", "Ankara", "Ankara", "Bursa"],
    "month": ["jan", "feb", "jan", "jan", "feb"],
    "amount": [80, 95, 70, 50, 65],
})
table = sales.pivot_table(index="city", columns="month", values="amount",
                          aggfunc="sum", fill_value=0,
                          margins=True, margins_name="total")
print(table)
counts = pd.crosstab(sales["city"], sales["month"])
print(counts.loc["Ankara"].to_dict())
```

```text
month   feb  jan  total
city                   
Ankara    0  120    120
Bursa    65    0     65
Izmir    95   80    175
total   160  200    360
{'feb': 0, 'jan': 2}
```

- Excel'deki özet tablonun karşılığı. `aggfunc` hesabı seçer (varsayılanı
  **`"mean"`**; toplam istiyorsan yazman gerekir).
- `fill_value=0`: hiç kaydı olmayan çift (Ankara'nın şubatı) `NaN` yerine 0.
- `margins=True` satır ve sütun toplamlarını ekler; adı `margins_name`.
- `pd.crosstab` iki sütunun **kaç kez** birlikte geçtiğini sayar: Ankara'nın
  ocakta 2 kaydı var. Sayım için pivot_table'dan kısa yol.

## stack ve unstack

```python
import pandas as pd

wide = pd.DataFrame({"jan": [80, 120], "feb": [95, None]},
                    index=["Izmir", "Ankara"])
long = wide.stack()
print(type(long.index).__name__, len(long))
print(long)
back = long.unstack()
print(back.columns.tolist(), back.isna().sum().sum())
```

```text
MultiIndex 4
Izmir   jan     80.0
        feb     95.0
Ankara  jan    120.0
        feb      NaN
dtype: float64
['jan', 'feb'] 1
```

- `stack()` sütunları indeksin iç düzeyine indirir: sonuç MultiIndex'li bir
  seri. `unstack()` tersi; iç düzeyi yeniden sütun yapar.
- melt ile pivot sütunlarla çalışır, stack ile unstack **indeksle**. Veri
  zaten indeksteyse (önceki bölümün groupby sonucu gibi) bunlar daha kısadır.
- pandas 3'te `stack` eksik değeri **atmaz**: Ankara'nın şubatı `nan` olarak
  durdu. Eski sürümler atıyordu; eski bir örnekteki satır sayısı tutmazsa
  sebep bu. Atmak için `.dropna()`.

## explode: listeyi satırlara aç

```python
import pandas as pd

orders = pd.DataFrame({"order": [1, 2], "tags": ["gift,fast", "fast"]})
orders["tags"] = orders["tags"].str.split(",")
print(orders["tags"].tolist())
rows = orders.explode("tags")
print(rows.index.tolist(), rows["tags"].tolist())
print(rows["tags"].value_counts().to_dict())
```

```text
[['gift', 'fast'], ['fast']]
[0, 0, 1] ['gift', 'fast', 'fast']
{'fast': 2, 'gift': 1}
```

- Bir hücrede birden fazla değer (etiketler, kategoriler) virgülle yazılmışsa
  önce `str.split(",")` ile listeye çevrilir.
- `explode` listenin her elemanını ayrı satır yapar; öteki sütunlar
  kopyalanır. Ardından sıradan bir sayım ya da `groupby` yapılabilir.
- İndeks kopyalanır (`[0, 0, 1]`): tekrarlı etiket. Gerekirse
  `explode(..., ignore_index=True)`.

## Özet

| Yön | Sütunla | İndeksle |
|---|---|---|
| Genişten uzuna | `melt` | `stack` |
| Uzundan genişe | `pivot` / `pivot_table` | `unstack` |

- `pivot` tekrarlı çiftte durur; tekrarları birleştirmek için `pivot_table`
  (varsayılan hesap ortalama).
- Sonuç sütunları alfabetik sıralanır; doğal sırayı kendin ver.
- pandas 3'te `stack` eksik değeri tutar. Listeli hücreler `explode` ile
  satırlara açılır.
