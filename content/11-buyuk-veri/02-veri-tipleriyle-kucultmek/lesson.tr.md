# Veri Tipleriyle Küçültmek

Geçen bölümün raporu iki şey söylemişti: tarih metin olarak saklanmış ve
şehir, kategori, ödeme sütunları aynı birkaç kelimeyi tekrar ediyor. Sayı
sütunları da her değere 8 bayt ayırıyor; oysa `quantity` hiçbir zaman 5'i
geçmiyor.

Bu bölümde her sütuna **doğru türü** vererek bir milyon siparişlik tabloyu
96 MB'tan 23 MB'a indireceğiz. Tek bir satır silinmeyecek, tek bir bilgi
kaybolmayacak. Ama yanlış tür seçmenin sessiz tuzakları da var; onları da
göreceğiz.

Bölümdeki örneklerin hepsi aynı tabloyla başlıyor:

```python
import numpy as np
import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 1_000_000)
df = pd.read_csv("orders.csv")
```

## Tam sayılar: doğru genişliği seç

pandas bir CSV'deki tam sayıları her zaman `int64` yapıyor: değer başına 8
bayt, yaklaşık ±9 kentilyonluk bir aralık. Bir sepetteki ürün adedi için bu
aralık fazlasıyla geniş. Daha dar türler daha az yer tutuyor:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>int8</code> · 1 bayt</span><span>−128 … 127: adet, puan</span></div>
    <div class="anat-row"><span><code>int16</code> · 2 bayt</span><span>−32 768 … 32 767: yıl, küçük sayaç</span></div>
    <div class="anat-row"><span><code>int32</code> · 4 bayt</span><span>yaklaşık ±2,1 milyar: kimlik numarası</span></div>
    <div class="anat-row"><span><code>int64</code> · 8 bayt</span><span>yaklaşık ±9,2 × 10¹⁸: pandas'ın varsayılanı</span></div>
  </div>
  <figcaption>Her basamak iki kat yer, çok daha geniş aralık. Önüne <code>u</code> gelen işaretsiz türler (<code>uint8</code>) eksi tutmaz, artıda iki kat yer açar: 0 … 255.</figcaption>
</figure>

Her türün aralığını `np.iinfo` ile görebilirsin:

```python
for t in ["int8", "int16", "int32", "int64"]:
    i = np.iinfo(t)
    print(t, i.min, i.max)
```

```text
int8 -128 127
int16 -32768 32767
int32 -2147483648 2147483647
int64 -9223372036854775808 9223372036854775807
```

Doğru türü seçmek için önce sütunun **en küçük ve en büyük** değerine bak:

```python
print(df["quantity"].min(), df["quantity"].max())
print(df["customer_id"].min(), df["customer_id"].max())
print(df["order_id"].min(), df["order_id"].max())
```

```text
1 5
1 249999
1 1000000
```

- `quantity` 1 ile 5 arasında: `int8` (1 bayt) rahatça yeter.
- `customer_id` en fazla 249 999: `int16`'nın 32 767'sini aşıyor, `int32`.
- `order_id` en fazla 1 000 000: yine `int32`.

Türü `astype` ile değiştiriyorsun:

```python
q8 = df["quantity"].astype("int8")
print(round(df["quantity"].memory_usage(deep=True) / 1024**2, 2))
print(round(q8.memory_usage(deep=True) / 1024**2, 2))
```

```text
7.63
0.95
```

Aynı sütun, sekizde bir yer.

### `downcast`: türü pandas'a seçtirmek

Aralığa bakıp türü elle seçmek yerine pandas'a bırakabilirsin.
`pd.to_numeric(..., downcast="integer")` değerlerin sığdığı **en küçük**
tam sayı türünü seçiyor:

```python
print(pd.to_numeric(df["customer_id"], downcast="integer").dtype)
print(pd.to_numeric(df["order_id"], downcast="integer").dtype)
print(pd.to_numeric(df["quantity"], downcast="unsigned").dtype)
```

```text
int32
int32
uint8
```

`downcast="unsigned"` **işaretsiz** türleri de deniyor: `uint8` 0 ile 255
arasında, eksi sayı tutmuyor. Adet, yaş, sayaç gibi hiç eksi olmayacak
değerler için uygun.

## Tuzak: taşma (overflow)

Küçük türün bir bedeli var: aralığın dışına çıkan değer **hata vermeden
bozulabiliyor**.

```python
stock = pd.Series([100, 200, 300])
print(stock.astype("int8").tolist())
```

```text
[100, -56, 44]
```

200 ve 300, `int8`'in 127'lik sınırını aştı. pandas uyarmadı; değerler
saatin akrebinin 12'den 1'e dönmesi gibi başa sarıp anlamsız sayılara dönüştü.
Hesap da aynı şekilde taşabiliyor:

```python
small = pd.Series([100, 120, 127]).astype("int8")
print((small + 1).tolist())
```

```text
[101, 121, -128]
```

<figure class="fig">
  <div class="flow">
    <span class="node">127<br><code>int8</code>'in sınırı</span><span class="arrow">→</span>
    <span class="node">+ 1</span><span class="arrow">→</span>
    <span class="node no">−128<br>başa sardı</span>
  </div>
  <figcaption>Taşan değer en küçük değere sarıyor. pandas bunu hata saymıyor; sonuç yalnızca yanlış.</figcaption>
</figure>

Kendini korumanın üç yolu:

1. Türü değiştirmeden önce `min()` ve `max()`'a bak.
2. `astype` yerine `pd.to_numeric(..., downcast=...)` kullan; sığmayan
   değeri küçük türe zorlamıyor.
3. Büyüme payı bırak. `quantity` bugün en fazla 5; yarın toptan satış
   başlarsa 300 olabilir. Emin değilsen bir basamak geniş tür seç (`int16`).

## Ondalıklı sayılar: `float32`

`float64` yaklaşık 15–16 basamak duyarlı, 8 bayt. `float32` 4 bayt ama
yalnızca yaklaşık **7 basamak** tutabiliyor:

```python
prices = pd.Series([19.99, 1234.56, 99999.99, 1234567.89])
print(prices.astype("float32").tolist())
```

```text
[19.989999771118164, 1234.56005859375, 99999.9921875, 1234567.875]
```

Küçük fiyatlarda fark virgülden sonraki altıncı basamakta; 1 234 567,89 ise
1 234 567,875 oldu. Tek tek bakınca küçük, ama toplayınca büyüyor:

```python
p32 = df["unit_price"].astype("float32")
print(round(df["unit_price"].sum(), 2))
print(round(float(p32.sum()), 2))
print(round(float(p32.astype("float64").sum()), 2))
```

```text
736869041.37
736869056.0
736869041.4
```

1. satır: gerçek toplam (`float64`).
2. satır: `float32` değerler `float32` içinde toplanınca 15 TL sapma.
3. satır: aynı `float32` değerler `float64`'e çevrilip toplanınca sapma
   kayboluyor.

Sorun saklamada değil, **toplamanın** 7 basamakla yapılmasında. Kurallar:

- `float32` ölçüm, oran, model girdisi gibi değerlerde çoğu zaman yeterli.
- Toplarken ve ortalama alırken `float64`'e çevir.
- **Para** için `float32` kullanma. Daha güvenli bir yol: kuruşu tam sayı
  olarak saklamak (`(fiyat * 100).round().astype("int64")`).

## Tekrar eden metin: `category`

`city` sütununda bir milyon satır var ama yalnızca 8 farklı şehir.
`category` türü her farklı değeri **bir kez** saklıyor, satırlarda ise o
değerin numarasını tutuyor:

<figure class="fig">
  <div class="versus">
    <div class="no"><h4><code>str</code></h4><p>Her satırda metnin kendisi<br><code>"Istanbul"</code>, <code>"Trabzon"</code>, <code>"Istanbul"</code>, …<br>Satır başına 14,5 bayt</p></div>
    <div class="ok"><h4><code>category</code></h4><p>Liste bir kez: <code>Adana</code>, <code>Ankara</code>, … (8 şehir)<br>Satırlarda numara: <code>4</code>, <code>7</code>, <code>4</code>, …<br>Satır başına 1 bayt</p></div>
  </div>
  <figcaption>Farklı değer az, tekrar çoksa <code>category</code> büyük kazanç. Farklı değer çoksa liste sütun kadar uzuyor ve kazanç kayboluyor.</figcaption>
</figure>

```python
city = df["city"].astype("category")
print(round(df["city"].memory_usage(deep=True) / 1024**2, 2))
print(round(city.memory_usage(deep=True) / 1024**2, 2))
print(city.cat.categories.tolist())
print(city.cat.codes.dtype, city.cat.codes.head(3).tolist())
```

```text
13.79
0.95
['Adana', 'Ankara', 'Antalya', 'Bursa', 'Istanbul', 'Izmir', 'Konya', 'Trabzon']
int8 [4, 7, 6]
```

- `cat.categories`: farklı değerlerin listesi (abece sırasında).
- `cat.codes`: her satırdaki numara. 8 şehir için `int8` yetiyor: satır
  başına 1 bayt. İlk satır `4` yani `Istanbul`.

Sütun 13,8 MB'tan 0,95 MB'a indi. Ama `category` her metin için doğru
değil:

```python
print(df["order_time"].nunique())
t = df["order_time"].astype("category")
print(round(df["order_time"].memory_usage(deep=True) / 1024**2, 2))
print(round(t.memory_usage(deep=True) / 1024**2, 2))
```

```text
984369
25.75
29.28
```

Bir milyon satırda 984 369 farklı zaman var; neredeyse hepsi tek. Bu durumda
kategori listesi sütunun kendisi kadar uzun, üstüne bir de numaralar
ekleniyor: sütun **büyüdü**. Kural:

> `category` farklı değer sayısı satır sayısına göre **küçükse** işe
> yarıyor. `nunique()` ile kontrol et.

`category` sütunu sıradan metin gibi kullanılabiliyor: `city == "Istanbul"`
karşılaştırması, `groupby("city")` ve süzme aynen çalışıyor.

## Tarihler: `datetime64`

`order_time` aslında bir tarih ve saat. Metin olarak 27 bayt tutuyor; tarih
türünde 8 bayt:

```python
times = pd.to_datetime(df["order_time"])
print(times.dtype)
print(round(df["order_time"].memory_usage(deep=True) / 1024**2, 2))
print(round(times.memory_usage(deep=True) / 1024**2, 2))
```

```text
datetime64[us]
25.75
7.63
```

`datetime64[us]`: mikrosaniye duyarlı tarih-saat, 8 bayt. Hem üç kat küçük
hem de artık gerçek bir tarih: `times.dt.month` ile ay, `times.dt.hour` ile
saat alınabiliyor, iki tarih arasındaki fark hesaplanabiliyor.

## Eksik değerler ve "nullable" türler

Tam sayı sütununda bir değer eksikse pandas sütunu sessizce ondalıklıya
çeviriyor, çünkü `NaN` bir ondalıklı sayı:

```python
s = pd.Series([1, 2, None, 4])
print(s.dtype, s.tolist())
n = pd.Series([1, 2, None, 4], dtype="Int8")
print(n.dtype, n.tolist())
```

```text
float64 [1.0, 2.0, nan, 4.0]
Int8 [1, 2, <NA>, 4]
```

Büyük harfle yazılan `Int8`, `Int16`, `Int32`, `Int64` türleri eksik değeri
`<NA>` olarak tutabiliyor: değer başına 1 bayt ve "bu değer eksik mi?"
bilgisi için 1 bayt daha. Eksik değeri olan küçük bir tam sayı sütunu için
`float64`'ten (8 bayt) çok daha ucuz.

`True` / `False` tutan sütunlar `bool` türünde ve değer başına 1 bayt.

## Hepsi bir arada

Bütün sütunlara doğru türü verelim:

```python
small = df.astype({
    "order_id": "int32",
    "customer_id": "int32",
    "quantity": "int8",
    "unit_price": "float32",
    "city": "category",
    "category": "category",
    "payment": "category",
})
small["order_time"] = pd.to_datetime(small["order_time"])
print(small.memory_usage(deep=True))
```

```text
Index              132
order_id       4000000
order_time     8000000
customer_id    4000000
city           1000113
category       1000087
quantity       1000000
unit_price     4000000
payment        1000041
dtype: int64
```

Toplam 95,9 MB'tan **22,9 MB'a** indi: dört kattan fazla küçülme. Aynı
satırlar, aynı bilgi.

`astype` bir sözlük alabiliyor: `{"sütun": "tür", ...}`. Sözlükte
olmayan sütunlar olduğu gibi kalıyor.

## Daha iyisi: okurken küçültmek

Yukarıda tablo önce 96 MB olarak kuruldu, sonra küçültüldü. Belleğin
yetmediği bir durumda o ilk adım bile mümkün olmayabilir. `read_csv`
türleri **okurken** alabiliyor:

```python
df = pd.read_csv(
    "orders.csv",
    dtype={"order_id": "int32", "customer_id": "int32", "quantity": "int8",
           "unit_price": "float32", "city": "category", "category": "category",
           "payment": "category"},
    parse_dates=["order_time"],
)
print(round(df.memory_usage(deep=True).sum() / 1024**2, 1))
```

```text
22.9
```

- `dtype=`: sütun başına tür sözlüğü.
- `parse_dates=`: tarih olarak okunacak sütunların listesi.

Sonuç aynı 22,9 MB, ama önce 96 MB'lık tabloyu kurup sonra küçültmek zorunda
kalmıyorsun.

## Karar tablosu

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Tam sayı, aralığı küçük</span><span><code>int8</code> / <code>int16</code> / <code>int32</code>; önce <code>min</code>, <code>max</code></span></div>
    <div class="anat-row"><span>Tam sayı, eksik değerli</span><span><code>Int8</code> … <code>Int64</code></span></div>
    <div class="anat-row"><span>Ondalıklı, ölçüm</span><span><code>float32</code>; toplarken <code>float64</code></span></div>
    <div class="anat-row"><span>Para</span><span><code>float64</code> ya da kuruş olarak tam sayı</span></div>
    <div class="anat-row"><span>Metin, az farklı değer</span><span><code>category</code></span></div>
    <div class="anat-row"><span>Metin, çoğu farklı</span><span><code>str</code> olarak bırak</span></div>
    <div class="anat-row"><span>Tarih, saat</span><span><code>datetime64</code> (<code>parse_dates</code>)</span></div>
  </div>
  <figcaption>Her satır bir soru: sütunda ne var? Cevap türü seçiyor.</figcaption>
</figure>

## Özet

- pandas tam sayıları `int64`, ondalıklıları `float64` okuyor. Değerlerin
  aralığına uyan daha dar tür aynı bilgiyi daha az yerde tutuyor.
- `pd.to_numeric(..., downcast="integer")` en küçük güvenli türü seçiyor.
- **Taşma sessiz:** `astype("int8")` 300'ü 44 yapıyor. Önce `min()` /
  `max()`, büyüme payı bırak.
- `float32` yaklaşık 7 basamak; toplarken `float64`'e çevir, para için
  kullanma.
- `category` az sayıda farklı değeri olan metinde büyük kazanç (13,8 MB →
  0,95 MB); neredeyse hepsi farklı değerlerde zarar.
- Tarihi `pd.to_datetime` ile `datetime64` yap: 27 bayt yerine 8 bayt ve
  tarih işlemleri.
- Eksik değerli tam sayılar için `Int8` … `Int64`.
- En iyisi türleri okurken vermek: `read_csv(dtype=..., parse_dates=...)`.
  Bir milyon sipariş: 95,9 MB → 22,9 MB.
