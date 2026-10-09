# Önek Toplamları

"3. günden 6. güne kadar toplam satış ne?" sorusunu bir kez soracaksan
döngüyle toplamak yeter. Ama bir panoda kullanıcılar binlerce farklı aralık
soruyorsa her soru için baştan toplamak `O(n)`, toplamda `O(n × soru)` olur.
Bu bölümün tekniği, listeyi **bir kez** hazırlayıp sonra her aralık sorusunu
**tek bir çıkarmayla** cevaplıyor: **önek toplamları (prefix sums)**.

## Önek toplamı nedir?

Bir listenin önek toplamı, her konuma kadar olan **birikmiş toplamdır**
(kümülatif toplam). Başına bir `0` koymak işleri kolaylaştırır:

```python
from itertools import accumulate

sales = [3, 1, 4, 1, 5, 9, 2, 6]
prefix = [0]
for x in sales:
    prefix.append(prefix[-1] + x)
print(prefix)
print(sum(sales[2:6]), prefix[6] - prefix[2])
print([0] + list(accumulate(sales)))
```

```text
[0, 3, 4, 8, 9, 14, 23, 25, 31]
19 19
[0, 3, 4, 8, 9, 14, 23, 25, 31]
```

`prefix[i]`, ilk `i` elemanın toplamı. Bu yüzden `sales[lo:hi]` aralığının
toplamı tek satır:

```text
toplam(lo, hi) = prefix[hi] - prefix[lo]
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>sales</span><span><code>[3, 1, 4, 1, 5, 9, 2, 6]</code></span></div>
    <div class="anat-row"><span>prefix</span><span><code>[0, 3, 4, 8, 9, 14, 23, 25, 31]</code></span></div>
    <div class="anat-row"><span>sales[2:6] = 4 + 1 + 5 + 9</span><span><code>prefix[6] - prefix[2]</code> = 23 − 4 = 19</span></div>
  </div>
  <figcaption>prefix[6] ilk altı günü, prefix[2] ilk iki günü topluyor; farkları aradaki dört gün.</figcaption>
</figure>

`itertools.accumulate` aynı birikmiş toplamı hazır veriyor; pandas'ta
`cumsum()`, NumPy'da `np.cumsum()` aynı işin karşılıkları.

## Ne kadar kazandırıyor?

100 000 elemanlı bir listede 2 000 aralık sorusunu iki yolla cevaplayıp
adımları saydık:

```text
from scratch: 99882591
prefix sums : 102000
```

Baştan toplamak yaklaşık 100 milyon adım; önek toplamı ise bir kez kurulup
(100 000 adım) her soruyu tek çıkarmayla cevapladı. **Hazırlık `O(n)`,
her soru `O(1)`.** Aynı veriye çok soru sorulacaksa bu kalıp kazandırır.

## Toplamı k olan parçaları saymak

Daha zor bir soru: listede toplamı tam `k` olan **kaç ardışık parça** var?
Sayılar negatif olabiliyorsa bir önceki bölümün kayan penceresi çalışmaz
(pencereyi küçültmek toplamı artırabilir).

Önek toplamlarıyla düşünelim: `lo` ile `hi` arasındaki parçanın toplamı
`prefix[hi] - prefix[lo]`. Bunun `k` olması için `prefix[lo] = prefix[hi] - k`
olmalı. Yani listeyi gezerken, her konumda **şimdiye kadar `prefix - k`
değerinin kaç kez görüldüğünü** sorarız. Bir sözlük bu sayıları tutar:

```python
def count_sum_k(values, k):
    seen = {0: 1}          # boş önek: toplam 0, bir kez
    total = 0
    count = 0
    for x in values:
        total += x                         # şimdiki önek toplamı
        count += seen.get(total - k, 0)    # bu noktada biten uygun parçalar
        seen[total] = seen.get(total, 0) + 1
    return count
```

Kaba kuvvetle (her parçayı deneyerek) karşılaştıralım; satırlar
`(parça sayısı, adım)`:

```text
(4, 21)
(4, 6)
(21594, 4501500) (21594, 3000)
```

İlk iki satır küçük örnek (`[1, 2, -1, 3, -2, 2]`, `k = 3`): iki yöntem de 4
parça buldu. Son satırda 3000 sayılık listede iki yöntem aynı sonucu verdi;
kaba kuvvet 4,5 milyon adım, önek toplamı 3000 adım attı. Bu kalıp
(**önek toplamı + sözlük**) veri işinde çok güçlü: "toplamı şu olan dönem",
"ortalaması sıfır olan aralık", "eşit sayıda 0 ve 1 içeren parça" gibi
soruların hepsi bu kalıba indirgenir.

## Ters işlem: fark dizisi

Önek toplamı "çok soru, değişmeyen veri" içindi. Tersi de var: **çok
güncelleme**. "1. ile 4. gün arasındaki her güne 3 ekle" gibi aralık
güncellemelerini tek tek uygulamak her biri için `O(aralık)` sürer. **Fark
dizisi (difference array)** her güncellemeyi iki adımda kaydeder: aralığın
başına `+miktar`, bitişinin bir sonrasına `−miktar`. Sonunda bir önek
toplamı her günün gerçek değerini verir.

```python
def apply_updates(n, updates):
    diff = [0] * (n + 1)
    for lo, hi, amount in updates:     # lo..hi dahil
        diff[lo] += amount
        diff[hi + 1] -= amount
    result = []
    running = 0
    for i in range(n):
        running += diff[i]             # önek toplamı
        result.append(running)
    return result

print(apply_updates(6, [(0, 2, 5), (1, 4, 3), (3, 5, -1)]))
```

```text
[5, 8, 8, 2, 2, -1]
```

Gün 0: yalnızca +5. Gün 1–2: +5 ve +3. Gün 3–4: +3 ve −1. Gün 5: yalnızca −1.
`u` güncelleme ve `n` gün için `O(u + n)`.

## Özet

- Önek toplamı: `prefix[i]` ilk `i` elemanın toplamı; başına `0` koy.
- Aralık toplamı `prefix[hi] - prefix[lo]`: hazırlık `O(n)`, soru `O(1)`.
- Hazırları: `itertools.accumulate`, `pandas.cumsum`, `np.cumsum`.
- Toplamı `k` olan parçaları saymak: önek toplamı + sözlük, negatif sayılarda
  da `O(n)`.
- Fark dizisi: aralık güncellemelerini `O(1)`'de kaydet, sonda bir önek
  toplamıyla uygula.
