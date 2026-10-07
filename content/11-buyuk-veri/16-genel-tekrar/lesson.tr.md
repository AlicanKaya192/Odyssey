# Genel Tekrar

Büyük Veri patikasının sonuna geldin. "Dosya belleğe sığmıyor" sorusuyla
başladın; şimdi bir veriyi ölçüp küçültebiliyor, sorulara uygun bir biçimde
saklayabiliyor, tek makinede bütün çekirdeklerle işleyebiliyor ve birçok
makineye ya da canlı akışa geçince neyin değiştiğini biliyorsun. Bu bölüm
yolu baştan sona bir kez daha yürüyor: her durakta en önemli fikir ve en çok
kullanacağın kod.

<figure class="fig">
  <div class="flow">
    <span class="node">Ölç, küçült<br><small>00–03</small></span><span class="arrow">→</span>
    <span class="node">Dosyalar<br><small>04–06</small></span><span class="arrow">→</span>
    <span class="node">DuckDB<br><small>07–09</small></span><span class="arrow">→</span>
    <span class="node">Çekirdekler<br><small>10–11</small></span><span class="arrow">→</span>
    <span class="node acc">Küme, akış<br><small>12–14</small></span>
  </div>
  <figcaption>Büyük Veri patikasının yolu: önce aynı makinede akıllı çalışmak, sonra birçok makine ve canlı veri.</figcaption>
</figure>

## 1. Büyük ne demek, nasıl ölçülür (Bölüm 0–1)

Veri, onu işleyen makine ve araç için fazlaysa **büyük**; sabit bir sınır
yok. Disk büyük ve kalıcı, bellek küçük ve hızlı; pandas dosyayı baştan sona
belleğe okuyor. Dosya boyutu bellekteki boyutu söylemiyor: 61 MB'lık sipariş
CSV'si bellekte 96 MB.

```python
df.info(memory_usage="deep")          # özet ve gerçek boyut
df.memory_usage(deep=True)            # sütun başına bayt
tracemalloc.start()                   # tepe bellek
time.perf_counter()                   # süre
```

Çöküp çökmemeyi sondaki boyut değil **tepe bellek** belirliyor. Önce
aynı makinede akıllı çalışmayı dene (dikey), sonra daha çok makine (yatay).

## 2. Türlerle küçültmek (Bölüm 2)

| Sütun | Tür | Dikkat |
|---|---|---|
| Küçük tam sayı | `int8`, `int16`, `int32` | Taşma sessiz: `astype("int8")` 300'ü 44 yapıyor |
| Ondalık | `float32` | ~7 basamak; para için değil |
| Az değerli metin | `category` | Neredeyse hepsi farklıysa zarar |
| Tarih | `datetime64` | `pd.to_datetime` ya da `parse_dates` |
| Eksikli tam sayı | `Int8` … `Int64` | Büyük harfle |

En iyisi türleri **okurken** vermek: `read_csv(dtype=..., parse_dates=...)`.
Bir milyon sipariş 95,9 MB'tan 22,9 MB'a indi.

## 3. Parça parça okumak (Bölüm 3)

```python
for chunk in pd.read_csv("orders.csv", chunksize=250_000):
    ...  # parçada özetle
```

Kalıp: **parçada özetle, özetleri birleştir.** Toplam, sayı, en küçük, en
büyük doğrudan birleşiyor; ortalama için toplam ve sayı ayrı biriktirilip
sonda bölünüyor (ortalamaların ortalaması yanlış). Farklı değerler `set` ile
birleşiyor; ortanca parçalardan kesin bulunamıyor.

## 4. Dosya biçimleri ve Parquet (Bölüm 4–5)

CSV metin, satır satır ve türsüz. **Parquet** sütunlu: yalnızca gereken
sütunları okuyor, türleri saklıyor, iyi sıkışıyor.

```python
df.to_parquet("orders.parquet", compression="zstd", row_group_size=100_000)
pd.read_parquet("orders.parquet", columns=["city", "unit_price"])
pf = pq.ParquetFile("orders.parquet")    # metadata, read_row_group
```

Dosyanın içi: satır grupları → sütun parçaları; altbilgide her grubun her
sütunu için en küçük ve en büyük değer. Koşula uymayacağı belli olan gruplar
okunmadan atlanıyor, ama ancak veri o sütuna göre **sıralıysa**.

## 5. Bölümlemek (Bölüm 6)

```text
orders/month=2024-03/part-0.parquet
```

Veriyi sık süzülen bir sütuna göre klasörlere ayırınca koşula uymayan
klasörler hiç açılmıyor (**bölüm budama**). Bölüm sütunu az değerli olmalı:
çok ince bölmek çok küçük dosya sorununa yol açıyor. Yeni veri yeni klasör
olarak ekleniyor.

## 6. DuckDB (Bölüm 7–8)

```python
import duckdb

duckdb.sql("SELECT city, count(*) FROM 'orders.parquet' GROUP BY city")
duckdb.sql("FROM read_parquet('orders/*/*.parquet', hive_partitioning = true)")
duckdb.sql("SELECT * FROM orders")                   # pandas tablosu, adıyla
duckdb.execute("... WHERE city = ?", ["Ankara"])     # dışarıdan gelen değer
```

Python'un içinde, sunucusuz bir analiz veritabanı: dosyayı tablo gibi
sorguluyor, yalnızca gereken sütunları, bütün çekirdeklerle okuyor. Büyük işi
DuckDB'ye, küçük sonucu pandas'a ver (`.df()`). Dışarıdan gelen değer `?`
ile verilir, metne eklenmez.

## 7. Örneklem ve yaklaşık hesap (Bölüm 9)

- `df.sample(n=..., random_state=...)`: tohum sonucu tekrarlanabilir yapıyor.
- Standart hata = standart sapma / √n; hata verinin tamamına değil
  **örneklemin büyüklüğüne** bağlı.
- `head` gibi düzenli seçimler yanlı; grupları karşılaştırırken katmanlı
  örneklem.
- Yaklaşık farklı sayısı (HyperLogLog) ve yüzdelikler sabit bellekle; kesin
  değer gereken yerde kullanılmaz.

## 8. Bütün çekirdekler: paralel ve dask (Bölüm 10–11)

| Araç | Ne zaman |
|---|---|
| `ProcessPoolExecutor` | Saf Python hesabı (GIL'i aşmak için süreçler) |
| `ThreadPoolExecutor` | Bekleme işleri, NumPy |
| dask DataFrame | pandas yazımı, bellekten büyük veri |
| `dask.delayed` | Herhangi bir fonksiyonu tembel ve paralel yapmak |

Süreç kullanan kod `if __name__ == "__main__":` altında olmalı. Paralelliğin
bedeli var: küçük işlerde ve büyük veri gönderilen işlerde sıralıdan yavaş.
dask tembel: `compute()` gelene kadar yalnızca görev grafiği kuruluyor.

## 9. Birçok makine: MapReduce ve Spark (Bölüm 12–13)

**MapReduce** üç adım: map (kayıt → anahtar–değer), shuffle (aynı anahtar
aynı yere), reduce (anahtarın değerleri → sonuç). Birleştirici her makinede
önceden toplayıp ağdan geçen veriyi bir milyon çiftten 32'ye indirdi.
Anahtar makineye kararlı bir karmayla dağıtılıyor (`zlib.crc32`; Python'un
`hash()`'i her süreçte farklı).

**Spark** ara sonuçları bellekte tutuyor ve zengin, tembel bir dil sunuyor:

```python
counts = (lines.flatMap(lambda line: line.split())
               .map(lambda word: (word, 1))
               .reduceByKey(lambda a, b: a + b))   # dönüşümler: tarif
counts.collect()                                    # eylem: çalıştır
```

Dar dönüşüm bölüm içinde, geniş dönüşüm shuffle istiyor; iki kez kullanılan
RDD `cache()` ile bir kez hesaplanıyor; büyük sonuç sürücüye `collect()`
edilmiyor, diske yazılıyor.

## 10. Akan veri (Bölüm 14)

- Akışın sonu yok; olaylar tutulmuyor, küçük bir **durum** güncelleniyor.
- **Pencereler:** sabit (`ts // 60 * 60`), kayan (son N saniye, `deque`),
  oturum (boşlukla kapanır).
- Pencere **olay zamanıyla** kuruluyor; geç gelenler için **su işareti**: az
  beklemek eksik, çok beklemek geç sonuç.
- En az bir kez teslimde kopyalar kimlikle ayıklanıyor (etkisiz tekrar).
- **Kafka:** konu, bölüm, ofset, onaylama; sıra yalnızca bölümün içinde.

## Hangi araç?

| Durum | Araç |
|---|---|
| Belleğe rahat sığıyor | pandas (doğru türlerle) |
| Bellekten büyük, tek seferlik özet | `chunksize` |
| Her gün sorgulanacak | Parquet + bölümleme |
| Dosyada SQL, tek makine | DuckDB |
| pandas yazımı, bellekten büyük | dask |
| Hızlı fikir yeterli | Örneklem, yaklaşık sayım |
| Birçok makine | Spark |
| Veri canlı geliyor | Akış: pencereler, Kafka |

## Bütün parçalar bir arada (Bölüm 15)

Bitirme projesindeki hat patikanın neredeyse her bölümünü kullandı: önce
örnekten bellek tahmini (1, 2), CSV'yi parça parça Parquet'e çevirmek (3, 5),
aya göre bölümlemek (6), DuckDB ile sorgulayıp bir ayın sorusunda 12 dosyadan
yalnızca birini okumak (7), sonucu satır gruplarından kısmi toplamlarla
doğrulamak (12) ve hızlı tahmin için örneklem (9). Her adımın neden orada
olduğunu söyleyebiliyorsan, bu patikanın amacına ulaştın.

## Sırada ne var?

Bu patika verinin **büyüklüğüyle** başa çıkmayı öğretti. Veri Mühendisi
rotasında sıradaki adımlar, bu hattı başkalarının kullanabileceği bir servise
çevirmek (API patikaları) ve her bilgisayarda aynı çalışacak şekilde
paketlemek (Docker). Makine öğrenmesine gidiyorsan, büyük bir veriden modele
girecek örneği seçerken burada öğrendiğin ölçmek, örneklemek ve doğrulamak
aynen geçerli.
