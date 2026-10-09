# Dinamik Programlama 1

Böl ve Fethet bölümünün sonunda bir uyarı vardı: parçalar **örtüşüyorsa**
yani aynı alt problem tekrar tekrar çıkıyorsa böl-fethet üstel büyür.
**Dinamik programlama (dynamic programming, DP)** bunun çaresi: her alt
problemi **bir kez** çöz, cevabını sakla, bir daha gerekince hesaplama, oku.

İki koşul arar:

- **Örtüşen alt problemler:** aynı küçük problem birçok kez gerekiyor.
- **En iyi alt yapı:** büyük problemin cevabı küçüklerin cevaplarından
  kurulabiliyor.

## Sorun: aynı işi tekrar tekrar yapmak

```python
calls = 0

def fib(n):
    global calls
    calls += 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(30), calls)
```

```text
832040 2692537
```

<figure class="fig">
<svg viewBox="0 0 696 274" width="696" xmlns="http://www.w3.org/2000/svg">
<line class="line" x1="72.4" y1="192.0" x2="28.4" y2="248.0"/>
<line class="line" x1="72.4" y1="192.0" x2="116.4" y2="248.0"/>
<line class="line" x1="160.4" y1="136.0" x2="72.4" y2="192.0"/>
<line class="line" x1="160.4" y1="136.0" x2="204.4" y2="192.0"/>
<line class="line" x1="336.4" y1="136.0" x2="292.4" y2="192.0"/>
<line class="line" x1="336.4" y1="136.0" x2="380.4" y2="192.0"/>
<line class="line" x1="248.4" y1="80.0" x2="160.4" y2="136.0"/>
<line class="line" x1="248.4" y1="80.0" x2="336.4" y2="136.0"/>
<line class="line" x1="512.4" y1="136.0" x2="468.4" y2="192.0"/>
<line class="line" x1="512.4" y1="136.0" x2="556.4" y2="192.0"/>
<line class="line" x1="600.4" y1="80.0" x2="512.4" y2="136.0"/>
<line class="line" x1="600.4" y1="80.0" x2="644.4" y2="136.0"/>
<line class="line" x1="424.4" y1="24.0" x2="248.4" y2="80.0"/>
<line class="line" x1="424.4" y1="24.0" x2="600.4" y2="80.0"/>
<rect class="box" x="6.0" y="232.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="28.4" y="252.2" font-size="12" text-anchor="middle">f(1)</text>
<rect class="box" x="50.0" y="176.0" width="44.9" height="32" rx="8"/>
<rect class="curve2" x="50.0" y="176.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="72.4" y="196.2" font-size="12" text-anchor="middle">f(2)</text>
<rect class="box" x="94.0" y="232.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="116.4" y="252.2" font-size="12" text-anchor="middle">f(0)</text>
<rect class="box" x="138.0" y="120.0" width="44.9" height="32" rx="8"/>
<rect class="curve2" x="138.0" y="120.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="160.4" y="140.2" font-size="12" text-anchor="middle">f(3)</text>
<rect class="box" x="182.0" y="176.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="204.4" y="196.2" font-size="12" text-anchor="middle">f(1)</text>
<rect class="box" x="226.0" y="64.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="248.4" y="84.2" font-size="12" text-anchor="middle">f(4)</text>
<rect class="box" x="270.0" y="176.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="292.4" y="196.2" font-size="12" text-anchor="middle">f(1)</text>
<rect class="box" x="314.0" y="120.0" width="44.9" height="32" rx="8"/>
<rect class="curve2" x="314.0" y="120.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="336.4" y="140.2" font-size="12" text-anchor="middle">f(2)</text>
<rect class="box" x="358.0" y="176.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="380.4" y="196.2" font-size="12" text-anchor="middle">f(0)</text>
<rect class="box" x="402.0" y="8.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="424.4" y="28.2" font-size="12" text-anchor="middle">f(5)</text>
<rect class="box" x="446.0" y="176.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="468.4" y="196.2" font-size="12" text-anchor="middle">f(1)</text>
<rect class="box" x="490.0" y="120.0" width="44.9" height="32" rx="8"/>
<rect class="curve2" x="490.0" y="120.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="512.4" y="140.2" font-size="12" text-anchor="middle">f(2)</text>
<rect class="box" x="534.0" y="176.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="556.4" y="196.2" font-size="12" text-anchor="middle">f(0)</text>
<rect class="box" x="578.0" y="64.0" width="44.9" height="32" rx="8"/>
<rect class="curve2" x="578.0" y="64.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="600.4" y="84.2" font-size="12" text-anchor="middle">f(3)</text>
<rect class="box" x="622.0" y="120.0" width="44.9" height="32" rx="8"/>
<text class="ink" x="644.4" y="140.2" font-size="12" text-anchor="middle">f(1)</text>
</svg>
<figcaption>fib(5)'in çağrı ağacı. Turuncu halkalılar birden çok kez hesaplanan alt problemler: f(3) iki, f(2) üç kez.</figcaption>
</figure>

30'uncu Fibonacci sayısı için iki buçuk milyondan fazla çağrı. Şekilde
`fib(5)` bile `fib(3)`'ü iki, `fib(2)`'yi üç kez hesaplıyor; `n` büyüdükçe
tekrarlar üstel artıyor. Oysa farklı alt problem yalnızca `n + 1` tane:
`fib(0)`'dan `fib(n)`'e.

## Bellekli özyineleme (memoization)

Aynı fonksiyon, yalnızca bir sözlükle: cevabı hesaplamadan önce sözlüğe bak,
hesapladıktan sonra yaz.

```python
memo = {}
memo_calls = 0

def fib_memo(n):
    global memo_calls
    memo_calls += 1
    if n < 2:
        return n
    if n in memo:                          # daha önce çözüldü: oku
        return memo[n]
    memo[n] = fib_memo(n - 1) + fib_memo(n - 2)
    return memo[n]

print(fib_memo(30), memo_calls)
```

```text
832040 59
```

2 692 537 çağrı 59'a indi. Python bunu hazır verir: fonksiyonun üstüne
`@functools.cache` yazınca aynı argümanla gelen çağrı önbellekten döner.

```python
from functools import cache

@cache
def fib_cached(n):
    return n if n < 2 else fib_cached(n - 1) + fib_cached(n - 2)

print(fib_cached(100))
print(fib_cached.cache_info())
```

```text
354224848179261915075
CacheInfo(hits=98, misses=101, maxsize=None, currsize=101)
```

## Tablo doldurma (tabulation)

Bellekli özyineleme yukarıdan aşağı gider. Aynı işi **aşağıdan yukarı**,
özyinelemesiz de yapabilirsin: küçük cevaplardan başlayıp bir tabloyu sırayla
doldur.

```python
def fib_table(n):
    table = [0, 1] + [0] * (n - 1)
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]   # öncekiler hazır
    return table[n]

print(fib_table(30), fib_table(100))
```

```text
832040 354224848179261915075
```

`n` adım, özyineleme derinliği sorunu yok. Burada yalnızca son iki değer
gerektiği için tablo yerine iki değişken bile yeter (`O(1)` bellek).

## Dinamik programlama tarifi

Bir DP çözümü yazarken beş soru:

1. **Durum:** `best[a]` neyi gösteriyor? (ör. "`a` tutarı için en az para")
2. **Geçiş:** `best[a]` küçük durumlardan nasıl hesaplanır?
3. **Taban:** en küçük durumların cevabı ne? (`best[0] = 0`)
4. **Sıra:** tablo hangi sırayla dolmalı ki ihtiyaç duyulan hücreler hazır
   olsun?
5. **Cevap:** tablonun hangi hücresi? (`best[amount]`)

## En az para

Açgözlü yöntem `[1, 3, 4]` paralarıyla 6 için yanılmıştı. DP ile: `a` tutarını
vermenin en az para sayısı, son verilen para `c` ise `best[a − c] + 1`; bütün
paraları dene, en küçüğünü al.

```python
def min_coins(amount, coins):
    best = [0] + [float("inf")] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
    return best

print(min_coins(10, [1, 3, 4]))
```

```text
[0, 1, 2, 1, 1, 2, 2, 2, 2, 3, 3]
```

Tablo 0'dan 10'a kadar her tutarın cevabı. `best[6] = 2` (`3 + 3`); açgözlü
üç demişti. Maliyet `O(tutar × para sayısı)`.

## Kaç farklı yol?

Aynı tabloyla "en az kaç" yerine **"kaç farklı şekilde"** sorusu da
cevaplanır: 10'u 1, 2 ve 5 ile kaç farklı şekilde verebilirsin?

```python
def count_ways(amount, coins):
    ways = [1] + [0] * amount              # 0'ı vermenin tek yolu: hiç para
    for c in coins:                        # dış döngü paralar
        for a in range(c, amount + 1):
            ways[a] += ways[a - c]
    return ways[amount]

print(count_ways(10, [1, 2, 5]), count_ways(100, [1, 5, 10, 25, 50]))
```

```text
10 292
```

Döngülerin sırası önemli: paralar dışta olduğu için `2 + 5` ile `5 + 2` aynı
seçim sayılıyor (kombinasyon). Tutarlar dışta olsaydı sıralanışlar ayrı
sayılırdı.

## En iyi dönem: Kadane

Böl ve Fethet bölümündeki en büyük toplamlı alt dizi, DP ile tek geçişte
çözülür. Durum: `current` = **burada biten** en iyi dönemin toplamı. Geçiş:
ya önceki döneme bu günü ekle ya da bugün yeniden başla.

```python
def kadane(values):
    best = current = values[0]
    for x in values[1:]:
        current = max(x, current + x)      # devam et ya da yeniden başla
        best = max(best, current)
    return best

print(kadane([2, -5, 6, -2, 3, -8, 4]))
```

```text
7
```

Böl ve Fethet bölümündeki 2000 günlük veride de cevap aynı: 1115. Bu kez yalnızca
2000 adımda, `O(n)`.

## Izgarada yollar

Bir ızgaranın sol üst köşesinden sağ alt köşesine yalnızca sağa ve aşağı
giderek kaç yol var? Bir hücreye ya üstünden ya solundan gelinir:
`paths[r][c] = paths[r − 1][c] + paths[r][c − 1]`. Engelli hücreye 0.

```python
def grid_paths(rows, cols, blocked):
    paths = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if (r, c) in blocked:
                continue
            if r == 0 and c == 0:
                paths[r][c] = 1
            else:
                up = paths[r - 1][c] if r else 0
                left = paths[r][c - 1] if c else 0
                paths[r][c] = up + left
    return paths[-1][-1]

print(grid_paths(3, 3, set()), grid_paths(3, 3, {(1, 1)}), grid_paths(10, 10, set()))
```

```text
6 2 48620
```

Bütün yolları tek tek gezmek 10 × 10'da on binlerce yol demek; tablo yalnızca
100 hücre dolduruyor.

## Özet

- DP: örtüşen alt problemleri bir kez çöz, sakla.
- Bellekli özyineleme (yukarıdan aşağı, `@cache`) ya da tablo doldurma
  (aşağıdan yukarı).
- Tarif: durum, geçiş, taban, sıra, cevap.
- En az para, kaç farklı yol, Kadane (`O(n)`), ızgarada yollar.
- Açgözlünün yanıldığı yerde DP kesin cevabı verir; bedeli tablonun boyu
  kadar zaman ve bellek.
