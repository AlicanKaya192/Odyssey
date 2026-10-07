# Dosya Biçimleri

Şimdiye kadar veriyi hep CSV'den okuduk. CSV her yerde var ve her program
açabiliyor, ama büyük veride en pahalı biçimlerden biri. Bu bölümde aynı bir
milyon siparişi beş farklı biçimde diske yazıp karşılaştıracağız. Sonuçlar
arasındaki fark çarpıcı: dosya boyutu 159 MB ile 14 MB arasında, okuma süresi
3 saniye ile birkaç yüzde bir saniye arasında değişiyor.

Karşılaştırmada kullandığımız tablo, geçen bölümdeki gibi doğru türlerle
hazırlanmış bir milyon sipariş:

```python
import pandas as pd
from orders_data import make_orders

df = make_orders(1_000_000)
df["order_time"] = pd.to_datetime(df["order_time"])
for c in ["city", "category", "payment"]:
    df[c] = df[c].astype("category")
```

## CSV: herkesin konuştuğu dil

CSV (*comma-separated values*) düz bir metin dosyası: her satır bir kayıt,
değerler virgülle ayrılmış, ilk satır sütun adları.

```python
make_orders(3).to_csv("o.csv", index=False)
print(open("o.csv").read())
```

```text
order_id,order_time,customer_id,city,category,quantity,unit_price,payment
1,2024-01-02 22:15:01,8,Ankara,toys,3,234.3,card
2,2024-07-01 22:07:37,2,Istanbul,clothing,1,443.5,card
3,2024-11-30 00:28:55,8,Istanbul,clothing,5,367.51,transfer
```

**Güçlü yanları:** Not Defteri'nde bile açılıyor, her dil ve her program
okuyabiliyor, gözle kontrol edilebiliyor.

**Zayıf yanları:**

1. **Her okumada metin çözülüyor.** `"234.3"` yazısının bir sayıya
   çevrilmesi gerekiyor; bir milyon satırda sekiz sütun için sekiz milyon
   kez.
2. **Türler kayboluyor.** CSV'de yalnızca metin var; tarih mi, kategori mi,
   bilmiyor. Tabloyu yazıp geri okuyalım:

```python
df.to_csv("orders.csv", index=False)
back = pd.read_csv("orders.csv")
print(df["order_time"].dtype, df["city"].dtype)
print(back["order_time"].dtype, back["city"].dtype)
```

```text
datetime64[us] category
str str
```

   Tarih ve kategori yazarken metne dönüştü, okurken de metin olarak kaldı.
   Geçen bölümde verdiğin türleri her okumada yeniden vermen gerekiyor.

3. **Satır satır dizili.** Yalnızca iki sütun istesen bile dosyanın her
   satırını baştan sona okuyup ayırmak gerekiyor.

## Sıkıştırılmış CSV

Dosya adının sonuna `.gz` eklersen pandas dosyayı **gzip** ile sıkıştırıp
yazıyor, okurken de kendisi açıyor:

```python
df.to_csv("orders.csv.gz", index=False)
back = pd.read_csv("orders.csv.gz")
```

Dosya 61,1 MB'tan 15,2 MB'a indi. Ama yazmak 1,3 saniyeden 3,5 saniyeye
çıktı ve okuma biraz yavaşladı: önce açmak, sonra yine metni çözmek gerekiyor.
Disk ya da ağ darsa iyi bir seçim; türler ve satır düzeni sorunu ise aynen
duruyor.

## JSON Lines: iç içe veri için

JSON Lines (`.jsonl`) her satıra bir JSON nesnesi yazıyor:

```python
small = make_orders(3)[["order_id", "city", "unit_price"]]
small.to_json("o.jsonl", orient="records", lines=True)
print(open("o.jsonl").read())
```

```text
{"order_id":1,"city":"Ankara","unit_price":234.3}
{"order_id":2,"city":"Istanbul","unit_price":443.5}
{"order_id":3,"city":"Istanbul","unit_price":367.51}
```

API'lerden gelen veri, uygulama kayıtları (*log*) ve iç içe yapılar
(bir siparişin içinde ürün listesi gibi) çoğu zaman bu biçimde. Okumak için
`pd.read_json("o.jsonl", lines=True)`.

Bedeli: her satırda **sütun adları tekrar ediyor**. Bir milyon siparişte
dosya 159,3 MB, CSV'nin iki buçuk katı; okuması da en yavaşı (3,25 saniye).

## Satır mı, sütun mu?

Asıl fark dosyanın **dizilişinde**. CSV ve JSON satır satır diziyor: önce
birinci siparişin bütün değerleri, sonra ikincininki. Sütunlu (*columnar*)
biçimler ise sütun sütun diziyor: önce bütün `order_id` değerleri, sonra
bütün `city` değerleri.

<figure class="fig">
  <div class="versus">
    <div><h4>Satır düzeni (CSV, JSON)</h4><p><code>1, 2024-01-02, Ankara, toys, 3, 234.3</code><br><code>2, 2024-07-01, Istanbul, clothing, 1, 443.5</code><br><code>3, 2024-11-30, Istanbul, clothing, 5, 367.51</code><br>İki sütun için bile bütün satırlar okunuyor.</p></div>
    <div class="ok"><h4>Sütun düzeni (Parquet)</h4><p><code>order_id</code>: 1, 2, 3, …<br><code>city</code>: Ankara, Istanbul, Istanbul, …<br><code>unit_price</code>: 234.3, 443.5, 367.51, …<br>Yalnızca istenen sütunlar okunuyor.</p></div>
  </div>
  <figcaption>Aynı üç sipariş iki dizilişte. Sütun düzeninde benzer değerler yan yana durduğu için iyi sıkışıyor.</figcaption>
</figure>

Bu dizilişin iki büyük kazancı var:

1. **Yalnızca gereken sütunlar okunuyor.** "Şehir başına ortalama fiyat"
   için iki sütun yeter; diğer altısının olduğu yere hiç dokunulmuyor.
2. **Benzer değerler yan yana.** Bir sütundaki değerler aynı türde ve
   çoğu zaman birbirine benziyor (`Istanbul`, `Istanbul`, `Ankara`, …);
   böyle bir dizi çok iyi sıkışıyor.

Analiz işlerinin çoğu "birkaç sütun, çok satır" sorusu sorduğu için büyük
veride sütunlu biçim neredeyse her zaman kazanıyor.

## Parquet

Parquet en yaygın sütunlu dosya biçimi: Spark, DuckDB, veri ambarları ve
bulut depolama sistemleri doğrudan okuyor. pandas'ta yazmak ve okumak tek
satır (arkada `pyarrow` kütüphanesi çalışıyor):

```python
df.to_parquet("orders.parquet")
back = pd.read_parquet("orders.parquet")
print(back["order_time"].dtype, back["city"].dtype)
```

```text
datetime64[us] category
```

Türler korundu: tarih tarih, kategori kategori olarak geri geldi. Parquet
dosyası her sütunun türünü kendi içinde saklıyor.

Yalnızca birkaç sütun okumak için `columns=`:

```python
prices = pd.read_parquet("orders.parquet", columns=["city", "unit_price"])
```

Parquet ikili (*binary*) bir dosya: Not Defteri'nde açınca anlamsız
karakterler görürsün. İnsan değil program okusun diye tasarlandı.

### Sıkıştırma

Parquet varsayılan olarak her sütunu **snappy** ile sıkıştırıyor: hızlı,
orta düzeyde sıkıştırma. Daha küçük dosya için **zstd**:

```python
df.to_parquet("orders_zstd.parquet", compression="zstd")
```

Snappy ile 20,9 MB, zstd ile 13,9 MB. İkisinin de okuma süresi bu
ölçümde aynıydı.

## Feather

Feather (Arrow IPC biçimi), tabloyu bellekteki düzenine çok yakın bir
biçimde diske yazıyor. Yazması ve okuması çok hızlı:

```python
df.to_feather("orders.feather")
back = pd.read_feather("orders.feather")
```

İki Python programı arasında ya da bir işin adımları arasında geçici ara
dosya olarak kullanışlı. Başka araçlarla paylaşılacak ya da uzun süre
saklanacak veri için Parquet daha yaygın.

## Excel neden değil?

Excel dosyası (`.xlsx`) tablo paylaşmanın en tanıdık yolu ama büyük veri
için uygun değil: bir sayfada en fazla 1 048 576 satır olabiliyor, okuması ve
yazması CSV'den bile yavaş. Bir milyon siparişimiz bu sınırın hemen altında.

## Karşılaştırma

Aynı bir milyon sipariş, bu bilgisayarda:

| Biçim | Boyut | Yazma | Okuma | İki sütun okuma |
|---|---|---|---|---|
| CSV | 61,1 MB | 1,3 sn | 0,84 sn | 0,32 sn |
| CSV + gzip | 15,2 MB | 3,5 sn | 0,92 sn | — |
| JSON Lines | 159,3 MB | 1,6 sn | 3,25 sn | — |
| Parquet (snappy) | 20,9 MB | 0,18 sn | 0,02 sn | 0,01 sn |
| Parquet (zstd) | 13,9 MB | 0,22 sn | 0,02 sn | — |
| Feather | 22,2 MB | 0,03 sn | 0,02 sn | — |

Okuma süreleri üç denemenin en hızlısı. Senin bilgisayarında sayılar farklı
olacak, ama oranlar benzer kalacak: Parquet CSV'den birkaç kat değil,
**onlarca kat** hızlı okunuyor (0,84 saniyeye karşı 0,02 saniye).

Neden bu kadar fark? CSV'de her değer metinden çözülüyor. Parquet'de değerler
zaten sayı olarak, sütun sütun ve türüyle birlikte duruyor; okuma büyük ölçüde
diskten belleğe kopyalamaktan ibaret.

## Hangisi ne zaman?

- **CSV:** veri başka birine, başka bir programa ya da bir insana
  gidecekse; küçükse.
- **CSV + gzip:** CSV gerekiyor ama dosya büyük ve disk/ağ dar.
- **JSON Lines:** veri iç içe yapıdaysa ya da bir API'den, kayıt
  dosyasından öyle geliyorsa.
- **Parquet:** büyük veri saklamak, analiz etmek ve başka büyük veri
  araçlarıyla paylaşmak için varsayılan seçim.
- **Feather:** aynı makinede, programlar arasında hızlı ara dosya.

Bu patikanın geri kalanında veriyi çoğunlukla Parquet olarak tutacağız.

## Özet

- CSV metin, satır satır ve türsüz: her okumada metin çözülüyor, tarih ve
  kategori kayboluyor.
- `.gz` uzantısı CSV'yi dörtte birine indiriyor ama yazmayı yavaşlatıyor.
- JSON Lines iç içe veri için uygun; sütun adları her satırda tekrar
  ettiği için en büyük dosya.
- Sütunlu biçim yalnızca gereken sütunları okuyor ve benzer değerleri yan
  yana koyduğu için iyi sıkışıyor.
- Parquet türleri saklıyor, `columns=` ile sütun seçiyor, snappy ya da zstd
  ile sıkışıyor; bu ölçümde okuma CSV'den onlarca kat hızlı.
- Feather hızlı ara dosya; Excel büyük veri için değil.
