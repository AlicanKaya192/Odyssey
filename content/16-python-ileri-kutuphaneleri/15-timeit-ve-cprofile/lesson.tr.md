# timeit ve cProfile

"Bu kod yavaş" demek kolay; **neresinin** yavaş olduğunu tahmin etmek çoğu
zaman yanlış çıkar. Hızlandırmanın kuralı: önce **ölç**, sonra en çok zaman
harcanan yeri düzelt, sonra yeniden ölç. Bu bölüm iki standart aracı
anlatıyor: küçük parçaları karşılaştıran **`timeit`** ve programın zamanını
fonksiyon fonksiyon dağıtan **`cProfile`**. Saatle tek ölçüm (`time.perf_counter`)
Python Başlangıç modülünün time bölümündeydi.

Süreler makineden makineye değişir; bu yüzden aşağıdaki çıktılar süre değil,
**oran** ve **sayı** yazdırıyor. Bu bilgisayardaki süreler metinde.

## timeit: küçük bir parçayı ölçmek

```python
import timeit

LIST_SETUP = "s = list(range(10_000)); x = 9_999"
SET_SETUP = "s = set(range(10_000)); x = 9_999"
list_time = min(timeit.repeat("x in s", setup=LIST_SETUP, number=1_000, repeat=5))
set_time = min(timeit.repeat("x in s", setup=SET_SETUP, number=1_000, repeat=5))
print(list_time / set_time > 100)
print(type(timeit.timeit("sum(range(100))", number=1_000)).__name__)
```

```text
True
float
```

- **`timeit.timeit(kod, setup=..., number=n)`** kodu `n` kez çalıştırır ve
  toplam süreyi saniye olarak (`float`) verir. `setup` bir kez, ölçüme
  girmeden çalışır.
- **`timeit.repeat(..., repeat=5)`** ölçümü beş kez yapıp beş süre verir.
  **En küçüğü** alınır: diğerleri bilgisayarın o an başka işle meşgul
  olmasından etkilenmiştir; en küçük olan kodun kendi hızına en yakın.
- Listede aramak sonuna kadar tek tek bakar, kümede aramak adresi doğrudan
  hesaplar. Bu bilgisayarda 1000 aramada liste 0,069 sn, küme 0,000024 sn:
  yaklaşık 2800 kat.

## İki çözümü karşılaştırmak

```python
import timeit


def slow_unique(items):
    out = []
    for x in items:
        if x not in out:
            out.append(x)
    return out


def fast_unique(items):
    return list(dict.fromkeys(items))


data = [i % 2_000 for i in range(20_000)]
print(slow_unique(data) == fast_unique(data))
slow = min(timeit.repeat(lambda: slow_unique(data), number=3, repeat=3))
fast = min(timeit.repeat(lambda: fast_unique(data), number=3, repeat=3))
print(slow / fast > 50)
```

```text
True
True
```

- **Önce sonuçların aynı olduğunu** denetle: hızlı ama yanlış kod işe
  yaramaz.
- `timeit`'e metin yerine **fonksiyon** (burada `lambda`) da verilebilir;
  değişkenleri `setup`'a taşımak gerekmez.
- `x not in out` listenin tamamına bakıyor; liste büyüdükçe her adım
  yavaşlıyor. `dict.fromkeys` sırayı koruyarak tekrarları tek geçişte
  atıyor. Bu bilgisayarda 3 tekrar: 0,42 sn'ye karşı 0,0008 sn.
- Komut satırında: `python -m timeit "sum(range(100))"`; kaç kez
  çalıştıracağını kendisi seçer.

## cProfile: zaman nereye gidiyor?

```python
import cProfile
import pstats
import time


def load():
    time.sleep(0.05)
    return [i % 500 for i in range(50_000)]


def report(rows):
    return {key: rows.count(key) for key in set(rows)}


def main():
    return report(load())


profiler = cProfile.Profile()
profiler.enable()
main()
profiler.disable()
stats = pstats.Stats(profiler)
top = sorted(stats.stats.items(), key=lambda item: -item[1][3])[:5]
for (file, line, name), (cc, calls, total, cumulative, callers) in top:
    print(name, calls)
```

```text
main 1
report 1
<method 'count' of 'list' objects> 500
load 1
<built-in method time.sleep> 1
```

- **`cProfile.Profile()`** açıkken (`enable` – `disable`) çağrılan her
  fonksiyonun kaç kez çağrıldığını ve ne kadar zaman harcadığını kaydeder.
- **`pstats.Stats`** sonuçları okur. Her satırın iki süresi var:
  **tottime** (fonksiyonun kendi içinde geçen) ve **cumtime** (çağırdıkları
  dahil). Burada birikimli süreye göre sıraladık.
- Okuma: `main` her şeyi kapsıyor; içinde en çok zamanı `report` alıyor ve
  onun da neredeyse tamamı **500 kez** çağrılan `list.count`. Bu
  bilgisayarda toplam 0,23 sn'nin 0,17'si `count`, 0,05'i `sleep`.
- Normalde `stats.sort_stats("cumulative").print_stats(10)` tablo halinde
  yazdırır; tabloda dosya yolları olduğu için burada yalnızca adları
  yazdırdık.

## Darboğazı düzeltmek, yeniden ölçmek

```python
import cProfile
import pstats
from collections import Counter


def report_slow(rows):
    return {key: rows.count(key) for key in set(rows)}


def report_fast(rows):
    return dict(Counter(rows))


rows = [i % 500 for i in range(50_000)]
print(report_slow(rows) == report_fast(rows))
profiler = cProfile.Profile()
profiler.runcall(report_fast, rows)
names = [name for (_, _, name) in pstats.Stats(profiler).stats]
print("<method 'count' of 'list' objects>" in names)
```

```text
True
False
```

- `rows.count(key)` her anahtar için listenin tamamını tarıyor: 500 anahtar ×
  50 000 eleman. **`Counter`** listeyi **bir kez** gezerek sayıyor.
- Sonuç aynı; yeni profilde `list.count` çağrısı hiç yok (`False`).
- **`profiler.runcall(f, ...)`** tek bir çağrıyı profiller; `enable`/`disable`
  yazmaya gerek kalmaz.
- Sıra her zaman bu: ölç → en büyük kalemi bul → düzelt → sonucun aynı
  olduğunu doğrula → yeniden ölç.

## Komut satırından

```text
python -m cProfile -s cumtime app.py     # bütün programı profille
python -m timeit -s "s = set(range(10000))" "9999 in s"
```

- `-s cumtime` tabloyu birikimli süreye göre sıralar.
- Profil sonucunu dosyaya yazıp (`-o profile.out`) görsel araçlarla
  incelemek de mümkün (`snakeviz` gibi ayrı paketler).
- Bellek ölçümü (`tracemalloc`) bellek sızıntısı bölümünde.

## Yapma

- **Ölçmeden hızlandırmak:** zamanın %5'ini alan yeri iki kat hızlandırmak
  programı %2,5 hızlandırır.
- **Tek ölçüme güvenmek:** `repeat` ile birkaç kez ölç, en küçüğü al.
- **Doğruluğu unutmak:** yeni çözümün sonucu eskisiyle aynı mı?
- **Okunmaz kod için mikro kazanç:** ölçülmüş ve önemli bir kazanç yoksa
  okunabilir kod kalır.

## Özet

- `timeit.repeat(..., number=n, repeat=r)` → `min(...)`; fonksiyon da
  verilebilir.
- `cProfile.Profile()` + `pstats.Stats`: hangi fonksiyon kaç kez çağrıldı,
  ne kadar sürdü; `tottime` kendi, `cumtime` alt çağrılar dahil.
- `runcall(f, ...)` tek çağrıyı profiller.
- Ölç → düzelt → doğrula → yeniden ölç.
