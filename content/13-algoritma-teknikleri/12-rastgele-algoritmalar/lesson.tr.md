# Rastgele Algoritmalar

Şimdiye kadarki algoritmalar aynı girdiye her seferinde aynı adımları attı.
**Rastgele algoritmalar (randomized algorithms)** bazı kararları zar atarak
verir. Bu iki işe yarar: kötü niyetli ya da talihsiz bir girdinin algoritmayı
en kötü duruma sokmasını engeller, ve kesin cevabı pahalı olan bir soruya
ucuz ve **yeterince iyi** bir cevap verir.

İki tür var:

- **Las Vegas:** cevap her zaman doğru, süresi şansa bağlı (rastgele pivotlu
  quickselect).
- **Monte Carlo:** süre sabit, cevap yaklaşık ya da küçük bir olasılıkla yanlış
  (π tahmini, Bloom filtresi).

Bu bölümdeki bütün denemeler `random.seed` ile tohumlandı; aynı kodu
çalıştıran aynı sayıları görür.

## Quickselect: sıralamadan k. eleman

Medyanı bulmak için listenin tamamını sıralamak `O(n log n)`. **Quickselect**
quick sort'un yarısı: bir pivot seç, elemanları küçük / eşit / büyük diye
ayır, ama yalnızca aranan sıranın düştüğü **tek** parçaya devam et.

```python
import random


def quickselect(values, k, pick):
    items = list(values)
    comparisons = 0
    while True:
        pivot = pick(items)
        smaller = [x for x in items if x < pivot]
        equal = [x for x in items if x == pivot]
        larger = [x for x in items if x > pivot]
        comparisons += len(items)
        if k < len(smaller):
            items = smaller                    # aranan solda
        elif k < len(smaller) + len(equal):
            return pivot, comparisons          # aranan pivotun kendisi
        else:
            k -= len(smaller) + len(equal)
            items = larger                     # aranan sağda


random.seed(1)
data = [random.randint(0, 1_000_000) for _ in range(100_001)]
median, comps = quickselect(data, 50_000, random.choice)
print(median == sorted(data)[50_000], comps)
```

```text
True 222329
```

Yüz bin elemanda medyan, eleman sayısının iki katı kadar karşılaştırmayla
bulundu; sıralama `n log n` ≈ 1,7 milyon karşılaştırma ister. Ortalama maliyet
`O(n)`: her turda parça kabaca yarıya iniyor, `n + n/2 + n/4 + ... ≈ 2n`.

## Pivot neden rastgele?

Pivotu hep ilk eleman seçersen ve liste zaten sıralıysa, her turda yalnızca
bir eleman elenir:

```python
ordered = list(range(5000))
print(quickselect(ordered, 4999, lambda xs: xs[0])[1])
print(quickselect(ordered, 4999, random.choice)[1])
```

```text
12502500
9049
```

İlk eleman pivotuyla 12,5 milyon karşılaştırma (`n²/2`), rastgele pivotla
yaklaşık on bin. Rastgelelik en kötü durumu yok etmiyor ama onu **hiçbir
girdinin** zorlayamayacağı kadar olasılıksız yapıyor. Python'un `sorted`'ı bu
sorunu başka bir yolla çözüyor (Timsort sıralı parçaları fark ediyor).

## Karıştırma: Fisher-Yates

Bir listeyi karıştırmak kolay görünür ama yanlış yapmak da kolaydır. Doğru
yol **Fisher-Yates**: sondan başa doğru her konumu, kendisi **ve solundakiler**
arasından rastgele biriyle değiştir. Sık yapılan hata, her konumu **bütün
liste** içinden biriyle değiştirmek.

```python
from collections import Counter


def shuffle(items):
    for i in range(len(items) - 1, 0, -1):
        j = random.randint(0, i)               # 0..i: yalnızca soldakiler
        items[i], items[j] = items[j], items[i]


def bad_shuffle(items):
    for i in range(len(items)):
        j = random.randint(0, len(items) - 1)  # her seferinde bütün liste
        items[i], items[j] = items[j], items[i]


random.seed(7)
good, bad = Counter(), Counter()
for _ in range(60_000):
    a, b = [1, 2, 3], [1, 2, 3]
    shuffle(a)
    bad_shuffle(b)
    good[tuple(a)] += 1
    bad[tuple(b)] += 1
for perm in sorted(good):
    print(perm, good[perm], bad[perm])
```

```text
(1, 2, 3) 9986 8900
(1, 3, 2) 9929 11185
(2, 1, 3) 9945 11117
(2, 3, 1) 10101 11053
(3, 1, 2) 9810 8906
(3, 2, 1) 10229 8839
```

Üç elemanın altı sıralanışı var; 60 000 denemede her biri 10 000 civarında
çıkmalı. Fisher-Yates öyle. Hatalı yöntem 27 eşit olasılıklı yol açıyor ve 27,
6'ya bölünmediği için bazı sıralar 8 900, bazıları 11 100 civarında: **yanlı**.
Python'un `random.shuffle`'ı Fisher-Yates kullanır.

## Rezervuar örnekleme: sonu belirsiz akıştan örnek

Bir akıştan (log satırları, tıklamalar) eşit olasılıkla `k` öğe seçmek
istiyorsun ama akışın kaç öğe süreceğini bilmiyorsun ve hepsini saklayamazsın.
**Rezervuar örnekleme (reservoir sampling):** ilk `k` öğeyi al; `i`. öğe
(0'dan sayarak) gelince `0..i` arasında bir sayı çek, sayı `k`'dan küçükse o
konumdaki öğeyi yenisiyle değiştir. Bellek yalnızca `k` öğe.

```python
def reservoir(stream, k):
    sample = []
    for i, item in enumerate(stream):
        if i < k:
            sample.append(item)
        else:
            j = random.randint(0, i)
            if j < k:                          # olasılık k / (i + 1)
                sample[j] = item
    return sample


random.seed(3)
counts = Counter()
for _ in range(10_000):
    counts.update(reservoir(range(10), 2))
print([counts[i] for i in range(10)])
```

```text
[2064, 1976, 1926, 2054, 2046, 1959, 1932, 2068, 2006, 1969]
```

On öğeden ikisi seçiliyor; 10 000 denemede her öğe yaklaşık 2000 kez seçilmeli
ve sayılar 1926 ile 2068 arasında. İlk gelen ile son gelen aynı şansa sahip.

## Monte Carlo: rastgele noktalarla π

Kenarı 1 olan karenin içine rastgele noktalar at. Çeyrek dairenin içine
düşenlerin oranı, alanların oranına (`π/4`) yaklaşır.

<figure class="fig">
<svg viewBox="0 0 260 260" width="260" xmlns="http://www.w3.org/2000/svg"><rect class="box" x="10" y="10" width="240" height="240"/><circle class="dot" cx="159.5" cy="72.0" r="2.6"/><circle class="dot2" cx="200.8" cy="23.8" r="2.6"/><circle class="dot2" cx="187.6" cy="28.6" r="2.6"/><circle class="dot" cx="17.0" cy="138.3" r="2.6"/><circle class="dot2" cx="236.4" cy="94.2" r="2.6"/><circle class="dot" cx="226.2" cy="222.8" r="2.6"/><circle class="dot" cx="122.6" cy="190.8" r="2.6"/><circle class="dot" cx="140.5" cy="112.3" r="2.6"/><circle class="dot" cx="13.1" cy="198.0" r="2.6"/><circle class="dot" cx="77.1" cy="30.1" r="2.6"/><circle class="dot" cx="193.8" cy="211.7" r="2.6"/><circle class="dot" cx="201.3" cy="216.7" r="2.6"/><circle class="dot" cx="158.2" cy="219.6" r="2.6"/><circle class="dot" cx="10.4" cy="40.9" r="2.6"/><circle class="dot" cx="60.3" cy="198.3" r="2.6"/><circle class="dot2" cx="245.8" cy="40.6" r="2.6"/><circle class="dot2" cx="79.4" cy="19.2" r="2.6"/><circle class="dot" cx="139.4" cy="87.3" r="2.6"/><circle class="dot" cx="59.1" cy="24.2" r="2.6"/><circle class="dot2" cx="175.8" cy="18.0" r="2.6"/><circle class="dot" cx="224.5" cy="178.3" r="2.6"/><circle class="dot" cx="96.7" cy="210.2" r="2.6"/><circle class="dot" cx="45.0" cy="234.4" r="2.6"/><circle class="dot" cx="82.3" cy="105.3" r="2.6"/><circle class="dot" cx="10.8" cy="87.3" r="2.6"/><circle class="dot" cx="91.1" cy="175.6" r="2.6"/><circle class="dot" cx="206.4" cy="134.6" r="2.6"/><circle class="dot" cx="85.8" cy="134.5" r="2.6"/><circle class="dot" cx="179.1" cy="236.3" r="2.6"/><circle class="dot" cx="244.0" cy="244.5" r="2.6"/><circle class="dot2" cx="190.0" cy="47.2" r="2.6"/><circle class="dot" cx="14.3" cy="60.9" r="2.6"/><circle class="dot" cx="97.9" cy="111.2" r="2.6"/><circle class="dot" cx="12.2" cy="238.8" r="2.6"/><circle class="dot" cx="53.4" cy="20.8" r="2.6"/><circle class="dot" cx="57.2" cy="68.6" r="2.6"/><circle class="dot2" cx="233.1" cy="23.9" r="2.6"/><circle class="dot" cx="92.7" cy="164.8" r="2.6"/><circle class="dot" cx="135.9" cy="63.9" r="2.6"/><circle class="dot" cx="35.9" cy="70.4" r="2.6"/><circle class="dot2" cx="201.3" cy="43.7" r="2.6"/><circle class="dot" cx="18.8" cy="23.0" r="2.6"/><circle class="dot" cx="31.9" cy="168.2" r="2.6"/><circle class="dot2" cx="156.6" cy="29.7" r="2.6"/><circle class="dot" cx="91.6" cy="28.2" r="2.6"/><circle class="dot" cx="140.8" cy="175.0" r="2.6"/><circle class="dot" cx="86.0" cy="207.4" r="2.6"/><circle class="dot" cx="28.8" cy="214.3" r="2.6"/><circle class="dot2" cx="175.4" cy="10.8" r="2.6"/><circle class="dot" cx="48.8" cy="238.3" r="2.6"/><circle class="dot2" cx="246.8" cy="122.0" r="2.6"/><circle class="dot" cx="107.4" cy="193.0" r="2.6"/><circle class="dot2" cx="152.6" cy="51.7" r="2.6"/><circle class="dot" cx="119.4" cy="148.8" r="2.6"/><circle class="dot" cx="23.4" cy="30.1" r="2.6"/><circle class="dot" cx="17.9" cy="131.5" r="2.6"/><circle class="dot" cx="211.2" cy="218.7" r="2.6"/><circle class="dot2" cx="185.6" cy="22.0" r="2.6"/><circle class="dot2" cx="161.3" cy="60.9" r="2.6"/><circle class="dot" cx="35.6" cy="145.7" r="2.6"/><circle class="dot" cx="45.8" cy="47.3" r="2.6"/><circle class="dot" cx="80.8" cy="141.2" r="2.6"/><circle class="dot2" cx="249.8" cy="45.5" r="2.6"/><circle class="dot2" cx="244.2" cy="141.2" r="2.6"/><circle class="dot" cx="127.2" cy="74.9" r="2.6"/><circle class="dot" cx="125.0" cy="180.2" r="2.6"/><circle class="dot" cx="106.9" cy="214.8" r="2.6"/><circle class="dot2" cx="100.5" cy="12.8" r="2.6"/><circle class="dot2" cx="240.4" cy="99.5" r="2.6"/><circle class="dot" cx="129.8" cy="168.8" r="2.6"/><circle class="dot" cx="31.4" cy="184.6" r="2.6"/><circle class="dot2" cx="197.7" cy="41.8" r="2.6"/><circle class="dot" cx="96.7" cy="61.4" r="2.6"/><circle class="dot2" cx="196.0" cy="83.3" r="2.6"/><circle class="dot2" cx="169.4" cy="67.7" r="2.6"/><circle class="dot" cx="97.2" cy="80.9" r="2.6"/><circle class="dot" cx="77.4" cy="133.4" r="2.6"/><circle class="dot2" cx="194.7" cy="84.2" r="2.6"/><circle class="dot" cx="80.5" cy="23.1" r="2.6"/><circle class="dot" cx="165.9" cy="110.6" r="2.6"/><circle class="dot" cx="12.8" cy="118.7" r="2.6"/><circle class="dot" cx="70.2" cy="88.8" r="2.6"/><circle class="dot" cx="121.1" cy="54.0" r="2.6"/><circle class="dot2" cx="165.4" cy="58.6" r="2.6"/><circle class="dot" cx="93.5" cy="95.4" r="2.6"/><circle class="dot2" cx="187.1" cy="51.2" r="2.6"/><circle class="dot" cx="94.0" cy="47.7" r="2.6"/><circle class="dot2" cx="218.8" cy="84.8" r="2.6"/><circle class="dot2" cx="244.3" cy="20.4" r="2.6"/><circle class="dot" cx="134.4" cy="123.0" r="2.6"/><circle class="dot" cx="49.9" cy="49.2" r="2.6"/><circle class="dot2" cx="235.0" cy="135.5" r="2.6"/><circle class="dot" cx="175.9" cy="77.3" r="2.6"/><circle class="dot" cx="185.3" cy="208.8" r="2.6"/><circle class="dot" cx="197.3" cy="110.6" r="2.6"/><circle class="dot" cx="169.7" cy="149.0" r="2.6"/><circle class="dot" cx="159.7" cy="64.1" r="2.6"/><circle class="dot" cx="162.8" cy="77.1" r="2.6"/><circle class="dot" cx="16.6" cy="211.6" r="2.6"/><circle class="dot" cx="115.9" cy="94.0" r="2.6"/><circle class="dot" cx="62.6" cy="85.4" r="2.6"/><circle class="dot" cx="161.4" cy="240.0" r="2.6"/><circle class="dot" cx="123.2" cy="195.7" r="2.6"/><circle class="dot" cx="23.0" cy="218.0" r="2.6"/><circle class="dot" cx="86.2" cy="206.4" r="2.6"/><circle class="dot" cx="56.4" cy="241.4" r="2.6"/><circle class="dot" cx="121.7" cy="158.7" r="2.6"/><circle class="dot" cx="156.8" cy="108.4" r="2.6"/><circle class="dot" cx="67.1" cy="33.2" r="2.6"/><circle class="dot" cx="10.2" cy="152.7" r="2.6"/><circle class="dot" cx="76.8" cy="151.6" r="2.6"/><circle class="dot" cx="37.6" cy="50.5" r="2.6"/><circle class="dot" cx="99.7" cy="241.3" r="2.6"/><circle class="dot" cx="157.3" cy="227.2" r="2.6"/><circle class="dot" cx="140.9" cy="168.6" r="2.6"/><circle class="dot2" cx="149.4" cy="20.0" r="2.6"/><circle class="dot" cx="206.4" cy="149.4" r="2.6"/><circle class="dot2" cx="205.1" cy="95.8" r="2.6"/><circle class="dot" cx="98.7" cy="215.9" r="2.6"/><circle class="dot" cx="153.0" cy="114.7" r="2.6"/><circle class="dot2" cx="239.7" cy="17.7" r="2.6"/><circle class="dot" cx="156.1" cy="165.7" r="2.6"/><circle class="dot" cx="224.4" cy="249.8" r="2.6"/><circle class="dot" cx="35.9" cy="114.2" r="2.6"/><circle class="dot" cx="157.6" cy="216.2" r="2.6"/><circle class="dot2" cx="161.1" cy="36.1" r="2.6"/><circle class="dot" cx="100.2" cy="146.4" r="2.6"/><circle class="dot" cx="64.3" cy="180.0" r="2.6"/><circle class="dot2" cx="243.4" cy="158.9" r="2.6"/><circle class="dot2" cx="240.7" cy="30.7" r="2.6"/><circle class="dot" cx="153.0" cy="187.6" r="2.6"/><circle class="dot2" cx="245.4" cy="130.9" r="2.6"/><circle class="dot" cx="109.7" cy="173.4" r="2.6"/><circle class="dot2" cx="246.2" cy="132.0" r="2.6"/><circle class="dot" cx="78.7" cy="135.5" r="2.6"/><circle class="dot" cx="39.3" cy="100.8" r="2.6"/><circle class="dot" cx="116.4" cy="179.7" r="2.6"/><circle class="dot2" cx="197.6" cy="51.6" r="2.6"/><circle class="dot" cx="13.2" cy="122.2" r="2.6"/><circle class="dot" cx="75.7" cy="25.5" r="2.6"/><circle class="dot" cx="197.7" cy="191.0" r="2.6"/><circle class="dot" cx="74.2" cy="212.9" r="2.6"/><circle class="dot2" cx="247.3" cy="179.6" r="2.6"/><circle class="dot" cx="155.9" cy="136.1" r="2.6"/><circle class="dot" cx="164.8" cy="105.1" r="2.6"/><circle class="dot" cx="188.4" cy="221.6" r="2.6"/><circle class="dot" cx="192.5" cy="177.8" r="2.6"/><circle class="dot" cx="138.0" cy="169.3" r="2.6"/><circle class="dot" cx="81.2" cy="122.8" r="2.6"/><circle class="dot" cx="121.4" cy="163.4" r="2.6"/><circle class="dot" cx="188.8" cy="108.2" r="2.6"/><circle class="dot" cx="18.7" cy="189.4" r="2.6"/><circle class="dot2" cx="119.3" cy="30.0" r="2.6"/><circle class="dot2" cx="223.1" cy="119.1" r="2.6"/><circle class="dot" cx="13.5" cy="63.2" r="2.6"/><circle class="dot" cx="112.7" cy="111.8" r="2.6"/><circle class="dot" cx="180.0" cy="98.3" r="2.6"/><circle class="dot2" cx="125.7" cy="31.2" r="2.6"/><circle class="dot" cx="102.5" cy="156.0" r="2.6"/><circle class="dot" cx="214.5" cy="202.8" r="2.6"/><circle class="dot" cx="81.1" cy="50.8" r="2.6"/><circle class="dot" cx="25.9" cy="49.3" r="2.6"/><circle class="dot" cx="176.7" cy="146.1" r="2.6"/><circle class="dot" cx="78.7" cy="62.6" r="2.6"/><circle class="dot" cx="228.6" cy="215.8" r="2.6"/><circle class="dot" cx="124.8" cy="118.2" r="2.6"/><circle class="dot" cx="129.4" cy="170.6" r="2.6"/><circle class="dot" cx="46.8" cy="109.4" r="2.6"/><circle class="dot" cx="204.8" cy="233.6" r="2.6"/><circle class="dot" cx="65.2" cy="53.3" r="2.6"/><circle class="dot2" cx="200.0" cy="90.7" r="2.6"/><circle class="dot" cx="16.1" cy="76.6" r="2.6"/><circle class="dot2" cx="244.9" cy="10.4" r="2.6"/><circle class="dot" cx="178.3" cy="238.3" r="2.6"/><circle class="dot" cx="212.1" cy="197.4" r="2.6"/><circle class="dot2" cx="165.0" cy="21.5" r="2.6"/><circle class="dot" cx="181.0" cy="217.7" r="2.6"/><circle class="dot" cx="80.2" cy="29.7" r="2.6"/><circle class="dot" cx="45.9" cy="103.5" r="2.6"/><circle class="dot" cx="109.3" cy="211.3" r="2.6"/><circle class="dot" cx="159.4" cy="239.5" r="2.6"/><circle class="dot" cx="36.0" cy="159.0" r="2.6"/><circle class="dot" cx="27.3" cy="236.2" r="2.6"/><circle class="dot" cx="148.1" cy="71.8" r="2.6"/><circle class="dot" cx="220.8" cy="217.8" r="2.6"/><circle class="dot" cx="113.6" cy="174.5" r="2.6"/><circle class="dot" cx="154.1" cy="132.5" r="2.6"/><circle class="dot2" cx="235.2" cy="160.2" r="2.6"/><circle class="dot" cx="23.4" cy="82.6" r="2.6"/><circle class="dot" cx="46.3" cy="98.5" r="2.6"/><circle class="dot2" cx="131.4" cy="31.5" r="2.6"/><circle class="dot" cx="143.2" cy="101.0" r="2.6"/><circle class="dot" cx="73.2" cy="117.6" r="2.6"/><circle class="dot" cx="71.0" cy="69.9" r="2.6"/><circle class="dot" cx="134.1" cy="217.9" r="2.6"/><circle class="dot" cx="66.3" cy="160.9" r="2.6"/><circle class="dot" cx="186.8" cy="207.0" r="2.6"/><circle class="dot" cx="181.2" cy="92.8" r="2.6"/><circle class="dot" cx="30.5" cy="89.7" r="2.6"/><circle class="dot" cx="31.9" cy="220.1" r="2.6"/><circle class="dot" cx="152.6" cy="192.7" r="2.6"/><circle class="dot" cx="220.5" cy="134.7" r="2.6"/><circle class="dot" cx="87.6" cy="58.8" r="2.6"/><circle class="dot" cx="17.1" cy="76.0" r="2.6"/><circle class="dot" cx="22.9" cy="213.8" r="2.6"/><circle class="dot2" cx="238.5" cy="86.5" r="2.6"/><circle class="dot" cx="63.5" cy="222.1" r="2.6"/><circle class="dot2" cx="243.4" cy="90.4" r="2.6"/><circle class="dot" cx="206.9" cy="216.5" r="2.6"/><circle class="dot" cx="160.0" cy="165.0" r="2.6"/><circle class="dot" cx="66.4" cy="170.0" r="2.6"/><circle class="dot" cx="157.3" cy="166.3" r="2.6"/><circle class="dot" cx="102.6" cy="217.3" r="2.6"/><circle class="dot2" cx="209.5" cy="94.5" r="2.6"/><circle class="dot" cx="203.1" cy="146.0" r="2.6"/><circle class="dot" cx="214.4" cy="125.8" r="2.6"/><circle class="dot" cx="152.2" cy="112.4" r="2.6"/><circle class="dot" cx="187.6" cy="155.1" r="2.6"/><circle class="dot" cx="33.3" cy="242.0" r="2.6"/><circle class="dot" cx="58.6" cy="240.5" r="2.6"/><circle class="dot2" cx="223.4" cy="134.6" r="2.6"/><circle class="dot" cx="192.5" cy="249.9" r="2.6"/><circle class="dot2" cx="122.8" cy="36.5" r="2.6"/><circle class="dot" cx="158.7" cy="147.1" r="2.6"/><circle class="dot" cx="121.7" cy="226.1" r="2.6"/><circle class="dot" cx="47.1" cy="211.8" r="2.6"/><circle class="dot" cx="99.9" cy="157.4" r="2.6"/><circle class="dot" cx="221.3" cy="213.5" r="2.6"/><circle class="dot" cx="71.0" cy="183.4" r="2.6"/><circle class="dot" cx="48.8" cy="181.1" r="2.6"/><circle class="dot" cx="66.4" cy="134.3" r="2.6"/><circle class="dot" cx="17.7" cy="28.1" r="2.6"/><circle class="dot2" cx="98.6" cy="24.9" r="2.6"/><circle class="dot" cx="175.1" cy="88.3" r="2.6"/><circle class="dot2" cx="123.2" cy="23.1" r="2.6"/><circle class="dot" cx="38.3" cy="89.5" r="2.6"/><circle class="dot" cx="79.9" cy="88.1" r="2.6"/><circle class="dot" cx="185.0" cy="210.8" r="2.6"/><circle class="dot" cx="58.2" cy="244.0" r="2.6"/><circle class="dot" cx="65.3" cy="231.2" r="2.6"/><circle class="dot2" cx="106.3" cy="16.3" r="2.6"/><circle class="dot" cx="97.4" cy="175.2" r="2.6"/><circle class="dot" cx="122.3" cy="182.0" r="2.6"/><circle class="dot2" cx="185.8" cy="77.7" r="2.6"/><circle class="dot" cx="49.2" cy="192.3" r="2.6"/><circle class="dot2" cx="171.3" cy="24.3" r="2.6"/><circle class="dot" cx="165.0" cy="146.6" r="2.6"/><circle class="dot" cx="244.1" cy="248.5" r="2.6"/><circle class="dot" cx="24.6" cy="63.0" r="2.6"/><circle class="dot" cx="108.4" cy="239.2" r="2.6"/><circle class="dot2" cx="141.6" cy="12.5" r="2.6"/><circle class="dot" cx="134.5" cy="166.0" r="2.6"/><circle class="dot" cx="32.5" cy="232.9" r="2.6"/><circle class="dot2" cx="225.7" cy="132.1" r="2.6"/><circle class="dot" cx="234.6" cy="237.1" r="2.6"/><circle class="dot" cx="68.4" cy="237.9" r="2.6"/><circle class="dot" cx="105.4" cy="235.6" r="2.6"/><circle class="dot" cx="71.3" cy="152.2" r="2.6"/><circle class="dot" cx="83.4" cy="237.7" r="2.6"/><circle class="dot" cx="19.0" cy="16.8" r="2.6"/><circle class="dot" cx="53.1" cy="127.9" r="2.6"/><circle class="dot" cx="106.6" cy="122.5" r="2.6"/><circle class="dot" cx="30.2" cy="174.7" r="2.6"/><circle class="dot" cx="35.9" cy="119.9" r="2.6"/><circle class="dot2" cx="231.1" cy="106.4" r="2.6"/><circle class="dot" cx="215.6" cy="198.5" r="2.6"/><circle class="dot" cx="14.2" cy="120.5" r="2.6"/><circle class="dot" cx="126.8" cy="112.9" r="2.6"/><circle class="dot" cx="100.4" cy="100.0" r="2.6"/><circle class="dot2" cx="184.2" cy="30.9" r="2.6"/><circle class="dot" cx="83.8" cy="142.2" r="2.6"/><circle class="dot" cx="208.3" cy="196.2" r="2.6"/><circle class="dot" cx="37.8" cy="175.2" r="2.6"/><circle class="dot" cx="31.0" cy="64.6" r="2.6"/><circle class="dot" cx="206.7" cy="174.9" r="2.6"/><circle class="dot" cx="41.2" cy="230.3" r="2.6"/><circle class="dot" cx="68.8" cy="229.8" r="2.6"/><circle class="dot" cx="112.9" cy="111.5" r="2.6"/><circle class="dot" cx="68.9" cy="235.3" r="2.6"/><circle class="dot" cx="178.1" cy="238.5" r="2.6"/><circle class="dot" cx="58.0" cy="181.4" r="2.6"/><circle class="dot" cx="99.7" cy="226.4" r="2.6"/><circle class="dot" cx="110.9" cy="174.7" r="2.6"/><circle class="dot" cx="190.6" cy="116.5" r="2.6"/><circle class="dot2" cx="225.1" cy="93.0" r="2.6"/><circle class="dot" cx="192.3" cy="112.1" r="2.6"/><circle class="dot" cx="116.1" cy="54.0" r="2.6"/><circle class="dot2" cx="167.3" cy="20.9" r="2.6"/><circle class="dot2" cx="184.7" cy="81.7" r="2.6"/><circle class="dot" cx="74.2" cy="55.1" r="2.6"/><circle class="dot" cx="101.8" cy="218.7" r="2.6"/><circle class="dot" cx="25.8" cy="209.4" r="2.6"/><circle class="dot" cx="73.0" cy="87.8" r="2.6"/><circle class="dot" cx="78.5" cy="234.8" r="2.6"/><circle class="dot" cx="193.3" cy="116.3" r="2.6"/><circle class="dot" cx="16.6" cy="237.8" r="2.6"/><circle class="dot" cx="41.2" cy="164.3" r="2.6"/><circle class="dot2" cx="216.4" cy="22.2" r="2.6"/><circle class="dot" cx="156.9" cy="194.5" r="2.6"/><circle class="dot" cx="112.9" cy="163.0" r="2.6"/><circle class="dot" cx="89.3" cy="247.0" r="2.6"/><circle class="dot2" cx="150.3" cy="51.5" r="2.6"/><circle class="dot" cx="184.4" cy="227.1" r="2.6"/><circle class="dot" cx="137.3" cy="208.9" r="2.6"/><circle class="dot" cx="180.3" cy="142.9" r="2.6"/><circle class="dot2" cx="235.2" cy="59.3" r="2.6"/><circle class="dot" cx="38.4" cy="173.9" r="2.6"/><circle class="dot2" cx="229.6" cy="139.4" r="2.6"/><circle class="dot" cx="114.2" cy="144.1" r="2.6"/><circle class="dot2" cx="194.2" cy="25.3" r="2.6"/><circle class="dot2" cx="137.8" cy="17.3" r="2.6"/><circle class="dot" cx="153.0" cy="225.1" r="2.6"/><circle class="dot" cx="205.4" cy="149.3" r="2.6"/><circle class="dot" cx="22.6" cy="15.3" r="2.6"/><circle class="dot" cx="17.9" cy="111.5" r="2.6"/><circle class="dot2" cx="125.7" cy="38.4" r="2.6"/><circle class="dot" cx="104.3" cy="198.3" r="2.6"/><circle class="dot" cx="76.5" cy="201.7" r="2.6"/><circle class="dot" cx="145.0" cy="164.3" r="2.6"/><circle class="dot" cx="190.3" cy="192.0" r="2.6"/><circle class="dot" cx="94.4" cy="190.4" r="2.6"/><circle class="dot2" cx="245.8" cy="48.3" r="2.6"/><circle class="dot2" cx="214.0" cy="101.6" r="2.6"/><circle class="dot" cx="106.2" cy="215.7" r="2.6"/><circle class="dot" cx="209.6" cy="132.4" r="2.6"/><circle class="dot" cx="19.1" cy="209.3" r="2.6"/><circle class="dot" cx="33.7" cy="77.8" r="2.6"/><circle class="dot" cx="226.0" cy="202.2" r="2.6"/><circle class="dot" cx="201.3" cy="172.2" r="2.6"/><circle class="dot2" cx="173.9" cy="42.9" r="2.6"/><circle class="dot2" cx="159.5" cy="57.9" r="2.6"/><circle class="dot" cx="100.3" cy="247.6" r="2.6"/><circle class="dot" cx="132.8" cy="109.2" r="2.6"/><circle class="dot" cx="54.3" cy="156.6" r="2.6"/><circle class="dot" cx="86.1" cy="243.5" r="2.6"/><circle class="dot" cx="84.9" cy="158.1" r="2.6"/><circle class="dot" cx="124.3" cy="81.2" r="2.6"/><circle class="dot2" cx="105.8" cy="14.2" r="2.6"/><circle class="dot2" cx="205.7" cy="28.3" r="2.6"/><circle class="dot" cx="176.3" cy="89.2" r="2.6"/><circle class="dot" cx="138.8" cy="58.3" r="2.6"/><circle class="dot" cx="97.1" cy="107.5" r="2.6"/><circle class="dot" cx="173.1" cy="124.7" r="2.6"/><circle class="dot" cx="78.2" cy="231.3" r="2.6"/><circle class="dot" cx="30.9" cy="164.6" r="2.6"/><circle class="dot" cx="149.3" cy="67.7" r="2.6"/><circle class="dot" cx="181.5" cy="176.4" r="2.6"/><circle class="dot" cx="233.0" cy="184.1" r="2.6"/><circle class="dot" cx="181.9" cy="232.7" r="2.6"/><circle class="dot2" cx="190.8" cy="89.2" r="2.6"/><circle class="dot2" cx="239.7" cy="34.7" r="2.6"/><circle class="dot2" cx="175.0" cy="48.8" r="2.6"/><circle class="dot" cx="187.3" cy="103.4" r="2.6"/><circle class="dot" cx="60.1" cy="126.0" r="2.6"/><circle class="dot" cx="225.1" cy="192.6" r="2.6"/><circle class="dot2" cx="243.9" cy="119.5" r="2.6"/><circle class="dot" cx="104.4" cy="249.3" r="2.6"/><circle class="dot" cx="103.6" cy="207.2" r="2.6"/><circle class="dot2" cx="166.7" cy="34.1" r="2.6"/><circle class="dot2" cx="228.4" cy="102.8" r="2.6"/><circle class="dot" cx="102.8" cy="223.9" r="2.6"/><circle class="dot" cx="175.3" cy="117.2" r="2.6"/><circle class="dot" cx="181.7" cy="160.2" r="2.6"/><circle class="dot" cx="222.8" cy="199.0" r="2.6"/><circle class="dot" cx="83.3" cy="185.8" r="2.6"/><circle class="dot2" cx="159.3" cy="34.7" r="2.6"/><circle class="dot" cx="50.2" cy="98.1" r="2.6"/><circle class="dot" cx="194.0" cy="196.1" r="2.6"/><circle class="dot" cx="25.0" cy="114.2" r="2.6"/><circle class="dot2" cx="209.3" cy="39.1" r="2.6"/><circle class="dot" cx="184.7" cy="150.0" r="2.6"/><circle class="dot" cx="112.1" cy="123.1" r="2.6"/><circle class="dot" cx="227.1" cy="177.4" r="2.6"/><circle class="dot" cx="77.4" cy="104.7" r="2.6"/><circle class="dot" cx="242.0" cy="205.1" r="2.6"/><circle class="dot" cx="17.3" cy="222.3" r="2.6"/><circle class="dot" cx="145.0" cy="105.2" r="2.6"/><circle class="dot" cx="54.1" cy="204.3" r="2.6"/><circle class="dot" cx="152.7" cy="94.9" r="2.6"/><circle class="dot2" cx="175.7" cy="75.1" r="2.6"/><circle class="dot" cx="24.7" cy="133.7" r="2.6"/><circle class="dot2" cx="210.3" cy="20.3" r="2.6"/><circle class="dot" cx="86.4" cy="45.9" r="2.6"/><circle class="dot2" cx="164.8" cy="27.6" r="2.6"/><circle class="dot" cx="65.0" cy="82.8" r="2.6"/><circle class="dot" cx="211.8" cy="135.6" r="2.6"/><circle class="dot" cx="34.2" cy="203.6" r="2.6"/><circle class="dot" cx="47.6" cy="227.7" r="2.6"/><circle class="dot" cx="46.5" cy="102.2" r="2.6"/><circle class="dot" cx="35.2" cy="68.1" r="2.6"/><circle class="dot2" cx="186.7" cy="54.1" r="2.6"/><circle class="dot2" cx="202.9" cy="78.9" r="2.6"/><circle class="dot2" cx="231.8" cy="20.3" r="2.6"/><circle class="dot2" cx="160.0" cy="18.4" r="2.6"/><circle class="dot" cx="34.8" cy="225.3" r="2.6"/><circle class="dot" cx="25.5" cy="200.5" r="2.6"/><circle class="dot" cx="99.9" cy="139.9" r="2.6"/><circle class="dot2" cx="173.3" cy="71.7" r="2.6"/><circle class="dot" cx="30.1" cy="153.2" r="2.6"/><circle class="dot" cx="140.4" cy="160.0" r="2.6"/><path class="curve" d="M250 250 A240 240 0 0 0 10 10" fill="none"/></svg>
<figcaption>400 rastgele noktanın 308 tanesi çeyrek dairenin içinde (mor): 4 × 308 / 400 = 3.08. Nokta arttıkça oran π/4'e yaklaşır.</figcaption>
</figure>

```python
import math


def estimate_pi(n):
    inside = 0
    for _ in range(n):
        x, y = random.random(), random.random()
        if x * x + y * y <= 1:
            inside += 1
    return 4 * inside / n


random.seed(42)
print(estimate_pi(1_000_000))
for n in (100, 1000, 10_000, 100_000):
    errors = [abs(estimate_pi(n) - math.pi) for _ in range(40)]
    print(n, round(sum(errors) / len(errors), 4))
```

```text
3.140592
100 0.1441
1000 0.038
10000 0.0114
100000 0.0037
```

Her satır 40 denemenin ortalama hatası. Nokta sayısı 10 kat artınca hata
yaklaşık 3 kat (`√10`) azalıyor: Monte Carlo hatası `1/√n` gibi küçülür. Bir
basamak daha doğruluk için 100 kat nokta gerekir. Yavaş, ama boyut sayısından
bağımsız: çok boyutlu integrallerde ve olasılık hesaplarında başka yol yokken
bu çalışır.

## Makine öğrenmesinde

- **Rastgele bölme ve karıştırma:** `train_test_split`, çapraz doğrulama ve her
  epoch'ta veriyi karıştırmak Fisher-Yates'e dayanır.
- **Bootstrap ve rastgele orman:** yerine koyarak örnekleme; her ağaç verinin
  rastgele bir örneğini ve özelliklerin rastgele bir alt kümesini görür.
- **Stokastik gradyan inişi (SGD):** bütün veri yerine rastgele küçük
  gruplarla adım atar.
- **Büyük veriden örnek:** rezervuar örnekleme ile akan veriden tek geçişte
  eşit olasılıklı örnek.

## Özet

- Las Vegas her zaman doğru, süresi şansa bağlı; Monte Carlo süresi sabit,
  cevabı yaklaşık.
- Quickselect: ortalama `O(n)`; rastgele pivot en kötü durumu olasılıksız
  yapar.
- Fisher-Yates: `j = randint(0, i)`; bütün listeden seçmek yanlı karıştırır.
- Rezervuar örnekleme: `k` öğelik bellekle akıştan eşit olasılıklı örnek.
- Monte Carlo hatası `1/√n` gibi küçülür.
