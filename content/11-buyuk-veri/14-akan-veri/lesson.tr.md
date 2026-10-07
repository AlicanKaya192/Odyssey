# Akan Veri

Şimdiye kadar veri hep bir yerde **duruyordu**: bir CSV, bir Parquet
klasörü, bir tablo. Dosyayı açıp baştan sona okuyor, sonucu bir kez
hesaplıyorduk. Ama birçok veri hiç durmuyor: kart ödemeleri, bir fabrikadaki
sensörlerin ölçümleri, bir sitedeki tıklamalar. Gece gündüz, saniye saniye
gelmeye devam ediyor ve **sonu yok**.

Böyle veride soru da farklı: "Bu kart son bir dakikada beş kez ödeme yaptı,
durdurmalı mıyız?" Bunun cevabı gece çalışan bir rapordan çıkarsa iş işten
geçmiş olur. Veriyi **geldiği anda** işlemeye **akan veri işleme**
(*stream processing*) deniyor.

## Toplu işleme ve akan veri

<figure class="fig">
  <div class="versus">
    <div><h4>Toplu işleme</h4><p>Veri durur, sonu belli<br>Dosyanın tamamı okunur<br>Sonuç bir kez çıkar<br>Gecikme: saatler</p></div>
    <div class="ok"><h4>Akan veri</h4><p>Veri gelir, sonu yok<br>Olay olay işlenir<br>Sonuç sürekli güncellenir<br>Gecikme: saniyeler</p></div>
  </div>
  <figcaption>Aynı ödemeler iki yolla da işlenebilir; fark, sonucun ne zaman gerektiği.</figcaption>
</figure>

İki yaklaşım birbirinin rakibi değil. Bir banka dolandırıcılığı akışta
yakalıyor, aylık raporu toplu işlemle çıkarıyor. Bu bölümde akışa özgü dört
soruyu ele alacağız: sonsuz veride **bellek**, **pencereler**, **geç gelen
olaylar** ve **aynı olayın iki kez gelmesi**.

## Python'da bir akış: üreteç

Alıştırmalarda salt okunur `stream_data.py` var. İçindeki `payments(n)`
sabit tohumlu bir kart ödemesi akışı: her çağrıda aynı ödemeler, **tek tek**
geliyor.

```python
from stream_data import payments

for event in payments(5):
    print(event)
```

```text
{'event_id': 1, 'ts': 3, 'card': 'C116', 'amount': 182.01, 'city': 'Bursa'}
{'event_id': 2, 'ts': 4, 'card': 'C049', 'amount': 82.59, 'city': 'Istanbul'}
{'event_id': 3, 'ts': 5, 'card': 'C115', 'amount': 146.12, 'city': 'Ankara'}
{'event_id': 4, 'ts': 7, 'card': 'C153', 'amount': 155.94, 'city': 'Istanbul'}
{'event_id': 5, 'ts': 10, 'card': 'C004', 'amount': 166.69, 'city': 'Istanbul'}
```

Her ödeme bir **olay** (*event*): bir kimlik (`event_id`), olayın olduğu an
(`ts`, akış başladığından beri geçen saniye), kart, tutar ve şehir.

`payments` bir **üreteç** (Bölüm 12'deki `yield`): listeyi baştan kurmuyor,
sen istedikçe bir sonraki olayı üretiyor. Akış da tam böyle: elinde yalnızca
**şu anki** olay var, geriye dönemiyorsun ve sonun ne zaman geleceğini
bilmiyorsun.

```python
stream = payments(1_000_000)
print(next(stream)["event_id"])
print(next(stream)["event_id"])
```

```text
1
2
```

Bir milyonluk akış "kuruldu" ama henüz hiçbir şey üretilmedi; `next()` her
çağrıldığında bir olay geliyor.

## Sabit bellekle hesap

Akışın sonu yoksa bütün olayları bir listede tutamazsın. Bunun yerine her
olaydan sonra küçük bir **özet** güncellenir: kaç olay geldi, toplam ne, en
büyüğü hangisi. Bu özete **durum** (*state*) deniyor.

```python
count = 0
total = 0.0
largest = None
for event in payments(100_000):
    count += 1
    total += event["amount"]
    if largest is None or event["amount"] > largest["amount"]:
        largest = event
print(count, round(total, 2), round(total / count, 2))
print(largest)
```

```text
100000 12367234.15 123.67
{'event_id': 24849, 'ts': 35239, 'card': 'C063', 'amount': 3423.02, 'city': 'Istanbul'}
```

Durum yalnızca üç değişken: akış yüz bin değil yüz milyar olay sürse de
bellek aynı kalır. Ölçelim (`tracemalloc`, Bölüm 1):

```python
import tracemalloc

def peak_kb(work):
    tracemalloc.start()
    work()
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    return round(peak / 1024)

def streaming():
    total = 0.0
    for event in payments(100_000):
        total += event["amount"]

def as_list():
    events = list(payments(100_000))

print(peak_kb(streaming), "KB")
print(peak_kb(as_list), "KB")
```

```text
13 KB
31644 KB
```

Akışla birkaç KB; önce listeye alınca otuz bin KB'tan fazla. Liste olay
sayısıyla büyüyor, akıştaki durum büyümüyor.

Her hesap bu kadar kolay özetlenmiyor. Toplam, sayı, en büyük, ortalama
kolay; **farklı kart sayısı** ise her kartı hatırlamayı gerektiriyor.
Orada Bölüm 9'daki HyperLogLog gibi yaklaşık yöntemler sabit bellekle iş
görüyor.

## Pencereler

"Akış başladığından beri toplam" çoğu zaman işe yaramaz; sorulan "**son bir
dakikada**" ya da "**her beş dakikada**" ne olduğu. Akışı zamana göre
dilimlemeye **pencere** (*window*) deniyor. Üç tür:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Sabit (tumbling)</span><span>0–60, 60–120, 120–180 … örtüşmüyor; her olay tek pencerede</span></div>
    <div class="anat-row"><span>Kayan (sliding)</span><span>her an "son 60 saniye"; pencereler örtüşüyor</span></div>
    <div class="anat-row"><span>Oturum (session)</span><span>uzunluğu yok; olaylar arasında uzun boşluk olunca kapanıyor</span></div>
  </div>
  <figcaption>Hangi pencere seçileceği sorudan çıkıyor: "her dakika", "son bir dakika" ya da "bir ziyaret".</figcaption>
</figure>

### Sabit pencere

Her olay tam bir pencereye düşüyor. Olayın penceresinin başlangıcı tam sayı
bölmesiyle bulunuyor: `ts // 60 * 60` (`ts` = 135 → 120).

```python
from collections import defaultdict

windows = defaultdict(int)
for event in payments(1_000):
    start = event["ts"] // 60 * 60
    windows[start] += 1
for start in sorted(windows)[:4]:
    print(start, windows[start])
```

```text
0 38
60 45
120 40
180 43
```

Bu kod bütün pencereleri sonuna kadar tutuyor ve sonucu en sonda yazıyor;
oysa akışın sonu yok. Akışta pencere **kapanınca** sonucu hemen gönderip
unutmak gerekiyor. Olaylar zaman sırasıyla geliyorsa yeni bir pencerenin ilk
olayı, öncekinin kapandığını söylüyor:

```python
current, count = None, 0
for event in payments(300):
    start = event["ts"] // 60 * 60
    if start != current:
        if current is not None:
            print("window", current, "closed:", count, "payments")
        current, count = start, 0
    count += 1
```

```text
window 0 closed: 38 payments
window 60 closed: 45 payments
window 120 closed: 40 payments
window 180 closed: 43 payments
window 240 closed: 41 payments
window 300 closed: 42 payments
window 360 closed: 40 payments
```

Durum artık yalnızca açık pencere. Son pencere (420) yazılmadı: o pencerenin
kapandığını söyleyecek bir sonraki olay gelmedi. Gerçek bir akışta gelecekti.

### Kayan pencere: dolandırıcılık uyarısı

"Bu kart **son 60 saniyede** beş ödeme yaptı mı?" sorusu her yeni ödemede
soruluyor; pencere ödemeyle birlikte kayıyor. Her kart için son ödemelerin
zamanlarını bir `deque`'de (iki ucundan hızlı eklenip çıkarılan liste)
tutuyoruz; 60 saniyeden eski olanlar soldan atılıyor:

```python
from collections import defaultdict, deque

recent = defaultdict(deque)
alerts = 0
for event in payments(100_000):
    times = recent[event["card"]]
    times.append(event["ts"])
    while times[0] <= event["ts"] - 60:
        times.popleft()
    if len(times) == 5:
        alerts += 1
        if alerts <= 3:
            print("alert:", event["card"], "at", event["ts"])
print(alerts, "alerts")
print(len(recent), "cards in state")
```

```text
alert: C061 at 328
alert: C149 at 508
alert: C175 at 2454
389 alerts
200 cards in state
```

İki ayrıntı:

- **`== 5`, `>= 5` değil.** Beşinci ödemede bir kez uyarıyoruz. `>= 5`
  yazılsaydı aynı patlamanın altıncı, yedinci ödemesi de uyarı olurdu: 389
  yerine 914 uyarı.
- **Durum kart sayısı kadar.** 200 kart, her birinde en fazla birkaç zaman.
  Kart sayısı milyonlarsa durum da büyür; uzun süre ödeme yapmayan kartın
  kaydı silinir.

### Oturum penceresi

Oturumun sabit bir uzunluğu yok: bir kullanıcının olayları arasında belli bir
süreden (örneğin 30 dakika) uzun **boşluk** olunca oturum kapanıyor. Bir
sitede "bir ziyarette kaç sayfa gezildi" sorusu böyle cevaplanıyor.

## Geç gelen olaylar

Şimdiye kadar olaylar zaman sırasıyla geldi. Gerçekte gelmiyor: telefon bir
süre çevrimdışı kalıyor, ağ yavaşlıyor, ödeme bir dakika sonra ulaşıyor. İki
ayrı zaman var:

- **Olay zamanı** (*event time*): ödemenin yapıldığı an (`ts`).
- **İşlenme zamanı** (*processing time*): olayın sisteme ulaştığı an.

`payments(n, late=True)` aynı ödemeleri bazıları gecikmiş olarak veriyor:

```python
newest = -1
out_of_order = 0
worst = 0
for event in payments(100_000, late=True):
    if event["ts"] < newest:
        out_of_order += 1
        worst = max(worst, newest - event["ts"])
    newest = max(newest, event["ts"])
print(out_of_order, worst)
```

```text
8005 119
```

8005 ödeme, kendisinden daha yeni bir ödemeden **sonra** geldi; en geç olanı
119 saniye geride kaldı. Yukarıdaki "yeni pencerenin ilk olayı gelince
öncekini kapat" kuralı bunları kaçırır: penceresi çoktan kapanmış bir ödeme
hiçbir sonuca girmez.

Hiç bilinmeyen bir şeyi beklemek de olmaz; pencere ne zaman kapanacak? Akış
sistemlerinin cevabı **su işareti** (*watermark*): "Görülen en yeni olay
zamanından `lateness` saniye eskisi artık gelmeyecek" varsayımı. Pencere,
su işareti bitişini geçince kapanıyor; ondan sonra gelen olay atılıyor (ya da
ayrıca kaydediliyor).

```python
def dropped(lateness):
    open_windows = defaultdict(int)
    newest = 0
    lost = 0
    for event in payments(100_000, late=True):
        start = event["ts"] // 60 * 60
        if start + 60 <= newest - lateness:
            lost += 1
            continue
        open_windows[start] += 1
        newest = max(newest, event["ts"])
        for s in [s for s in open_windows if s + 60 <= newest - lateness]:
            del open_windows[s]
    return lost

for lateness in [0, 30, 60, 90, 120]:
    print(lateness, dropped(lateness))
```

```text
0 6128
30 4078
60 1963
90 475
120 0
```

`del open_windows[s]` satırında pencerenin sonucu gönderilirdi. Takas açık:

- **Az beklemek** sonucu çabuk veriyor ama eksik: beklemeden (0) 6128 ödeme
  kayboldu.
- **Çok beklemek** sonucu tam veriyor ama geç: 120 saniye beklenince hiçbir
  ödeme kaybolmadı, ama her dakikanın sonucu iki dakika gecikmeli geliyor.

Doğru değer işe göre seçiliyor. Dolandırıcılıkta birkaç saniye bile uzun;
günlük ciro raporunda bir saat beklemek sorun değil.

## Aynı olay iki kez

Akışı taşıyan sistemler (biraz sonra Kafka) bir olayın ulaştığından emin
olamazsa onu **yeniden** gönderiyor. Kaybetmekten iyidir, ama bu sefer aynı
ödeme iki kez sayılabilir. `payments(n, duplicates=True)` bazı ödemeleri iki
kez veriyor:

```python
seen = set()
received = 0
naive = 0.0
total = 0.0
for event in payments(100_000, duplicates=True):
    received += 1
    naive += event["amount"]
    if event["event_id"] in seen:
        continue
    seen.add(event["event_id"])
    total += event["amount"]
print(received, len(seen))
print(round(naive, 2), round(total, 2))
```

```text
103003 100000
12732813.33 12367234.15
```

103003 olay geldi ama 100000'i farklı. Kopyaları ayıklamadan toplanan ciro
fazla; `event_id` ile ayıklanınca, sabit bellek bölümündeki toplamın aynısı.

Burada `seen` kümesi her kimliği tutuyor, yani akışla birlikte büyüyor.
Gerçek sistemlerde kimlikler yalnızca bir süre tutuluyor (kopyanın en fazla
ne kadar geç gelebileceği kadar).

Bu konunun adı **teslim garantisi**:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>En fazla bir kez</span><span>yeniden gönderilmez; olay kaybolabilir</span></div>
    <div class="anat-row"><span>En az bir kez</span><span>emin olunana kadar gönderilir; olay iki kez gelebilir</span></div>
    <div class="anat-row"><span>Tam bir kez</span><span>her olay bir kez sayılır; sistemin desteği gerekir, daha pahalı</span></div>
  </div>
  <figcaption>En sık seçilen: en az bir kez teslim ve kimlikle kopya ayıklamak.</figcaption>
</figure>

Pratikte en sık yol: en az bir kez teslim + işlemi **etkisiz tekrarlanabilir**
(*idempotent*) yapmak. Aynı olayı iki kez işlemek bir kez işlemekle aynı
sonucu veriyorsa kopya zarar vermez; kimlikle ayıklamak bunu sağlıyor.

## Kafka: akışı taşıyan kayıt defteri

Ödemeleri üreten (kasa, uygulama) ile işleyen (dolandırıcılık denetimi,
rapor) çoğu zaman ayrı programlar, ayrı makineler. Arada olayları güvenle
taşıyan bir sistem gerekiyor. En yaygını **Apache Kafka**:

<figure class="fig">
  <div class="flow">
    <span class="node">Üreticiler<br>kasa, uygulama</span><span class="arrow">→</span>
    <span class="node acc">Konu<br>3 bölüm</span><span class="arrow">→</span>
    <span class="node">Tüketiciler<br>denetim, rapor</span>
  </div>
  <figcaption>Üreticiler konuya yazıyor, tüketiciler kendi hızlarında okuyor; ikisi birbirini beklemiyor.</figcaption>
</figure>

- **Konu** (*topic*): bir olay türünün akışı, örneğin `payments`.
- **Bölüm** (*partition*): konu birkaç bölüme ayrılıyor, böylece birçok
  makineye yayılıyor. Her bölüm yalnızca **sonuna eklenen** bir kayıt
  defteri.
- **Ofset** (*offset*): bir kaydın kendi bölümündeki sırası (0, 1, 2, ...).
- **Anahtar** (*key*): aynı anahtarlı kayıtlar hep aynı bölüme gidiyor,
  Bölüm 12'deki shuffle'ın kuralıyla (anahtarın özeti, bölüm sayısına göre
  kalan).

Alıştırmalardaki salt okunur `minilog.py` bunun tek süreçlik küçük bir
taklidi:

```python
from minilog import Topic

topic = Topic("payments", partitions=3)
for event in payments(6):
    p, offset = topic.send(event["card"], event["amount"])
    print(event["card"], "-> partition", p, "offset", offset)
print(topic.read(0, 0))
```

```text
C116 -> partition 0 offset 0
C049 -> partition 1 offset 0
C115 -> partition 0 offset 1
C153 -> partition 2 offset 0
C004 -> partition 2 offset 1
C152 -> partition 1 offset 1
[(0, 'C116', 182.01), (1, 'C115', 146.12)]
```

`read(bölüm, ofset)` o ofsetten itibaren kayıtları `(ofset, anahtar, değer)`
olarak veriyor. **Sıra yalnızca bölümün içinde garanti**: bir kartın
ödemeleri hep aynı bölümde ve sırasıyla, ama farklı bölümlerdeki iki ödemenin
sırası belli değil. Bu yüzden anahtar, sırası önemli olan şey seçiliyor
(burada kart).

Kafka okunan kaydı **silmiyor**; kayıtlar bir süre (örneğin yedi gün)
saklanıyor. Her tüketici nerede kaldığını, yani bölüm başına bir sonraki
ofseti kendisi hatırlıyor:

```python
offsets = {0: 0, 1: 0, 2: 0}
batch = topic.read(2, offsets[2], max_records=1)
print(batch)
offsets[2] = batch[-1][0] + 1
print(offsets)
```

```text
[(0, 'C153', 155.94)]
{0: 0, 1: 0, 2: 1}
```

Ofseti kaydetmeye **onaylama** (*commit*) deniyor. Tüketici kayıtları işleyip
onaylamadan çökerse, yeniden başladığında son onaylanan ofsetten okuyor: o
kayıtları **ikinci kez** işliyor. En az bir kez teslim buradan geliyor; kimlikle
ayıklama da bu yüzden gerekiyor.

Aynı konuyu okuyan birkaç tüketici bir **tüketici grubu** oluşturuyor: konunun
bölümleri aralarında paylaşılıyor, her bölümü grupta tek bir tüketici okuyor.
Üç bölümlü bir konuyu en fazla üç tüketici paralel okuyabiliyor; bölüm sayısı,
paralelliğin üst sınırı.

## Gerçek araçlar

| Araç | Ne yapar |
|---|---|
| Apache Kafka | Olayları taşır ve saklar (konu, bölüm, ofset) |
| Spark Structured Streaming | Akışı küçük toplu işler dizisi olarak işler |
| Apache Flink | Olayları tek tek, düşük gecikmeyle işler |
| Bulut servisleri | Kinesis (AWS), Pub/Sub (Google): yönetilen taşıma |

Bu bölümde elle kurduğumuz her şeyin bu araçlarda bir karşılığı var. Gerçek
Spark'ta (burada çalıştırmıyoruz) bir dakikalık pencere ve 90 saniyelik su
işareti şöyle yazılıyor:

```python
from pyspark.sql.functions import window

counts = (stream.withWatermark("event_time", "90 seconds")
                .groupBy(window("event_time", "1 minute"))
                .count())
```

Kavramlar aynı: olay zamanı, pencere, su işareti, durum. Araç değişiyor,
sorular değişmiyor.

## Özet

- Akan veri sonsuz; geldiği anda işleniyor. Python'da bir akış bir üreteç gibi
  düşünülebilir: yalnızca şu anki olay elinde.
- Bütün olaylar tutulmaz; küçük bir **durum** güncellenir. Bu örnekte
  akışla birkaç KB, listeyle otuz bin KB'tan fazla.
- **Pencereler**: sabit (her olay tek pencerede), kayan (son N saniye),
  oturum (boşlukla kapanır). Pencere kapanınca sonuç gönderilir, durum
  bırakılır.
- **Olay zamanı** işlenme zamanından farklı; olaylar geç ve sırasız gelir.
  **Su işareti** ne kadar bekleneceğini söyler: az beklemek eksik, çok
  beklemek geç sonuç.
- Taşıma sistemleri olayı **iki kez** gönderebilir; kimlikle ayıklamak
  işlemi etkisiz tekrarlanabilir yapar.
- **Kafka**: konu, bölüm, ofset, onaylama, tüketici grubu. Sıra yalnızca
  bölümün içinde garanti.
