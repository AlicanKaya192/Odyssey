# Bölümlenmiş Veri

Geçen bölümde Parquet'nin bir dosyanın **içindeki** satır gruplarını
istatistiklerle atladığını gördük. Bölümleme (*partitioning*) aynı fikri bir
adım öteye taşıyor: veriyi bir sütunun değerine göre **ayrı dosyalara ve
klasörlere** ayırıyorsun. Okuyan program hangi dosyaya ihtiyaç olduğunu
dosyayı açmadan, yalnızca **klasör adına** bakarak anlıyor.

Büyük veri sistemlerinin neredeyse hepsi veriyi böyle saklıyor: bir şirketin
yıllarca biriken satışları tek dosyada değil, gün ya da ay klasörlerinde
duruyor.

Örnekler bir milyon siparişle çalışıyor; her siparişin ayını bir sütuna
alıyoruz:

```python
from pathlib import Path
import pandas as pd
from orders_data import make_orders

df = make_orders(1_000_000)
df["order_time"] = pd.to_datetime(df["order_time"])
df["month"] = df["order_time"].dt.strftime("%Y-%m")
```

## Klasör düzeni

Aya göre bölünmüş bir veri diskte şöyle görünüyor:

<figure class="fig">
<pre><code class="language-text">orders/
├─ month=2024-01/
│  └─ part-0.parquet
├─ month=2024-02/
│  └─ part-0.parquet
├─ month=2024-03/
│  └─ part-0.parquet
└─ ... (12 klasör)</code></pre>
  <figcaption>Her ay kendi klasöründe. Klasör adı <code>month=2024-03</code>, içindeki her satırın ayını söylüyor; ay sütunu dosyaların içinde yok.</figcaption>
</figure>

Klasör adları `sütun=değer` biçiminde: `month=2024-03`. Bu yazım Hadoop
dünyasındaki Hive aracından geliyor ve bugün neredeyse her araç tanıyor
(pandas, Spark, DuckDB). Klasörün adı o klasördeki bütün satırlar için bir
bilgi taşıyor: "buradaki her sipariş Mart 2024'te".

## Elle bölmek

Bölmenin mekanizmasını görmek için önce kendimiz yapalım: `groupby` ile aylara
ayır, her ayı kendi klasörüne yaz.

```python
for month, part in df.groupby("month"):
    folder = Path("orders") / f"month={month}"
    folder.mkdir(parents=True, exist_ok=True)
    part.drop(columns="month").to_parquet(folder / "part-0.parquet", index=False)

files = sorted(Path("orders").rglob("*.parquet"))
print(len(files))
for f in files[:3]:
    print(f.as_posix(), round(f.stat().st_size / 1024**2, 2))
```

```text
12
orders/month=2024-01/part-0.parquet 2.22
orders/month=2024-02/part-0.parquet 2.08
orders/month=2024-03/part-0.parquet 2.22
```

- `groupby("month")` her ay için `(ay, o ayın satırları)` ikilisi veriyor.
- `Path("orders") / f"month={month}"` klasörün yolunu kuruyor;
  `mkdir(parents=True, exist_ok=True)` klasörü (ve gerekiyorsa üstlerini)
  açıyor, varsa hata vermiyor.
- `month` sütununu dosyaya koymuyoruz: bilgi zaten klasörün adında.
- `rglob("*.parquet")` klasörün içindeki bütün Parquet dosyalarını, alt
  klasörler dahil buluyor.

On iki dosyanın toplamı 26,2 MB; aynı veri tek dosyada 20,9 MB'tı. Her dosya
kendi sözlüğünü ve altbilgisini taşıdığı için bölmenin biraz yer bedeli var.

## Yalnızca gereken klasörü okumak

Mart siparişleri lazım. Bölümlenmiş veride yalnızca bir dosya açılıyor; tek
dosyada ise hepsi okunup süzülüyor:

```python
march = pd.read_parquet("orders/month=2024-03/part-0.parquet")

whole = pd.read_parquet("all.parquet")
march2 = whole[whole["order_time"].dt.month == 3]
```

İkisi de 84 836 sipariş veriyor. Bu bilgisayarda ilki 0,009 saniye, ikincisi
0,077 saniye sürdü: yaklaşık **sekiz kat**. Veri büyüdükçe okunmayan kısım da
büyüyor; bir ayı istediğin sürece okuduğun hep bir ay.

Bu atlamaya **bölüm budama** (*partition pruning*) deniyor: koşula uymayan
bölümler, dosyaları açılmadan, yalnızca adlarına bakılarak eleniyor.

<figure class="fig">
  <div class="flow">
    <span class="node">Koşul<br><code>month = 2024-03</code></span><span class="arrow">→</span>
    <span class="node">Klasör adlarına bak</span><span class="arrow">→</span>
    <span class="node">11 klasörü ele</span><span class="arrow">→</span>
    <span class="node acc">Tek dosyayı oku</span>
  </div>
  <figcaption>Bölüm budama: elenen klasörlerdeki dosyalar hiç açılmıyor.</figcaption>
</figure>

## pandas'a bıraktırmak: `partition_cols`

Elle bölmek mekanizmayı gösteriyor; günlük işte `to_parquet` bunu kendisi
yapabiliyor:

```python
df.to_parquet("by_month", partition_cols=["month"], index=False)
```

```text
by_month/month=2024-01/b4ee06afe85b42749f2cd20b49999f3c-0.parquet
by_month/month=2024-02/...
```

Dosya adları rastgele (her yazışta farklı); klasör adları aynı düzende.
Okurken klasörün kendisini vermek yetiyor ve `filters=` bölüm budamayı
kendisi yapıyor:

```python
back = pd.read_parquet("by_month")
march = pd.read_parquet("by_month", filters=[("month", "==", "2024-03")])
```

`back` tablosunda `month` sütunu geri geliyor; pandas onu klasör adlarından
kurup `category` yapıyor.

`partition_cols` ve klasör okuma da geçen bölümdeki `filters=` gibi arkada
`pyarrow.dataset` modülünü kullanıyor. O modülün yüklenemediği bir kurulumda
bu yazımlar hata veriyor; o zaman bölümdeki elle yöntem her yerde çalışıyor.

## Ne kadar ince bölmeli?

Aya göre 12 dosya iyi gitti. Güne göre bölsek?

| Bölme | Dosya | Toplam | Hepsini okumak |
|---|---|---|---|
| Tek dosya | 1 | 20,9 MB | 0,069 sn |
| Aya göre | 12 | 26,2 MB | — |
| Güne göre | 366 | 28,1 MB | 1,09 sn |

366 küçük dosyanın hepsini okumak tek dosyadan **on beş kat** yavaş: her
dosyanın açılması, altbilgisinin okunması, sonuçların birleştirilmesi ayrı
bir iş. Bu büyük veri dünyasının bilinen sorunu: **çok küçük dosya** (*small
files problem*). Müşteriye göre bölmeye kalksak 245 461 klasör olurdu.

Bölüm sütunu seçerken:

1. **Sık süzdüğün** bir sütun olsun (zaman, ülke, kaynak).
2. **Az sayıda farklı değeri** olsun: onlarca, en fazla birkaç bin.
3. Her bölüm **yeterince büyük** olsun. Büyük sistemlerde yaygın öneri dosya
   başına onlarca – yüzlerce megabayt.

Bir milyon siparişlik bir tablo için ay fazlasıyla yeterli; milyarlarca
satırda gün ya da saat uygun hâle geliyor.

## Yeni veriyi eklemek

Bölümlemenin bir kazancı daha var: yeni ay geldiğinde **yalnızca yeni bir
klasör** ekliyorsun, eski dosyalara dokunmuyorsun. `january_2025` Ocak 2025
siparişlerinin tablosu olsun:

```python
folder = Path("orders") / "month=2025-01"
folder.mkdir(parents=True, exist_ok=True)
january_2025.to_parquet(folder / "part-0.parquet", index=False)
```

Son iki ayı okumak için klasör adlarına bakıp ayın kendisini adından geri
kuruyoruz:

```python
parts = []
for f in sorted(Path("orders").glob("month=*/*.parquet")):
    month = f.parent.name.split("=")[1]
    if month >= "2024-12":
        p = pd.read_parquet(f)
        p["month"] = month
        parts.append(p)
recent = pd.concat(parts, ignore_index=True)
print(recent.groupby("month").size().to_dict())
```

```text
{'2024-12': 85002, '2025-01': 6750}
```

- `f.parent.name` dosyanın bulunduğu klasörün adı: `month=2024-12`.
- `split("=")[1]` eşittirden sonrasını alıyor: `2024-12`.
- `"2024-12" >= "2024-12"`: `YYYY-MM` biçiminde yazılmış aylar metin olarak
  da doğru sıralanıyor.

Ay sütunu dosyalarda yoktu; klasör adından geri koyduk. `partition_cols` ile
okurken pandas aynı işi kendisi yapıyor.

## Kovalara bölmek

Müşteriye göre süzmek de sık bir iş: "1234 numaralı müşterinin bütün
siparişleri". Ama 245 461 müşteri klasör açmak için fazla. Çözüm: müşteri
numarasını **sabit sayıda kovaya** dağıtmak.

```python
df["bucket"] = df["customer_id"] % 8
print(df["bucket"].value_counts().sort_index().tolist())
```

```text
[124749, 124952, 124796, 125218, 125315, 124915, 125034, 125021]
```

`%` bölümden kalanı veriyor: her müşteri 0 ile 7 arasında tek bir kovaya
düşüyor ve kovalar neredeyse eşit büyüklükte. Bir müşterinin bütün
siparişleri **aynı kovada**; onları bulmak için sekiz dosyadan yalnızca biri
okunuyor (`1234 % 8 = 2` → 2 numaralı kova). Bu yönteme **kovalama**
(*bucketing* ya da *hash partitioning*) deniyor; Spark ve veri ambarları da
kullanıyor.

## Özet

- Bölümleme veriyi bir sütunun değerine göre ayrı klasörlere ayırıyor:
  `orders/month=2024-03/part-0.parquet`.
- Okurken koşula uymayan klasörler açılmadan eleniyor (**bölüm budama**);
  bu ölçümde bir ayı okumak sekiz kat hızlıydı.
- Elle: `groupby` + her parçayı kendi klasörüne `to_parquet`. pandas'a
  bıraktırmak: `to_parquet(..., partition_cols=[...])` ve
  `read_parquet(klasör, filters=...)`.
- Bölüm sütunu sık süzülen ve az değerli olmalı; çok ince bölmek **çok küçük
  dosya** sorununa yol açıyor (366 dosya, on beş kat yavaş).
- Yeni veri yeni klasör olarak ekleniyor; eskiler yeniden yazılmıyor.
- Çok değerli sütunlar için sabit sayıda kova: `customer_id % 8`.
