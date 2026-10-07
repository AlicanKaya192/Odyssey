# Büyük Veri Nedir?

Veri Bilimi patikasında her şey aynı yoldan geçiyordu: dosyayı
`pd.read_csv` ile oku, tabloyla çalış. Dosya birkaç megabayt olduğu sürece
bu yol kusursuz. Peki dosya 50 gigabayt olursa?

Çoğu zaman program **çöker** ya da bilgisayar dakikalarca donar. Kodda
hata yok; sorun, verinin bilgisayarın **belleğine sığmaması**.

Bu patika tam o anı anlatıyor: veri, elindeki araçların rahatça
taşıyabileceğinden büyük olduğunda ne yapılır? Bu ilk bölümde hiçbir yeni
araç öğrenmiyoruz. Önce sorunun kendisini anlıyoruz: bellek nedir, bir tablo
orada ne kadar yer tutar, "büyük" tam olarak ne demek?

## "Büyük" kime göre büyük?

Büyük verinin sabit bir sınırı yok. "1 milyon satırdan sonrası büyüktür"
gibi bir kural yok. Kullanışlı tanım şu:

> Veri, onu işlemek istediğin makinenin ve aracın **rahatça
> taşıyabileceğinden fazlaysa** büyüktür.

Aynı 20 GB'lık dosya 8 GB belleği olan bir dizüstü bilgisayar için büyük,
256 GB belleği olan bir sunucu için sıradan. Aynı dosya pandas için zor,
bir veritabanı için kolay olabilir. Yani soru hep şu: **bu veri, bu makinede,
bu araçla** sorun çıkarıyor mu?

Bu yüzden patika boyunca tek bir "büyük veri aracı" öğrenmeyeceksin. Bir
alet çantası öğreneceksin: veriyi küçültmek, parça parça işlemek, daha iyi
bir dosya biçimine geçmek, işi veriye götürmek, işi birden çok çekirdeğe ya
da makineye bölmek.

## Bellek ve disk

Bilgisayarında veri iki ayrı yerde durabilir:

- **Disk** (SSD ya da sabit disk): dosyaların durduğu yer. Büyük ve
  kalıcı; bilgisayar kapanınca da veri orada. Bugünün dizüstü
  bilgisayarlarında genellikle 512 GB ya da 1 TB.
- **Bellek** (RAM): programın **o anda** üzerinde çalıştığı yer. Küçük ve
  geçici; program kapanınca boşalıyor. Genellikle 8, 16 ya da 32 GB.

Bir benzetme: disk bir kütüphanenin rafları, bellek ise çalışma masan. Kitap
okumak için onu raftan alıp masaya koyman gerekiyor. Masa raflardan çok daha
küçük ama elinin altında; bir sayfaya masada bakmak, her seferinde rafa
yürümekten kat kat hızlı.

<figure class="fig">
  <div class="versus">
    <div class="ok"><h4>Bellek (RAM)</h4><p>Çalışma masası<br>Genellikle 8–32 GB<br>Çok hızlı<br>Program kapanınca boşalır</p></div>
    <div><h4>Disk (SSD)</h4><p>Kütüphane rafları<br>Genellikle 512 GB – 1 TB<br>Bellekten yavaş<br>Kalıcı</p></div>
  </div>
  <figcaption>pandas çalışmak için tabloyu diskten belleğe taşıyor. Masa raflardan çok küçük: büyük veri sorunu çoğu zaman bir "masaya sığmama" sorunu.</figcaption>
</figure>

`pd.read_csv("orders.csv")` yazdığında pandas dosyanın **tamamını** diskten
okuyup belleğe koyuyor. Tablo masaya sığıyorsa sorun yok. Sığmıyorsa iki
şeyden biri oluyor:

1. Python bellek ayıramıyor ve `MemoryError` hatası veriyor.
2. Windows, belleğin bir kısmını diske taşıyarak yer açmaya çalışıyor
   (buna *sayfa dosyası* deniyor). Program çökmüyor ama disk bellekten çok
   yavaş olduğu için bilgisayar sürünmeye başlıyor.

Odyssey'de alıştırmalar en fazla **3 GB** bellek kullanabiliyor; kodun bunu
aşarsa çalıştırma durduruluyor ve terminal bunu söylüyor. Bu patikadaki
alıştırmalar bu sınırın çok altında kalıyor, ama sınırın varlığı iyi bir
hatırlatma: bellek sonsuz değil.

## Bayt, kilobayt, megabayt

Bellekteki ve diskteki her şey **bayt** ile ölçülüyor. Bir bayt, 0 ile 255
arasında bir sayı tutabilen en küçük birim. Daha büyük birimler 1024'er
katla büyüyor:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>1 bayt</span><span>0 ile 255 arasında bir sayı</span></div>
    <div class="anat-row"><span>1 KB</span><span>1024 bayt: kısa bir metin</span></div>
    <div class="anat-row"><span>1 MB</span><span>1024 KB: bir fotoğraf, binlerce satırlık bir tablo</span></div>
    <div class="anat-row"><span>1 GB</span><span>1024 MB: bir film, on milyonlarca satır</span></div>
    <div class="anat-row"><span>1 TB</span><span>1024 GB: bir şirketin yıllarca biriken kayıtları</span></div>
  </div>
  <figcaption>Her basamak bir öncekinin 1024 katı: bayttan gigabayta üç basamak, 1024 × 1024 × 1024.</figcaption>
</figure>

Neden 1000 değil de 1024? Bilgisayar ikili sayı sistemiyle çalışıyor ve
1024, 2'nin 10. kuvveti. Bu patikada da Windows'un yaptığını yapıp 1 MB'ı
1024 × 1024 bayt sayıyoruz. Kodda bu `1024**2` olarak yazılıyor:

```python
size_in_bytes = 5_000_000
print(size_in_bytes / 1024**2, "MB")
```

```text
4.76837158203125 MB
```

> Disk üreticileri ise 1 GB'ı 1 000 000 000 bayt sayıyor. "1 TB" diye
> satılan diskin Windows'ta 931 GB görünmesinin sebebi bu: ikisi aynı
> miktarı farklı birimle söylüyor.

## Bir sayı bellekte ne kadar yer tutar?

pandas ve NumPy sayıları sabit genişlikte saklıyor. En sık gördüğün iki tür:

- `int64`: tam sayı, **8 bayt**
- `float64`: ondalıklı sayı, **8 bayt**

Bu, bir tablonun ne kadar yer tutacağını kâğıt üzerinde hesaplayabileceğin
anlamına geliyor. 10 milyon satırlık, 6 sayı sütunlu bir tablo:

```python
rows = 10_000_000
columns = 6
size = rows * columns * 8
print(size / 1024**2, "MB")
print(round(size / 1024**3, 2), "GB")
```

```text
457.763671875 MB
0.45 GB
```

Yarım gigabayt. 16 GB belleği olan bir bilgisayar için sorun değil. Ama aynı
tablo 1 milyar satır olsaydı 45 GB'ı geçerdi.

## Python listesi ile NumPy dizisi

Aynı bir milyon sayıyı iki farklı şekilde saklayıp ölçelim:

```python
import sys
import numpy as np

numbers = list(range(1_000_000))
array = np.arange(1_000_000)

list_mb = (sys.getsizeof(numbers) + sum(sys.getsizeof(x) for x in numbers)) / 1024**2
array_mb = array.nbytes / 1024**2
print(f"list:  {list_mb:.1f} MB")
print(f"array: {array_mb:.1f} MB")
```

```text
list:  34.3 MB
array: 7.6 MB
```

Liste **dört buçuk kat** fazla yer tutuyor. Sebebi şu: Python listesinde
her sayı ayrı bir nesne. Her nesnenin kendi başlığı var (türü, kaç yerden
kullanıldığı gibi bilgiler) ve liste bu nesnelerin yalnızca **adresini**
tutuyor. NumPy dizisi ise sayıları yan yana, başlıksız diziyor: her sayı tam
8 bayt.

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>Python listesi</h4><p>Liste yalnızca adres tutuyor: sayı başına 8 bayt<br>Her sayı ayrı bir nesne: 28 bayt<br><b>Sayı başına yaklaşık 36 bayt</b></p></div>
    <div class="ok"><h4>NumPy dizisi</h4><p>Sayılar yan yana, başlıksız<br><code>int64</code>: 8 bayt<br><b>Sayı başına 8 bayt</b></p></div>
  </div>
  <figcaption>Bir milyon sayıda 34,3 MB'a karşı 7,6 MB. pandas sütunları NumPy dizisine benzer biçimde saklıyor.</figcaption>
</figure>

`sys.getsizeof(x)` bir nesnenin bayt cinsinden boyutunu veriyor. Listenin
kendi boyutuna yalnızca adresler dahil; içindeki sayıları ayrıca topladık.
pandas'ın büyük veride Python listelerinden çok daha iyi olmasının bir sebebi
bu: sütunları NumPy dizileri gibi sıkı saklıyor.

## Dosya boyutu bellekteki boyutu söylemiyor

Bu patikada sık kullanacağımız veri, bir mağazanın 2024 siparişleri.
Alıştırmalarda yanında salt okunur bir `orders_data.py` dosyası olacak; içindeki
`make_orders(n)` her seferinde **aynı** `n` satırı üretiyor. Böylece büyük
dosyaları indirmek gerekmiyor, herkes aynı tabloyu kendi bilgisayarında
üretiyor.

```python
import pandas as pd
from orders_data import make_orders

df = make_orders(5)
print(df.iloc[:, :4].to_string(index=False))
print()
print(df.iloc[:, 4:].to_string(index=False))
```

```text
 order_id          order_time  customer_id    city
        1 2024-04-11 21:41:26            3   Izmir
        2 2024-04-20 21:50:12            9 Trabzon
        3 2024-05-05 00:38:40            5 Antalya
        4 2024-09-20 07:49:57            5   Izmir
        5 2024-10-25 19:49:47            5 Trabzon

   category  quantity  unit_price  payment
       toys         2      226.16     card
   clothing         1      531.06     card
   clothing         4      831.23     card
electronics         1     2020.20     card
electronics         4     1931.51 transfer
```

Tablo geniş olduğu için iki parça hâlinde yazdırdık: önce ilk dört sütun, sonra son dört.

Şimdi bir milyon siparişi CSV dosyasına yazıp geri okuyalım ve iki boyutu
karşılaştıralım:

```python
import os
import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 1_000_000)
df = pd.read_csv("orders.csv")

file_mb = os.path.getsize("orders.csv") / 1024**2
memory_mb = df.memory_usage(deep=True).sum() / 1024**2
print(f"rows:   {len(df):,}")
print(f"file:   {file_mb:.1f} MB")
print(f"memory: {memory_mb:.1f} MB")
```

```text
rows:   1,000,000
file:   61.1 MB
memory: 95.9 MB
```

İki yeni araç var:

- `os.path.getsize(yol)`: diskteki dosyanın bayt cinsinden boyutu.
- `df.memory_usage(deep=True)`: her sütunun bellekte kaç bayt tuttuğu;
  `.sum()` ile tablonun tamamı. `deep=True` metin sütunlarının içine de
  bakılmasını sağlıyor (bir sonraki bölümde ayrıntısıyla).

61 MB'lık dosya bellekte 96 MB oldu. Dosya boyutu, verinin bellekte ne kadar
tutacağını **söylemiyor**; ölçmek gerekiyor.

### Aynı tablo, iki ayrı saklama

pandas'ın eski sürümleri metni her hücrede ayrı bir Python nesnesi olarak
saklıyordu (`object` türü). Bugün kullandığın pandas 3 ise metni çok daha sıkı
bir biçimde (`str` türü) saklıyor. Aynı dosyayı iki yolla okuyalım:

```python
import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 1_000_000)
text_columns = ["order_time", "city", "category", "payment"]
old = pd.read_csv("orders.csv", dtype={c: object for c in text_columns})
new = pd.read_csv("orders.csv")
print(f"object: {old.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
print(f"str:    {new.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
```

```text
object: 252.3 MB
str:    95.9 MB
```

Aynı veri, aynı satırlar: biri 252 MB, öbürü 96 MB. İnternette sık
okuyacağın "pandas dosyanın 5–10 katı bellek ister" kuralı eski `object`
saklamadan kalma. Kural yerine **ölçmeyi** alışkanlık edin: kullandığın
pandas sürümü, sütun türleri ve metnin uzunluğu sonucu değiştiriyor.

## Büyük verinin üç V'si

Büyük veri anlatılırken sık sık üç kelime geçiyor. Hepsi İngilizcede V ile
başlıyor:

- **Volume (hacim):** verinin büyüklüğü. Bu patikanın asıl konusu.
- **Velocity (hız):** verinin gelme hızı. Bir sitenin saniyede binlerce
  tıklaması, bir fabrikanın her saniye ölçüm gönderen sensörleri. Veri
  bitmiş bir dosya değil, akan bir nehir (Bölüm 14).
- **Variety (çeşitlilik):** verinin biçimi. Tablolar, JSON kayıtları, metin,
  resim, ses; hepsi bir arada.

Bazı kaynaklar iki V daha ekliyor: **Veracity** (doğruluk: veri ne kadar
güvenilir?) ve **Value** (değer: bu veriden bir şey çıkıyor mu?). Bir
sınavda "büyük veriyi tanımla" sorusu gelirse üç V'yi örnekleriyle
saymak iyi bir başlangıç.

## İki büyüme yolu: dikey ve yatay

Veri makineye sığmayınca iki seçenek var:

<figure class="fig">
  <div class="versus">
    <div><h4>Dikey ölçekleme</h4><p>Daha güçlü <b>tek</b> makine<br>Kod değişmiyor<br>Sınırı var, fiyatı hızla artıyor</p></div>
    <div><h4>Yatay ölçekleme</h4><p><b>Daha çok</b> makine<br>İş bölünüyor, sonuçlar birleşiyor<br>Sınırı neredeyse yok, kurması zor</p></div>
  </div>
  <figcaption>İngilizcede <i>scale up</i> ve <i>scale out</i>. Spark ve Hadoop yatay ölçekleme için var.</figcaption>
</figure>

- **Dikey ölçekleme** (*scale up*): daha güçlü bir makine. 16 GB yerine
  256 GB bellek. Kodun hiç değişmiyor ama bir sınırı var: dünyanın en büyük
  makinesinden büyüğünü alamazsın ve fiyat hızla artıyor.
- **Yatay ölçekleme** (*scale out*): daha çok makine. Veriyi parçalara
  bölüp her parçayı başka bir makineye vermek. Sınırı neredeyse yok ama işi
  bölmek, sonuçları birleştirmek ve bozulan makineyle başa çıkmak gerekiyor.
  Hadoop ve Spark bu iş için var (Bölüm 12 ve 13).

Çoğu zaman en iyi ilk adım ikisi de değil: **aynı makinede daha akıllı
çalışmak**. 100 GB'lık bir dosyanın ihtiyacın olan üç sütunu 5 GB
tutabilir. Patikanın ilk yarısı bunu anlatıyor.

## Bu patikanın haritası

<figure class="fig">
  <div class="flow">
    <span class="node">Ölç</span><span class="arrow">→</span>
    <span class="node">Küçült</span><span class="arrow">→</span>
    <span class="node">Parçala</span><span class="arrow">→</span>
    <span class="node">Doğru biçim</span><span class="arrow">→</span>
    <span class="node acc">Böl ve dağıt</span>
  </div>
  <figcaption>Patikanın sırası aynı zamanda bir sorunla karşılaşınca denenecek sıra: önce ucuz ve basit olan, en son birden çok makine.</figcaption>
</figure>

1. **Ölç** (Bölüm 1): tablo bellekte ne kadar tutuyor, hangi sütun en
   pahalı?
2. **Küçült** (Bölüm 2): doğru veri türleriyle aynı tablo daha az yer
   tutuyor.
3. **Parçala** (Bölüm 3): dosyayı tek seferde değil, parça parça oku.
4. **Doğru biçim** (Bölüm 4–6): CSV yerine Parquet; yalnızca gereken
   sütunları ve satırları oku.
5. **İşi veriye götür** (Bölüm 7–8): DuckDB ile dosyanın üstünde doğrudan
   SQL.
6. **Az veriyle yetin** (Bölüm 9): örnekleme ve yaklaşık hesap.
7. **Böl ve dağıt** (Bölüm 10–14): çekirdekler, dask, MapReduce, Spark ve
   akan veri.

## Önce ölç, sonra çöz

Bu patikanın en önemli alışkanlığı: **tahmin etme, ölç.** Bir şeyin yavaş
ya da büyük olduğunu düşünüyorsan önce sayıyı al:

- Dosya ne kadar? `os.path.getsize`
- Tablo bellekte ne kadar? `df.memory_usage(deep=True).sum()`
- Hangi sütun en çok yer tutuyor? `df.memory_usage(deep=True)` (Bölüm 1)

Ölçmeden yapılan iyileştirme çoğu zaman yanlış yere yapılıyor.

## Özet

- Veri, onu işleyen makine ve araç için fazlaysa **büyüktür**; sabit bir
  sınır yok.
- **Disk** büyük ve kalıcı, **bellek** küçük ve hızlı. pandas dosyayı
  baştan sona belleğe okuyor.
- 1 KB = 1024 bayt, 1 MB = 1024² bayt. `int64` ve `float64` sayı başına
  8 bayt.
- Python listesi her sayıyı ayrı nesne olarak saklıyor; NumPy dizisi yan
  yana. Bir milyon sayıda 34,3 MB'a karşı 7,6 MB.
- Dosya boyutu bellekteki boyutu söylemiyor: 61 MB'lık CSV pandas 3'te
  96 MB, eski `object` saklamayla 252 MB.
- Üç V: hacim, hız, çeşitlilik.
- Dikey ölçekleme daha büyük makine, yatay ölçekleme daha çok makine. Önce
  aynı makinede akıllı çalışmayı dene.
