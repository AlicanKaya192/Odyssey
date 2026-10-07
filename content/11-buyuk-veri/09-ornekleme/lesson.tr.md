# Örnekleme ve Yaklaşık Hesap

Şimdiye kadar her soruyu verinin **tamamına** sorduk. Çoğu zaman buna gerek
yok. Bir tencere çorbanın tuzunu anlamak için bütün tencereyi içmiyorsun;
iyi karıştırıp bir kaşık tadıyorsun. Veride de böyle: iyi seçilmiş bir
**örneklem** (*sample*), verinin tamamından çok daha az işle, gerçeğe çok
yakın bir cevap veriyor. Üstelik o cevabın ne kadar yanılabileceğini de
söyleyebiliyorsun.

Bu bölümde örneklemin nasıl alındığını, ne kadar güvenilir olduğunu, hangi
örneklemlerin yanılttığını ve büyük veri araçlarının "tam değil ama çok
yakın ve çok ucuz" hesaplarını göreceğiz.

Örneklerde bir milyon sipariş var. Gerçek ortalama fiyat (verinin tamamından):

```python
import numpy as np
import pandas as pd
from orders_data import make_orders

orders = make_orders(1_000_000)
print(round(orders["unit_price"].mean(), 2))
```

```text
736.87
```

## Rastgele örneklem

`sample` tablodan rastgele satırlar seçiyor. `random_state` rastgeleliğin
tohumu: aynı sayı her seferinde aynı satırları veriyor, sonuç tekrar
edilebiliyor.

```python
s = orders.sample(n=10_000, random_state=42)
est = s["unit_price"].mean()
print(round(est, 2))
```

```text
729.31
```

Bir milyon satırın yüzde biriyle 736,87 yerine 729,31 bulduk. Peki bu ne
kadar iyi? Başka bir örneklem başka bir sayı verirdi; tek bir tahmin "ne kadar
yanılıyor olabilirim?" sorusunu cevaplamıyor.

## Ne kadar yanılıyor olabilirim? Standart hata

İstatistiğin bu soruya bir cevabı var: **standart hata** (*standard error*).
Örneklem ortalamasının, rastgele örneklemden örneklemden ne kadar oynadığını
tahmin ediyor:

```text
standart hata = örneklemin standart sapması / √(örneklem büyüklüğü)
```

Gerçek değer, tahminin iki yanında yaklaşık **1,96 standart hata** içinde
olur; bu aralığa **%95 güven aralığı** deniyor:

```python
se = s["unit_price"].std() / np.sqrt(len(s))
low, high = est - 1.96 * se, est + 1.96 * se
print(round(se, 2), round(low, 2), round(high, 2))
```

```text
8.33 712.99 745.64
```

Tahmin 729,31, aralık 712,99 ile 745,64 arasında; gerçek değer 736,87 bu
aralığın içinde. Matematik patikasında güven aralığını formülleriyle
görmüştün; burada bir büyük veri aracı olarak kullanıyoruz.

### "%95" ne demek?

Aynı işi 200 farklı rastgele örneklemle tekrarladım ve her seferinde
aralığın gerçek değeri içerip içermediğine baktım:

```python
true_mean = orders["unit_price"].mean()
hits = 0
for i in range(200):
    s = orders["unit_price"].sample(n=10_000, random_state=i)
    se = s.std() / np.sqrt(len(s))
    if s.mean() - 1.96 * se <= true_mean <= s.mean() + 1.96 * se:
        hits += 1
print(hits)
```

```text
191
```

200 denemenin 191'inde (yüzde 95,5) aralık gerçek değeri yakaladı. "%95
güven" tam olarak bu: bu yöntemle kurulan aralıkların yaklaşık yüzde 95'i
gerçek değeri içeriyor.

## Örneklem büyüdükçe hata nasıl küçülüyor?

Farklı büyüklüklerde 200'er örneklem alıp tahminlerin ne kadar dağıldığını
(standart sapmasını) ölçtüm:

```python
for n in [100, 1_000, 10_000, 100_000]:
    means = [orders["unit_price"].sample(n=n, random_state=i).mean() for i in range(200)]
    print(n, round(np.std(means), 2))
```

```text
100 87.6
1000 25.82
10000 8.2
100000 2.39
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>100 satır</span><span>tahminler ± 87,6 TL oynuyor</span></div>
    <div class="anat-row"><span>1 000 satır</span><span>± 25,8 TL</span></div>
    <div class="anat-row"><span>10 000 satır</span><span>± 8,2 TL</span></div>
    <div class="anat-row"><span>100 000 satır</span><span>± 2,4 TL</span></div>
  </div>
  <figcaption>Her satırda örneklem on kat büyüyor, hata yaklaşık üçte birine iniyor: hata 1/√n ile küçülüyor.</figcaption>
</figure>

Örneklem **on katına** çıkınca hata yaklaşık **üçte birine** (√10 ≈ 3,16)
iniyor. Hatayı yarıya indirmek için dört kat, onda birine indirmek için yüz
kat veri gerekiyor. Bu, **karekök kuralı**.

Bunun büyük veri için önemli bir sonucu var: hata, verinin tamamının değil
**örneklemin** büyüklüğüne bağlı. Bir milyon satırdan da bir milyar satırdan
da alınan 10 000 satırlık rastgele bir örneklem ortalamayı benzer bir
doğrulukla tahmin ediyor. Veri büyüdükçe örneklemin değeri artıyor.

## Kötü örneklem: ilk N satır

En kolay örneklem `head` gibi görünüyor: "ilk 10 000 satıra bakayım".
İki örneklemi karşılaştıralım:

```python
for name, part in [("head", orders.head(10_000)),
                   ("random", orders.sample(n=10_000, random_state=1))]:
    t = pd.to_datetime(part["order_time"])
    print(name, t.dt.month.nunique(), t.min().date(), t.max().date())
```

```text
head 1 2024-01-01 2024-01-04
random 12 2024-01-01 2024-12-31
```

Siparişler zaman sırasıyla yazıldığı için ilk 10 000 satır yılın yalnızca
**ilk dört günü**. Ocak başında olmayan her şey (bayramlar, yaz, yıl sonu
kampanyası) bu örneklemde yok. Rastgele örneklem ise yılın on iki ayından
geliyor.

Bu bir **yanlılık** (*bias*): örneklem bütünü temsil etmiyor. Yanlılığın en
tehlikeli yanı, örneklemi büyütmenin onu düzeltmemesi. İlk bir milyon satır
da yalnızca "ilk" satırlardır.

## Katmanlı örnekleme

Rastgele örneklem bütünün oranlarını taşıyor: İstanbul siparişlerin yüzde
34'ü, Trabzon yüzde 5'i. 1 600 satırlık bir örneklemde bu, İstanbul için 536,
Trabzon için 75 sipariş demek. Şehirleri **karşılaştırmak** istiyorsan
Trabzon'un tahmini az veriyle yapılıyor ve çok oynuyor.

**Katmanlı örnekleme** (*stratified sampling*) veriyi gruplara (katmanlara)
ayırıp her gruptan ayrı örneklem alıyor. Her şehirden eşit, 200'er sipariş:

```python
strat = orders.groupby("city", group_keys=False).sample(n=200, random_state=0)
```

Aynı toplam büyüklükte (1 600) iki yolu 200 kez tekrarlayıp her şehrin
ortalama fiyat tahminindeki ortalama hatayı ölçtüm:

| Şehir | Basit rastgele | Her şehirden 200 |
|---|---|---|
| İstanbul | 25,9 | 47,4 |
| Ankara | 42,2 | 47,6 |
| İzmir | 45,6 | 48,1 |
| Trabzon | 74,2 | 47,2 |

Katmanlı örneklemde her şehrin hatası benzer; Trabzon'un hatası 74,2'den
47,2'ye indi. Bedeli İstanbul'da: 536 yerine 200 siparişle onun hatası
büyüdü. Gruplar arasında karşılaştırma yapacaksan katmanlı, bütünün tek bir
sayısı lazımsa basit rastgele örneklem.

## Okurken örneklemek

Bir dosyanın tamamını okuyup sonra örneklem almak, verinin tamamını belleğe
almak demek. `read_csv`'nin `skiprows` seçeneği bir fonksiyon alabiliyor;
her satır için "atla mı?" diye soruyor:

```python
import random

rng = random.Random(42)
part = pd.read_csv("orders.csv", skiprows=lambda i: i > 0 and rng.random() > 0.01)
print(len(part))
```

```text
9962
```

- `i > 0`: 0. satır sütun adları, onu hiçbir zaman atlama.
- `rng.random() > 0.01`: her satırı yüzde 99 olasılıkla atla, yani yaklaşık
  yüzde birini tut.

Bellekte yalnızca seçilen satırlar duruyor (0,96 MB). Bu bilgisayarda okuma
0,47 saniye, dosyanın tamamını okumak 1,37 saniye sürdü: atlanan satırlar
yine baştan sona taranıyor ama tabloya dönüştürülmüyor.

## Uzunluğunu bilmediğin bir akış: rezervuar örneklemesi

Bazen kaç satır geleceğini bilmiyorsun: veri bir akıştan geliyor ya da dosya
o kadar büyük ki saymak bile bir iş. Akışı bir kez baştan sona geçip **tam
k** öğelik, her öğeye eşit şans veren bir örneklem almak mümkün mü? Evet:
**rezervuar örneklemesi** (*reservoir sampling*).

```python
import random

def reservoir(items, k, seed):
    rng = random.Random(seed)
    sample = []
    for i, item in enumerate(items):
        if i < k:
            sample.append(item)
        else:
            j = rng.randint(0, i)
            if j < k:
                sample[j] = item
    return sample

print(sorted(reservoir(range(1, 1_000_001), 10, seed=7)))
```

```text
[241872, 242003, 265420, 441598, 474876, 500179, 562811, 653273, 783341, 819875]
```

Fikir:

1. İlk k öğeyi rezervuara koy.
2. Sonraki her öğe (i. öğe) için 0 ile i arasında rastgele bir sayı çek.
   Sayı k'dan küçükse o öğe rezervuardaki bir öğenin yerini alıyor.
3. Akış bitince rezervuardaki k öğe, gelen bütün öğeler arasından eşit
   şansla seçilmiş oluyor.

Bellekte her an yalnızca k öğe var; akış ne kadar uzun olursa olsun. "Eşit
şans" iddiasını ölçtüm: 0–999 arasından 10'ar öğelik 2 000 örneklemde
seçilenlerin 10 022'si alt yarıdan, 9 978'i üst yarıdan geldi.

## DuckDB'de örneklem

DuckDB örneklemi sorgunun içinde alabiliyor:

```sql
SELECT avg(unit_price) FROM 'orders.parquet' USING SAMPLE 1% (bernoulli, 42);
SELECT * FROM 'orders.parquet' USING SAMPLE 10000 ROWS;
```

- `1% (bernoulli, 42)`: her satırı yüzde bir olasılıkla al, tohum 42. İki
  kez çalıştırınca ikisinde de 9 881 satır geldi: tohum sonucu sabitliyor.
- `10000 ROWS`: tam 10 000 satır.

## Yaklaşık hesaplar

Bazı soruların kesin cevabı pahalı. "Kaç farklı müşteri var?" sorusunu kesin
cevaplamak için her müşteriyi bir kez görüp hatırlamak gerekiyor (Bölüm
3'teki küme). Yüz milyonlarca farklı değerde bu küme belleğe sığmayabilir.

**Yaklaşık algoritmalar** bu soruları sabit ve çok küçük bir bellekle, küçük
bir hata payıyla cevaplıyor:

```python
import duckdb

duckdb.sql("SELECT count(DISTINCT customer_id) FROM 'orders.parquet'")
duckdb.sql("SELECT approx_count_distinct(customer_id) FROM 'orders.parquet'")
duckdb.sql("SELECT median(unit_price) FROM 'orders.parquet'")
duckdb.sql("SELECT approx_quantile(unit_price, 0.5) FROM 'orders.parquet'")
```

Bu bilgisayardaki sonuçlar:

| Soru | Kesin | Yaklaşık |
|---|---|---|
| Farklı müşteri sayısı | 245 461 (0,056 sn) | 219 479 (0,018 sn) |
| Ortanca fiyat | 449,05 (0,056 sn) | 449,18 (0,080 sn) |

- Farklı değer sayısında yaklaşık sonuç yüzde 10,6 eksik çıktı ama üç kat
  hızlıydı. Bu tür sayımın arkasında **HyperLogLog** adlı bir algoritma var;
  ne kadar farklı değer olursa olsun küçük ve sabit bir bellek kullanıyor.
- Ortancada yaklaşık sonuç çok yakın, ama bu boyutta kesin hesaptan **yavaş**
  çıktı. Bir milyon satır tek makinede hâlâ küçük; yaklaşık yöntemlerin asıl
  kazancı bellekte ve birçok makinenin sonuçlarını birleştirmekte. Her
  makine küçük bir özet çıkarıyor, özetler birleşiyor; kesin ortanca ise
  bütün değerleri tek bir yere toplamayı gerektiriyor.

## Ne zaman örneklem, ne zaman tamamı?

**Örneklem uygun:** veriyi keşfetmek, bir grafiğin genel şeklini görmek, bir
yöntemi hızlıca denemek, panolarda "yaklaşık" sayılar.

**Tamamı gerekli:** fatura, muhasebe, maaş gibi kuruşu kuruşuna doğru olması
gereken sayılar; **nadir olaylar** (dolandırıcılık, arıza): yüzde birlik bir
örneklem binde birlik olayları kolayca kaçırır.

## Özet

- `df.sample(n=..., random_state=...)` rastgele örneklem; tohum sonucu
  tekrar edilebilir yapıyor.
- Standart hata = standart sapma / √n; %95 güven aralığı tahmin ± 1,96
  standart hata. Bu ölçümde 200 aralığın 191'i gerçek değeri içerdi.
- Hata örneklemin büyüklüğüne bağlı, verinin tamamınınkine değil;
  örneklem on kat büyüyünce hata üçte birine iniyor.
- `head` gibi düzenli seçimler yanlı: ilk 10 000 sipariş yılın ilk dört
  günü.
- Grupları karşılaştıracaksan katmanlı örneklem:
  `groupby(...).sample(n=...)`.
- Okurken örneklemek için `read_csv(skiprows=fonksiyon)`; uzunluğu belli
  olmayan akış için rezervuar örneklemesi.
- Yaklaşık sayım ve yüzdelikler sabit, küçük bellekle çalışıyor; kesin değer
  gerektiren işlerde ve nadir olaylarda kullanılmaz.
