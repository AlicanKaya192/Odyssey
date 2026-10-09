# time ve Zaman Ölçmek

`datetime` takvimle ilgilenir: hangi gün, hangi saat. **`time`** modülü ise
daha alt düzeyde çalışır: bilgisayarın saatini okur, programı bekletir ve
**bir işin ne kadar sürdüğünü** ölçer. Bu bölümde zaman damgasını (timestamp),
`sleep` ile beklemeyi ve süre ölçmenin doğru yolunu görüyoruz.

## Zaman damgası

Bilgisayarlar zamanı çoğu yerde tek bir sayı olarak tutar: **1 Ocak 1970
00:00 UTC'den** (Unix epoch) bu yana geçen saniye. Buna **zaman damgası**
(timestamp) denir; dosyaların değiştirilme zamanı, sunucu kayıtları ve
API'lerdeki zamanlar çoğunlukla böyledir.

```python
import time
from datetime import datetime, timezone

moment = datetime(2026, 3, 15, 14, 30, tzinfo=timezone.utc)
stamp = moment.timestamp()
print(stamp)
print(datetime.fromtimestamp(stamp, timezone.utc))
print(datetime.fromtimestamp(0, timezone.utc))
print(time.strftime("%Y-%m-%d %H:%M", time.gmtime(stamp)))
print(time.time() > stamp, type(time.time()).__name__)
```

```text
1773585000.0
2026-03-15 14:30:00+00:00
1970-01-01 00:00:00+00:00
2026-03-15 14:30
True float
```

- `timestamp()` tarihi saniyeye, `datetime.fromtimestamp(sayı, timezone.utc)`
  saniyeyi tarihe çevirir. 0 saniye 1970'in ilk anı.
- `time.time()` şu anın zaman damgasını ondalık sayı olarak verir; bu
  bölümü okuduğun an 15 Mart 2026'dan sonra olduğu için `True`.
- `time.gmtime` ve `time.strftime` aynı işi `time` modülünün içinde yapar;
  yeni kodda `datetime` daha okunaklıdır.

`fromtimestamp`'a saat dilimi verilmezse sonuç bilgisayarın **yerel** saatine
göre olur ve her bilgisayarda farklı çıkar. Damgayı tarihe çevirirken
dilimi açıkça yaz.

## Beklemek: sleep

```python
import time

start = time.perf_counter()
time.sleep(0.2)
elapsed = time.perf_counter() - start
print(round(elapsed, 1))
```

```text
0.2
```

`time.sleep(saniye)` programı verilen süre kadar bekletir; ondalık süre de
olur. Sık kullanıldığı yerler: bir API'ye art arda çok istek atmamak, hata
alınca yeniden denemeden önce beklemek, bir dosyanın oluşmasını beklemek.
`sleep` en az o kadar bekler, biraz fazlası olabilir; bu yüzden ölçülen süreyi
yuvarladık.

## Süre ölçmek: perf_counter

Bir işin süresini ölçmek için **`time.perf_counter()`** kullanılır: işten
önce ve sonra okunur, fark alınır. Değerin kendisinin anlamı yok (başlangıcı
belirsiz); yalnızca **iki okumanın farkı** anlamlı.

```python
import time

wall = time.perf_counter()
cpu = time.process_time()
time.sleep(0.3)
print(round(time.perf_counter() - wall, 1), time.process_time() - cpu < 0.05)
```

```text
0.3 True
```

İki farklı süre var:

- **`perf_counter`** duvar saatidir: işin başından sonuna geçen gerçek süre
  (0,3 saniye).
- **`process_time`** yalnızca işlemcinin **bu program için** çalıştığı süre.
  `sleep` sırasında işlemci çalışmadığı için neredeyse sıfır.

Kullanıcının beklediği süreyi merak ediyorsan `perf_counter`; bir hesabın
işlemciye ne kadar yük olduğunu merak ediyorsan `process_time`.

## İki yolu karşılaştırmak

Tek ölçüm güvenilir değildir: o sırada bilgisayar başka bir işle meşgul
olabilir. İşi birkaç kez çalıştırıp **en kısa** süreyi almak yaygın bir
yöntemdir; en kısa süre, araya en az şeyin girdiği çalıştırmadır.

```python
import time


def measure(func, repeat=5):
    best = float("inf")
    for _ in range(repeat):
        start = time.perf_counter()
        func()
        best = min(best, time.perf_counter() - start)
    return best


items = list(range(100_000))
as_set = set(items)
t_list = measure(lambda: 99_999 in items)
t_set = measure(lambda: 99_999 in as_set)
print(t_list > t_set * 100)
```

```text
True
```

`lambda: ...` ölçülecek işi bir fonksiyon olarak paketliyor; `measure` onu
beş kez çağırıyor. Bu bilgisayarda listede arama yaklaşık **0,4 ms**,
kümede arama **0,0001 ms**'nin altında sürdü (`perf_counter`'ın ölçebildiği
en küçük adıma yakın): liste baştan sona taranıyor, küme doğrudan yerine
bakıyor. Süreler bilgisayardan bilgisayara değiştiği için burada yalnızca
karşılaştırmanın sonucunu yazdırdık.

Daha titiz ölçüm için standart kütüphanede **`timeit`** modülü var; İleri
Python modülünde, kodun hangi satırının yavaş olduğunu bulan `cProfile` ile
birlikte anlatılıyor.

## Hangi saat?

```python
import time

for name in ["time", "monotonic", "perf_counter"]:
    info = time.get_clock_info(name)
    print(name, info.monotonic, info.adjustable)
```

```text
time False True
monotonic True False
perf_counter True False
```

`time.time()` **ayarlanabilir** bir saattir: bilgisayarın saati internetten
düzeltilince ya da kişi saati elle değiştirince geri bile gidebilir. Bu
yüzden süre ölçmek için kullanılmaz. `monotonic` ve `perf_counter` hiç geri
gitmez (**monoton**); süre ölçmek ve "5 saniye geçti mi?" diye bakmak için
bunlar kullanılır.

## Sık hata: aynı ad

```python
import time
from datetime import time

try:
    time.sleep(0.1)
except AttributeError as error:
    print("AttributeError:", error)
```

```text
AttributeError: type object 'datetime.time' has no attribute 'sleep'
```

`datetime` modülünde de `time` adlı bir sınıf var. İkinci satır `time`
adını o sınıfa bağladı ve modül kayboldu. İki modülü birlikte kullanırken
`import time` ile `import datetime as dt` ya da `from datetime import
datetime` yazılır; aynı ad iki şeye verilmez.

## Özet

- Zaman damgası 1970'ten bu yana geçen saniye; `timestamp()` ve
  `fromtimestamp(..., timezone.utc)` ile tarihe gidip gelinir.
- `time.sleep(saniye)` bekletir.
- Süre `perf_counter()` farkıyla ölçülür; işlemci süresi `process_time()`.
- Tek ölçüm yanıltır: birkaç kez çalıştırıp en kısasını al.
- `time.time()` süre ölçmek için değil, şu anın damgası için.
- `datetime.time` sınıfı ile `time` modülünü aynı adla içe aktarma.
