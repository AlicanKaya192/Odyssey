# Olasılıksal Veri Yapıları

Milyarlarca kullanıcının hangisinin siteyi daha önce ziyaret ettiğini, bir
günde kaç **farklı** IP adresinin geldiğini ya da hangi kelimelerin en sık
arandığını kesin olarak tutmak, bütün öğeleri saklamayı gerektirir. Bellek
yetmez. **Olasılıksal veri yapıları** küçük ve **ölçülebilir** bir hata payını
kabul edip belleği yüzlerce kat küçültür. Hepsinin temelinde aynı araç var:
bir öğeyi rastgele görünen bir sayıya çeviren **hash fonksiyonu**.

## Tohumlu hash

Bir öğeden birbirinden bağımsız görünen birçok sayı istiyoruz. Öğeyi bir
tohumla birleştirip hash'lemek yeter; `hashlib` her bilgisayarda ve her
çalıştırmada aynı sonucu verir (Python'un `hash()`'i vermez).

```python
import hashlib
import math
import sys


def h(item, seed):
    data = f"{seed}:{item}".encode()
    return int.from_bytes(hashlib.blake2b(data, digest_size=8).digest(), "big")


print(h("data", 0), h("data", 0) == h("data", 0), h("data", 1) == h("data", 0))
```

```text
6802316569817657998 True False
```

Aynı öğe ve aynı tohum hep aynı 64 bitlik sayıyı veriyor; tohum değişince
bambaşka bir sayı.

## Bloom filtresi: "kesinlikle yok" ya da "muhtemelen var"

**Bloom filtresi** `m` bitlik bir dizi ve `k` hash fonksiyonudur. Öğe eklemek:
`k` hash'in gösterdiği bitleri 1 yap. Sorgu: `k` bitin **hepsi** 1 ise
"muhtemelen var", biri bile 0 ise "kesinlikle yok".

<figure class="fig">
<svg viewBox="0 0 682 66" width="682" xmlns="http://www.w3.org/2000/svg">
<text class="dim" x="4" y="18" font-size="12">bits</text>
<text class="dim" x="89.0" y="18" font-size="12" text-anchor="middle">0</text>
<rect class="box" x="70" y="26" width="38" height="36"/>
<text class="ink" x="89.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="127.0" y="18" font-size="12" text-anchor="middle">1</text>
<rect class="box" x="108" y="26" width="38" height="36"/>
<text class="ink" x="127.0" y="48.9" font-size="14" text-anchor="middle">1</text>
<text class="dim" x="165.0" y="18" font-size="12" text-anchor="middle">2</text>
<rect class="box" x="146" y="26" width="38" height="36"/>
<text class="ink" x="165.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="203.0" y="18" font-size="12" text-anchor="middle">3</text>
<rect class="box" x="184" y="26" width="38" height="36"/>
<rect class="curve4" x="186" y="28" width="34" height="32" rx="4"/>
<text class="ink" x="203.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="241.0" y="18" font-size="12" text-anchor="middle">4</text>
<rect class="box" x="222" y="26" width="38" height="36"/>
<text class="ink" x="241.0" y="48.9" font-size="14" text-anchor="middle">1</text>
<text class="dim" x="279.0" y="18" font-size="12" text-anchor="middle">5</text>
<rect class="box" x="260" y="26" width="38" height="36"/>
<text class="ink" x="279.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="317.0" y="18" font-size="12" text-anchor="middle">6</text>
<rect class="box" x="298" y="26" width="38" height="36"/>
<text class="ink" x="317.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="355.0" y="18" font-size="12" text-anchor="middle">7</text>
<rect class="box" x="336" y="26" width="38" height="36"/>
<text class="ink" x="355.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="393.0" y="18" font-size="12" text-anchor="middle">8</text>
<rect class="box" x="374" y="26" width="38" height="36"/>
<text class="ink" x="393.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="431.0" y="18" font-size="12" text-anchor="middle">9</text>
<rect class="box" x="412" y="26" width="38" height="36"/>
<rect class="curve4" x="414" y="28" width="34" height="32" rx="4"/>
<text class="ink" x="431.0" y="48.9" font-size="14" text-anchor="middle">1</text>
<text class="dim" x="469.0" y="18" font-size="12" text-anchor="middle">10</text>
<rect class="box" x="450" y="26" width="38" height="36"/>
<rect class="curve4" x="452" y="28" width="34" height="32" rx="4"/>
<text class="ink" x="469.0" y="48.9" font-size="14" text-anchor="middle">1</text>
<text class="dim" x="507.0" y="18" font-size="12" text-anchor="middle">11</text>
<rect class="box" x="488" y="26" width="38" height="36"/>
<text class="ink" x="507.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="545.0" y="18" font-size="12" text-anchor="middle">12</text>
<rect class="box" x="526" y="26" width="38" height="36"/>
<text class="ink" x="545.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="583.0" y="18" font-size="12" text-anchor="middle">13</text>
<rect class="box" x="564" y="26" width="38" height="36"/>
<text class="ink" x="583.0" y="48.9" font-size="14" text-anchor="middle">0</text>
<text class="dim" x="621.0" y="18" font-size="12" text-anchor="middle">14</text>
<rect class="box" x="602" y="26" width="38" height="36"/>
<text class="ink" x="621.0" y="48.9" font-size="14" text-anchor="middle">1</text>
<text class="dim" x="659.0" y="18" font-size="12" text-anchor="middle">15</text>
<rect class="box" x="640" y="26" width="38" height="36"/>
<text class="ink" x="659.0" y="48.9" font-size="14" text-anchor="middle">0</text>
</svg>
<figcaption>16 bit, 3 hash. <code>cat</code> [1, 4, 14] ve <code>dog</code> [9, 10, 14] bitlerini 1 yaptı. <code>fox</code> yeşil halkalı bitlere bakıyor [3, 9, 10]; biri 0 olduğu için kesinlikle yok.</figcaption>
</figure>

```python
class Bloom:
    def __init__(self, bits, hashes):
        self.bits = bytearray(bits)            # sadelik için bit başına bir bayt
        self.hashes = hashes

    def _spots(self, item):
        return [h(item, s) % len(self.bits) for s in range(self.hashes)]

    def add(self, item):
        for i in self._spots(item):
            self.bits[i] = 1

    def __contains__(self, item):
        return all(self.bits[i] for i in self._spots(item))


bloom = Bloom(100_000, 7)
seen = [f"user{i}" for i in range(10_000)]
for name in seen:
    bloom.add(name)
print(all(name in bloom for name in seen))
false_hits = sum(f"guest{i}" in bloom for i in range(10_000))
expected = (1 - math.exp(-7 * 10_000 / 100_000)) ** 7      # formül
print(false_hits / 10_000, round(expected, 4))
set_bytes = sys.getsizeof(set(seen)) + sum(sys.getsizeof(s) for s in seen)
print(sys.getsizeof(bloom.bits), set_bytes)
```

```text
6802316569817657998 True False
True
0.0073 0.0082
100057 1013394
```

Eklenen on bin adın hepsi bulundu: Bloom filtresi **yanlış negatif vermez**.
Hiç eklenmemiş on bin addan 73'ü "muhtemelen var" dedi: yanlış pozitif oranı
%0,73, formülün öngördüğü %0,82'ye yakın. Bellek: bu sade sürüm bit başına bir
bayt kullanıyor ve yaklaşık 100 KB; bitler sıkıştırılınca 12,5 KB olur. Aynı
adları bir kümede tutmak yaklaşık 1 MB.

Bloom filtresi pahalı bir işten önce kapıda durur: veritabanı diske gitmeden
önce "bu anahtar kesinlikle yok mu?" diye sorar (Cassandra ve LevelDB böyle
çalışır).

## Count-Min sketch: kabaca kaç kez?

Bir akışta her öğenin kaç kez geçtiğini saymak için her öğeye bir sayaç
gerekir. **Count-Min sketch** `d` satır ve `w` sütunluk bir sayaç tablosudur.
Her satırın kendi hash'i var; öğe gelince her satırda bir sayaç artar. Tahmin,
öğenin `d` sayacının **en küçüğü**: başka öğeler aynı sayaca düşüp onu
şişirebilir, ama hiçbir sayaç gerçek sayının altına inemez.

```python
import random
from collections import Counter

random.seed(4)
words = ["the", "data", "model", "train", "test", "loss", "batch", "epoch"]
weights = [400, 200, 100, 60, 40, 20, 10, 5]
stream = random.choices(words, weights=weights, k=20_000)
stream += [f"rare{i}" for i in range(3000)]


class CountMin:
    def __init__(self, width, depth):
        self.table = [[0] * width for _ in range(depth)]

    def add(self, item):
        for row, counts in enumerate(self.table):
            counts[h(item, row) % len(counts)] += 1

    def estimate(self, item):
        return min(counts[h(item, row) % len(counts)]
                   for row, counts in enumerate(self.table))


cms = CountMin(200, 4)
for w in stream:
    cms.add(w)
true = Counter(stream)
for w in ["the", "batch", "epoch", "rare7"]:
    print(w, true[w], cms.estimate(w))
```

```text
6802316569817657998 True False
the 9678 9693
batch 244 258
epoch 130 140
rare7 1 11
```

3008 farklı öğe için 800 sayaç. Sık öğelerde tahmin gerçeğe çok yakın
(`the`: 9678 yerine 9693); bir kez geçen `rare7` ise 11 görünüyor. Count-Min
hep **fazla** tahmin eder ve hata sık öğeler için önemsizdir: "en çok
arananlar" (heavy hitters) sorusu için biçilmiş kaftan.

## HyperLogLog: kaç farklı öğe?

Farklı öğe sayısı (cardinality) için bir hash'in ikili gösteriminde baştaki
sıfırlara bakılır. Hash'lerin yarısı `1` ile, dörtte biri `01` ile, sekizde
biri `001` ile başlar. Gördüğün en uzun sıfır dizisi `r` ise yaklaşık `2ʳ`
farklı öğe görmüşsündür. Tek bir tahmin çok oynak olduğu için **HyperLogLog**
hash'in ilk bitleriyle öğeleri `m` kovaya dağıtır, her kova kendi en uzun
dizisini tutar ve sonuçların uygun bir ortalaması alınır.

```python
def hll_count(items, p=10):
    m = 1 << p                                 # 1024 kova
    registers = [0] * m
    for item in items:
        v = h(item, 0)
        bucket = v & (m - 1)                   # son p bit: kova
        rest = v >> p
        rank = (64 - p) - rest.bit_length() + 1   # baştaki sıfırlar + 1
        registers[bucket] = max(registers[bucket], rank)
    alpha = 0.7213 / (1 + 1.079 / m)
    estimate = alpha * m * m / sum(2.0 ** -r for r in registers)
    zeros = registers.count(0)
    if estimate <= 2.5 * m and zeros:          # küçük sayılarda düzeltme
        estimate = m * math.log(m / zeros)
    return round(estimate)


for n in (1000, 50_000, 200_000):
    items = [f"id{i % n}" for i in range(3 * n)]   # her öğe üç kez
    est = hll_count(items)
    print(n, est, round(abs(est - n) / n * 100, 1))
```

```text
6802316569817657998 True False
1000 991 0.9
50000 48634 2.7
200000 192751 3.6
```

Her satırda öğeler üçer kez geçiyor ama sayılan farklı öğe sayısı. 1024 küçük
sayaçla iki yüz bine kadar hata %4'ün altında; kuramsal hata `1.04/√m` ≈ %3,3.
Bellek, öğe sayısı milyarları bulsa da aynı kalır. Redis, BigQuery ve Spark'ın
`approx_count_distinct`'i bu yapıyı kullanır.

## MinHash: kümeler ne kadar benziyor?

İki kümenin Jaccard benzerliği (ortak / birleşim) için kümelerin tamamı
gerekir. **MinHash** her kümeyi `k` sayılık bir **imzaya** indirir: her tohum
için kümedeki öğelerin hash'lerinin **en küçüğü**. İki kümenin en küçük
hash'inin aynı çıkma olasılığı tam olarak Jaccard benzerliğidir; `k` imzanın
kaçının tuttuğu bunu tahmin eder.

```python
def shingles(text, k=3):
    w = text.split()
    return {" ".join(w[i:i + k]) for i in range(len(w) - k + 1)}


def signature(items, size=128):
    return [min(h(x, s) for x in items) for s in range(size)]


a = shingles("the quick brown fox jumps over the lazy dog "
             "near the river bank today")
b = shingles("the quick brown fox leaps over the lazy dog "
             "near the river bank today")
true_j = len(a & b) / len(a | b)
sa, sb = signature(a), signature(b)
est_j = sum(x == y for x, y in zip(sa, sb)) / len(sa)
print(round(true_j, 3), round(est_j, 3))
```

```text
6802316569817657998 True False
0.6 0.57
```

Gerçek benzerlik 0.6, 128 sayılık imzalarla tahmin 0.57. İmzalar küçük ve
sabit boyutlu olduğu için milyonlarca belge karşılaştırılabilir; LSH (yerel
duyarlı hash) imzaları kovalara bölüp yalnızca aynı kovaya düşen adayları
karşılaştırır. Dil modellerinin eğitim verisinden kopya belgeleri ayıklamak
çoğunlukla bu yolla yapılır.

## Özet

| Yapı | Soru | Hata | Bellek |
|---|---|---|---|
| Bloom filtresi | var mı? | yanlış pozitif, yanlış negatif yok | öğe başına birkaç bit |
| Count-Min | kaç kez? | yalnızca fazla tahmin | `w × d` sayaç |
| HyperLogLog | kaç farklı? | `1.04/√m` | `m` küçük sayaç |
| MinHash | ne kadar benzer? | `k` arttıkça azalır | küme başına `k` sayı |
