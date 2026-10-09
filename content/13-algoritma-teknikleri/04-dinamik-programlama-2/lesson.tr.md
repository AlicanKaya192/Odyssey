# Dinamik Programlama 2

DP 1'de tablolar tek boyutluydu ya da bir ızgaraydı. Bu bölümde iki boyutlu
tabloların en çok kullanılan dört örneği var: bütün (0/1) sırt çantası, iki
metnin ortak kısmı, iki metin arasındaki düzenleme uzaklığı ve en uzun artan
alt dizi. Sonunda veri biliminden bir örnek: zaman serilerini karşılaştıran
dinamik zaman bükme (DTW). Bir de yeni bir beceri: tablodan yalnızca cevabı
değil, **cevabın nasıl oluştuğunu** geri çıkarmak.

## Bütün (0/1) sırt çantası

Açgözlü yöntem 50 kiloluk çantada `(60, 10)`, `(100, 20)`, `(120, 30)`
eşyalarıyla 160 bulmuştu; doğrusu 220. DP ile durum: `best[i][w]` = **ilk
`i` eşyayla** ve **`w` kilo** kapasiteyle alınabilecek en büyük değer.
`i`'inci eşya için iki seçenek var: almamak (`best[i − 1][w]`) ya da sığıyorsa
almak (`best[i − 1][w − ağırlık] + değer`).

```python
def knapsack(items, capacity):
    n = len(items)
    best = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        value, weight = items[i - 1]
        for w in range(capacity + 1):
            best[i][w] = best[i - 1][w]                    # almamak
            if weight <= w and best[i - 1][w - weight] + value > best[i][w]:
                best[i][w] = best[i - 1][w - weight] + value   # almak
    chosen, w = [], capacity                               # geri çıkar
    for i in range(n, 0, -1):
        if best[i][w] != best[i - 1][w]:                   # bu eşya alınmış
            chosen.append(i - 1)
            w -= items[i - 1][1]
    return best[n][capacity], sorted(chosen)

print(knapsack([(60, 10), (100, 20), (120, 30)], 50))
```

```text
(220, [1, 2])
```

220, ikinci ve üçüncü eşya (indeks 1 ve 2). **Geri çıkarma** tablonun son
hücresinden geriye yürür: değer bir üst satırla aynıysa o eşya alınmamış,
farklıysa alınmış ve kapasite onun ağırlığı kadar azalır. Maliyet
`O(eşya × kapasite)`.

## En uzun ortak alt dizi (LCS)

İki metinde **aynı sırada** geçen en uzun harf dizisi (yan yana olmaları
gerekmez). Dosya karşılaştırma (`diff`), DNA dizilerini hizalama ve
intihal denetimi bunun üstüne kurulur. Durum: `dp[i][j]` = `a`'nın ilk `i`,
`b`'nin ilk `j` harfinin ortak alt dizisinin uzunluğu.

<figure class="fig">
<svg viewBox="0 0 258 290" width="258" xmlns="http://www.w3.org/2000/svg">
<text class="dim" x="48.0" y="22" font-size="13" text-anchor="middle"></text>
<text class="dim" x="80.0" y="22" font-size="13" text-anchor="middle">B</text>
<text class="dim" x="112.0" y="22" font-size="13" text-anchor="middle">D</text>
<text class="dim" x="144.0" y="22" font-size="13" text-anchor="middle">C</text>
<text class="dim" x="176.0" y="22" font-size="13" text-anchor="middle">A</text>
<text class="dim" x="208.0" y="22" font-size="13" text-anchor="middle">B</text>
<text class="dim" x="240.0" y="22" font-size="13" text-anchor="middle">A</text>
<text class="dim" x="20" y="52.5" font-size="13" text-anchor="middle"></text>
<text class="dim" x="20" y="84.5" font-size="13" text-anchor="middle">A</text>
<text class="dim" x="20" y="116.5" font-size="13" text-anchor="middle">B</text>
<text class="dim" x="20" y="148.6" font-size="13" text-anchor="middle">C</text>
<text class="dim" x="20" y="180.6" font-size="13" text-anchor="middle">B</text>
<text class="dim" x="20" y="212.6" font-size="13" text-anchor="middle">D</text>
<text class="dim" x="20" y="244.6" font-size="13" text-anchor="middle">A</text>
<text class="dim" x="20" y="276.6" font-size="13" text-anchor="middle">B</text>
<rect class="box" x="32" y="32" width="32" height="32"/>
<text class="ink" x="48.0" y="52.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="64" y="32" width="32" height="32"/>
<text class="ink" x="80.0" y="52.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="96" y="32" width="32" height="32"/>
<text class="ink" x="112.0" y="52.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="128" y="32" width="32" height="32"/>
<text class="ink" x="144.0" y="52.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="160" y="32" width="32" height="32"/>
<text class="ink" x="176.0" y="52.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="192" y="32" width="32" height="32"/>
<text class="ink" x="208.0" y="52.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="224" y="32" width="32" height="32"/>
<text class="ink" x="240.0" y="52.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="32" y="64" width="32" height="32"/>
<text class="ink" x="48.0" y="84.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="64" y="64" width="32" height="32"/>
<text class="ink" x="80.0" y="84.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="96" y="64" width="32" height="32"/>
<text class="ink" x="112.0" y="84.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="128" y="64" width="32" height="32"/>
<text class="ink" x="144.0" y="84.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="160" y="64" width="32" height="32"/>
<text class="ink" x="176.0" y="84.5" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="192" y="64" width="32" height="32"/>
<text class="ink" x="208.0" y="84.5" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="224" y="64" width="32" height="32"/>
<text class="ink" x="240.0" y="84.5" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="32" y="96" width="32" height="32"/>
<text class="ink" x="48.0" y="116.5" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="64" y="96" width="32" height="32"/>
<rect class="curve4" x="66" y="98" width="28" height="28" rx="4"/>
<text class="ink" x="80.0" y="116.5" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="96" y="96" width="32" height="32"/>
<text class="ink" x="112.0" y="116.5" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="128" y="96" width="32" height="32"/>
<text class="ink" x="144.0" y="116.5" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="160" y="96" width="32" height="32"/>
<text class="ink" x="176.0" y="116.5" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="192" y="96" width="32" height="32"/>
<text class="ink" x="208.0" y="116.5" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="224" y="96" width="32" height="32"/>
<text class="ink" x="240.0" y="116.5" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="32" y="128" width="32" height="32"/>
<text class="ink" x="48.0" y="148.6" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="64" y="128" width="32" height="32"/>
<text class="ink" x="80.0" y="148.6" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="96" y="128" width="32" height="32"/>
<text class="ink" x="112.0" y="148.6" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="128" y="128" width="32" height="32"/>
<rect class="curve4" x="130" y="130" width="28" height="28" rx="4"/>
<text class="ink" x="144.0" y="148.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="160" y="128" width="32" height="32"/>
<text class="ink" x="176.0" y="148.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="192" y="128" width="32" height="32"/>
<text class="ink" x="208.0" y="148.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="224" y="128" width="32" height="32"/>
<text class="ink" x="240.0" y="148.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="32" y="160" width="32" height="32"/>
<text class="ink" x="48.0" y="180.6" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="64" y="160" width="32" height="32"/>
<text class="ink" x="80.0" y="180.6" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="96" y="160" width="32" height="32"/>
<text class="ink" x="112.0" y="180.6" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="128" y="160" width="32" height="32"/>
<text class="ink" x="144.0" y="180.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="160" y="160" width="32" height="32"/>
<text class="ink" x="176.0" y="180.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="192" y="160" width="32" height="32"/>
<rect class="curve4" x="194" y="162" width="28" height="28" rx="4"/>
<text class="ink" x="208.0" y="180.6" font-size="13" text-anchor="middle">3</text>
<rect class="box" x="224" y="160" width="32" height="32"/>
<text class="ink" x="240.0" y="180.6" font-size="13" text-anchor="middle">3</text>
<rect class="box" x="32" y="192" width="32" height="32"/>
<text class="ink" x="48.0" y="212.6" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="64" y="192" width="32" height="32"/>
<text class="ink" x="80.0" y="212.6" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="96" y="192" width="32" height="32"/>
<text class="ink" x="112.0" y="212.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="128" y="192" width="32" height="32"/>
<text class="ink" x="144.0" y="212.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="160" y="192" width="32" height="32"/>
<text class="ink" x="176.0" y="212.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="192" y="192" width="32" height="32"/>
<text class="ink" x="208.0" y="212.6" font-size="13" text-anchor="middle">3</text>
<rect class="box" x="224" y="192" width="32" height="32"/>
<text class="ink" x="240.0" y="212.6" font-size="13" text-anchor="middle">3</text>
<rect class="box" x="32" y="224" width="32" height="32"/>
<text class="ink" x="48.0" y="244.6" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="64" y="224" width="32" height="32"/>
<text class="ink" x="80.0" y="244.6" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="96" y="224" width="32" height="32"/>
<text class="ink" x="112.0" y="244.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="128" y="224" width="32" height="32"/>
<text class="ink" x="144.0" y="244.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="160" y="224" width="32" height="32"/>
<text class="ink" x="176.0" y="244.6" font-size="13" text-anchor="middle">3</text>
<rect class="box" x="192" y="224" width="32" height="32"/>
<text class="ink" x="208.0" y="244.6" font-size="13" text-anchor="middle">3</text>
<rect class="box" x="224" y="224" width="32" height="32"/>
<rect class="curve4" x="226" y="226" width="28" height="28" rx="4"/>
<text class="ink" x="240.0" y="244.6" font-size="13" text-anchor="middle">4</text>
<rect class="box" x="32" y="256" width="32" height="32"/>
<text class="ink" x="48.0" y="276.6" font-size="13" text-anchor="middle">0</text>
<rect class="box" x="64" y="256" width="32" height="32"/>
<text class="ink" x="80.0" y="276.6" font-size="13" text-anchor="middle">1</text>
<rect class="box" x="96" y="256" width="32" height="32"/>
<text class="ink" x="112.0" y="276.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="128" y="256" width="32" height="32"/>
<text class="ink" x="144.0" y="276.6" font-size="13" text-anchor="middle">2</text>
<rect class="box" x="160" y="256" width="32" height="32"/>
<text class="ink" x="176.0" y="276.6" font-size="13" text-anchor="middle">3</text>
<rect class="box" x="192" y="256" width="32" height="32"/>
<text class="ink" x="208.0" y="276.6" font-size="13" text-anchor="middle">4</text>
<rect class="box" x="224" y="256" width="32" height="32"/>
<text class="ink" x="240.0" y="276.6" font-size="13" text-anchor="middle">4</text>
</svg>
<figcaption>ABCBDAB (satırlar) ile BDCABA (sütunlar) tablosu. Yeşil hücreler geri çıkarmada eşleşen harfler: B, C, B, A.</figcaption>
</figure>

```python
def lcs(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1        # eşleşti: çaprazdan +1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    out, i, j = [], len(a), len(b)                     # geri çıkar
    while i and j:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i, j = i - 1, j - 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return dp[-1][-1], "".join(reversed(out))

print(lcs("ABCBDAB", "BDCABA"))
```

```text
(4, 'BCBA')
```

## Düzenleme uzaklığı (Levenshtein)

Bir metni öbürüne çevirmek için gereken en az **ekleme, silme ya da
değiştirme** sayısı. Yazım denetimi, "bunu mu demek istediniz?" önerileri ve
veri temizlemede yazım farkı olan kayıtları eşlemek bunu kullanır. Her hücre
üç seçenekten en ucuzu: üstten (silme), soldan (ekleme), çaprazdan (harf aynıysa
bedava, değilse değiştirme).

```python
def edit_distance(a, b):
    prev = list(range(len(b) + 1))           # boş metinden b'ye: j ekleme
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(prev[j] + 1,        # silme
                         cur[j - 1] + 1,     # ekleme
                         prev[j - 1] + cost) # değiştirme ya da eşleşme
        prev = cur
    return prev[-1]

print(edit_distance("kitten", "sitting"), edit_distance("python", "pyhton"))

words = ["pandas", "numpy", "python", "matplotlib", "seaborn", "sklearn"]
for typo in ["pyhton", "pnadas", "numpi", "seborn"]:
    print(typo, "->", min(words, key=lambda w: edit_distance(typo, w)))
```

```text
3 2
pyhton -> python
pnadas -> pandas
numpi -> numpy
seborn -> seaborn
```

Bütün tablo yerine yalnızca bir önceki satırı tutuyoruz (DP 1'in "belleği
küçültmek" notu): bellek `O(len(b))`. İki harfin yer değiştirmesi
(`pyhton`) burada iki işlem sayılıyor.

## En uzun artan alt dizi (LIS)

Bir dizide sırası bozulmadan seçilebilen en uzun **artan** alt dizi. Durum:
`best[i]` = `i`'inci elemanda **biten** en uzun artan alt dizinin uzunluğu;
her `i` için önceki bütün `j`'lere bakılır: `O(n²)`.

Daha zekice bir yol `O(n log n)`: `tails[k]`, uzunluğu `k + 1` olan artan alt
dizilerin **en küçük son elemanı**. Bu liste her zaman sıralı olduğu için her
yeni eleman `bisect` ile yerine konur.

```python
import bisect

def lis_slow(values):
    best = [1] * len(values)
    for i in range(len(values)):
        for j in range(i):
            if values[j] < values[i] and best[j] + 1 > best[i]:
                best[i] = best[j] + 1
    return max(best, default=0)

def lis_fast(values):
    tails = []
    for x in values:
        k = bisect.bisect_left(tails, x)     # x'in yeri
        if k == len(tails):
            tails.append(x)                  # daha uzun bir dizi
        else:
            tails[k] = x                     # aynı uzunlukta, daha küçük son
    return len(tails)

print(lis_slow([10, 9, 2, 5, 3, 7, 101, 18]), lis_fast([10, 9, 2, 5, 3, 7, 101, 18]))
```

```text
4 4
```

5000 rastgele sayıda iki yöntem:

```text
O(n^2)       : 135 in 469.7 ms
O(n log n)   : 135 in 0.47 ms
```

## Veri biliminde: dinamik zaman bükme (DTW)

İki zaman serisini karşılaştırırken noktaları **aynı anda** eşlemek
(Öklid ya da mutlak fark) aynı şekil biraz kaymışsa büyük fark gösterir.
**Dinamik zaman bükme (dynamic time warping)** bir serinin noktasını öbürünün
**yakınındaki** noktalarla eşlemeye izin verir; en ucuz eşlemeyi düzenleme
uzaklığının aynı tablosuyla bulur.

```python
import math

def dtw(a, b):
    dp = [[math.inf] * (len(b) + 1) for _ in range(len(a) + 1)]
    dp[0][0] = 0
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = abs(a[i - 1] - b[j - 1])
            dp[i][j] = cost + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[-1][-1]

wave = [0, 1, 3, 4, 3, 1, 0, 0, 0]
late = [0, 0, 0, 1, 3, 4, 3, 1, 0]       # aynı dalga, iki adım geç
other = [4, 3, 1, 0, 0, 0, 1, 3, 4]      # başka bir şekil
point = lambda a, b: sum(abs(x - y) for x, y in zip(a, b))
print("same shape, late :", point(wave, late), dtw(wave, late))
print("other shape      :", point(wave, other), dtw(wave, other))
```

```text
same shape, late : 14 0
other shape      : 24 15
```

Nokta nokta farkta geç gelen aynı dalga (14) başka bir şekle (24) yakın
görünüyor; DTW'de aynı dalga 0, başka şekil 15. Ses tanıma, sensör verisinde
hareket tanıma ve zaman serisi kümeleme DTW kullanır.

## Özet

- 0/1 sırt çantası: `best[i][w]`, al ya da alma; `O(eşya × kapasite)`.
- LCS: eşleşirse çaprazdan +1, değilse üst ya da solun büyüğü.
- Düzenleme uzaklığı: silme, ekleme, değiştirmenin en ucuzu; yazım denetimi
  ve kayıt eşleme.
- LIS: `O(n²)` DP ya da `bisect` ile `O(n log n)`.
- Geri çıkarma: tablonun sonundan hangi seçimin yapıldığına bakarak geriye
  yürü.
- DTW: kaymış zaman serilerini eşleyen DP.
