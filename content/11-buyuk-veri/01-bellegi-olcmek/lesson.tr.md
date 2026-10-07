# Belleği Ölçmek

Geçen bölümde tablonun **tamamının** ne kadar yer tuttuğuna baktık. Bir
şeyi küçültmek için bu yetmiyor; asıl soru şu: **hangi sütun** pahalı ve
**neden**? Bu bölümde tabloyu sütun sütun ölçmeyi, indeksin payını, bir
işlemin ne kadar yeni bellek açtığını ve kodun en yüksek bellek anını
yakalamayı öğreneceksin.

Bütün örneklerde 100 000 siparişlik tabloyu kullanıyoruz:

```python
import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 100_000)
df = pd.read_csv("orders.csv")
```

## `info`: tek bakışta özet

`df.info()` tablonun iskeletini gösteriyor: satır sayısı, sütunlar, her
sütunun türü ve boş olmayan değer sayısı. `memory_usage="deep"` eklenince en
alta gerçek bellek kullanımını da yazıyor:

```python
df.info(memory_usage="deep")
```

```text
<class 'pandas.DataFrame'>
RangeIndex: 100000 entries, 0 to 99999
Data columns (total 8 columns):
 #   Column       Non-Null Count   Dtype  
---  ------       --------------   -----  
 0   order_id     100000 non-null  int64  
 1   order_time   100000 non-null  str    
 2   customer_id  100000 non-null  int64  
 3   city         100000 non-null  str    
 4   category     100000 non-null  str    
 5   quantity     100000 non-null  int64  
 6   unit_price   100000 non-null  float64
 7   payment      100000 non-null  str    
dtypes: float64(1), int64(3), str(4)
memory usage: 9.6 MB
```

Satır satır:

- `RangeIndex: 100000 entries`: 100 000 satır, indeks 0'dan 99 999'a.
- Her sütun için `Non-Null Count` (boş olmayan değer sayısı) ve `Dtype`
  (tür). `int64` ve `float64` sayılar, `str` metin.
- `dtypes: float64(1), int64(3), str(4)`: hangi türden kaç sütun var.
- `memory usage: 9.6 MB`: tablonun bellekte tuttuğu yer.

`info` hızlı bir ilk bakış. Ama hangi sütunun ne kadar tuttuğunu
söylemiyor; bunun için bir sonraki araç gerekiyor.

## Sütun sütun: `memory_usage`

```python
print(df.memory_usage(deep=True))
```

```text
Index              132
order_id        800000
order_time     2700000
customer_id     800000
city           1446549
category       1426855
quantity        800000
unit_price      800000
payment        1279540
dtype: int64
```

Sonuç bir seri: her sütun için **bayt** sayısı. İlk satırdaki `Index`
tablonun indeksi; sütun değil ama o da yer tutuyor (birazdan bakacağız).

Sayı sütunları tam olarak 800 000 bayt: 100 000 satır × 8 bayt. Metin
sütunları ise farklı farklı. Neden?

## Metin neden pahalı?

Bir sayı her zaman 8 bayt, ama metin uzunluğu kadar yer tutuyor. pandas 3
her metin hücresini iki parçayla saklıyor:

- metnin kendi karakterleri: `"Istanbul"` için 8 bayt (İngilizce harfler
  birer bayt; `ş`, `ğ` gibi harfler ikişer),
- metnin nerede başladığını gösteren **8 baytlık** bir işaret.

`order_time` sütunundaki her değer `"2024-04-11 21:41:26"` gibi 19
karakter. 19 + 8 = 27 bayt; 100 000 satırda 2 700 000 bayt. Tablonun en
pahalı sütunu bir tarih, ama **metin olarak** saklanmış bir tarih.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>42</code> (<code>int64</code>)</span><span>8 bayt, her zaman</span></div>
    <div class="anat-row"><span><code>"card"</code></span><span>4 karakter + 8 baytlık işaret = 12 bayt</span></div>
    <div class="anat-row"><span><code>"Istanbul"</code></span><span>8 karakter + 8 = 16 bayt</span></div>
    <div class="anat-row"><span><code>"2024-04-11 21:41:26"</code></span><span>19 karakter + 8 = 27 bayt</span></div>
  </div>
  <figcaption>pandas 3'te bir metin hücresi karakterleri kadar bayt artı nerede başladığını gösteren 8 baytlık işaret tutuyor. Uzun metin, pahalı sütun.</figcaption>
</figure>

Bunu sütun başına bir rapora dökelim:

```python
memory = df.memory_usage(deep=True).drop("Index")
report = pd.DataFrame({
    "mb": (memory / 1024**2).round(2),
    "share": (memory / memory.sum() * 100).round(1),
    "per_row": (memory / len(df)).round(1),
})
print(report.sort_values("mb", ascending=False))
```

```text
               mb  share  per_row
order_time   2.57   26.9     27.0
city         1.38   14.4     14.5
category     1.36   14.2     14.3
payment      1.22   12.7     12.8
customer_id  0.76    8.0      8.0
order_id     0.76    8.0      8.0
quantity     0.76    8.0      8.0
unit_price   0.76    8.0      8.0
```

- `mb`: sütunun megabaytı.
- `share`: tablonun yüzde kaçı.
- `per_row`: satır başına bayt.

Rapor üç şey söylüyor:

1. Dört metin sütunu tablonun **üçte ikisinden fazlası** (26,9 + 14,4 +
   14,2 + 12,7 = %68,2).
2. `order_time` tek başına dörtte biri; tarih olarak saklansa 8 bayta
   inerdi.
3. `city`, `category` ve `payment` her satırda aynı birkaç kelimeyi tekrar
   ediyor (`Istanbul`, `card` gibi). Tekrar eden metni çok daha ucuza
   saklamanın yolu var.

İkinci ve üçüncü maddenin çözümü bir sonraki bölümün konusu. Şimdilik
önemli olan şu: neyi küçülteceğini artık **sayıyla** biliyorsun.

## `deep=True` ne zaman fark eder?

pandas 3'ün `str` türünde `deep=True` yazsan da yazmasan da sonuç aynı;
pandas metnin boyutunu zaten biliyor. Ama metin eski usulle, `object` türüyle
okunmuşsa iş değişiyor:

```python
df = pd.read_csv("orders.csv", dtype={"city": object})
print(df["city"].memory_usage())
print(df["city"].memory_usage(deep=True))
```

```text
800132
5546681
```

`object` sütunu her hücrede bir Python nesnesinin **adresini** tutuyor.
`deep` olmadan pandas yalnızca adresleri sayıyor: 8 bayt × 100 000. Metin
nesneleriyle birlikte gerçek boyut yaklaşık yedi kat fazla. Başkasının kodunda, eski bir
pandas'ta ya da `object` türlü bir sütunda ölçüyorsan `deep=True`'yu unutma;
yoksa sonuç sana gerçeğin bir parçasını söyler.

## İndeks de yer tutar

Tablonun indeksi de bellekte duruyor. `read_csv`'nin verdiği indeks bir
`RangeIndex`: 0'dan 99 999'a giden sayıları tek tek saklamıyor, yalnızca
"başlangıç, bitiş, adım" üçlüsünü tutuyor. Bu yüzden 132 bayt.

Bir sütunu indeks yaparsan durum değişebilir:

```python
from orders_data import make_orders

df = make_orders(100_000)
a = df.set_index("order_id")
b = df.set_index("customer_id")
print(type(a.index).__name__, a.memory_usage(deep=True)["Index"])
print(type(b.index).__name__, b.memory_usage(deep=True)["Index"])
```

```text
RangeIndex 132
Index 800000
```

`order_id` 1, 2, 3, … diye düzenli artıyor; pandas bunu fark edip yine
`RangeIndex` kuruyor. `customer_id` ise karışık sayılar; her biri ayrı ayrı
saklanıyor: satır başına 8 bayt. İndeksi seçerken bu da hesaba katılmalı.

## İşlemler yeni bellek açar

Tablo üzerinde yaptığın her işlem bellekte iz bırakıyor. Küçük bir ölçüm
fonksiyonu yazıp adım adım bakalım:

```python
def mb(frame):
    return round(frame.memory_usage(deep=True).sum() / 1024**2, 1)

df = pd.read_csv("orders.csv")
print("start:   ", mb(df))
df["total"] = df["quantity"] * df["unit_price"]
print("+ total: ", mb(df))
istanbul = df[df["city"] == "Istanbul"]
print("istanbul:", mb(istanbul), len(istanbul))
copy = df.copy()
print("copy:    ", mb(copy))
```

```text
start:    9.6
+ total:  10.4
istanbul: 3.9 34196
copy:     10.4
```

- Yeni bir sayı sütunu: satır başına 8 bayt daha (9,6 → 10,4 MB).
- Süzme (`df[...]`) **yeni bir tablo** üretiyor: İstanbul siparişleri 3,9 MB
  daha. `df` de bellekte durmaya devam ediyor.
- `copy()` tablonun tamamını bir kez daha kuruyor.

Buradan çıkan önemli bir kavram var: **tepe bellek** (*peak memory*). Bir
işlemin sonunda tablo küçük olsa bile işlem **sürerken** eskisi ile yenisi
aynı anda bellekte duruyor. Bir programın çöküp çökmeyeceğini sondaki
boyut değil, bu tepe belirliyor.

<figure class="fig">
  <div class="flow">
    <span class="node"><code>a</code> kuruldu<br>7,6 MB</span><span class="arrow">→</span>
    <span class="node acc"><code>b = a * 2</code><br>ikisi birden: 15,3 MB</span><span class="arrow">→</span>
    <span class="node"><code>del a</code><br>yalnızca <code>b</code>: 7,6 MB</span>
  </div>
  <figcaption>Sondaki kullanım 7,6 MB ama tepe 15,3 MB. Bilgisayarın belleği 10 MB olsaydı program ortadaki adımda çökerdi.</figcaption>
</figure>

## Tepeyi yakalamak: `tracemalloc`

Python'un standart kütüphanesindeki `tracemalloc` modülü, açıldığı andan
itibaren ayrılan belleği izliyor ve iki sayı veriyor: **şu anki** kullanım ve
o ana kadarki **tepe**.

```python
import tracemalloc
import numpy as np

tracemalloc.start()
a = np.arange(1_000_000)
b = a * 2
del a
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(round(current / 1024**2, 1), round(peak / 1024**2, 1))
```

```text
7.6 15.3
```

Sonda yalnızca `b` kaldı: 7,6 MB. Ama `a * 2` hesaplanırken `a` da bellekteydi;
tepe iki dizinin toplamı, 15,3 MB. `del a` bir adı siliyor; o nesneyi
kullanan başka bir ad kalmadıysa belleği de serbest bırakıyor.

Adımlar:

1. `tracemalloc.start()`: izlemeyi başlat.
2. Ölçmek istediğin kodu çalıştır.
3. `tracemalloc.get_traced_memory()`: `(şu an, tepe)` ikilisi, bayt.
4. `tracemalloc.stop()`: izlemeyi kapat (izleme kodu biraz yavaşlatıyor).

> **Dikkat:** `tracemalloc` yalnızca Python'un kendi bellek yöneticisinden
> geçen ayırmaları görüyor: Python nesneleri ve NumPy dizileri. pandas 3'ün
> `str` sütunları ise ayrı bir kütüphanenin (Arrow) belleğinde duruyor ve
> `tracemalloc` onları saymıyor. Bir tablonun boyutu için
> `memory_usage(deep=True)`, bir işlemin tepesi için `tracemalloc` kullan.

## Süreyi ölçmek

Büyük veride bellek kadar **süre** de önemli. Python'da bir kod parçasının
ne kadar sürdüğünü `time.perf_counter()` ile ölçüyorsun: işten önce ve sonra
saati okuyup farkı alıyorsun.

```python
import time

start = time.perf_counter()
df = pd.read_csv("orders.csv")
print(round(time.perf_counter() - start, 2), "s")

start = time.perf_counter()
df = pd.read_csv("orders.csv", usecols=["city", "unit_price"])
print(round(time.perf_counter() - start, 2), "s")
```

Bir milyon satırlık dosyada bu bilgisayarda ilk okuma 0,84 saniye,
yalnızca iki sütunu okumak (`usecols`) 0,32 saniye sürdü. Senin
bilgisayarında sayılar farklı çıkacak; süre işlemciye, diske ve o anda
çalışan diğer programlara bağlı. Bu yüzden:

- Süreyi **birkaç kez** ölç; ilk çalıştırma çoğu zaman daha yavaş.
- İki yolu **aynı bilgisayarda, art arda** karşılaştır.
- Mutlak sayıya değil, **orana** bak: "üçte biri kadar sürdü".

`usecols` ile yalnızca gereken sütunları okumak hem süreyi hem belleği
düşürüyor. Bölüm 3'te ayrıntısıyla göreceğiz.

## Ölçüm alışkanlığı

Yeni bir veriyle karşılaştığında:

1. `df.info(memory_usage="deep")`: genel resim.
2. `df.memory_usage(deep=True)`: hangi sütun pahalı?
3. Satır başına bayt: metin sütunları 8'den ne kadar fazla?
4. Ağır bir işlemden önce: tepe ne olacak? Bellekte aynı anda kaç kopya
   duracak?

## Özet

- `df.info(memory_usage="deep")` tablonun özetini ve gerçek boyutunu
  veriyor.
- `df.memory_usage(deep=True)` sütun başına bayt; `Index` satırı indeksin
  payı.
- Sayı sütunu satır başına 8 bayt; `str` sütunu karakter sayısı + 8 bayt.
  Bu tabloda metin sütunları belleğin %68'i.
- `deep=True` asıl `object` sütunlarında fark ediyor: onsuz yalnızca
  adresler sayılıyor.
- `RangeIndex` neredeyse yer tutmuyor; karışık sayılardan indeks satır
  başına 8 bayt.
- Süzme ve `copy()` yeni tablo üretiyor. Çöküp çökmemeyi sondaki boyut
  değil **tepe bellek** belirliyor; `tracemalloc` ile ölçülüyor.
- Süreyi `time.perf_counter()` ile ölç, karşılaştırmayı aynı bilgisayarda
  yap.
