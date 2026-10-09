# Sayı Algoritmaları

Şifreleme, hash fonksiyonları, rastgele sayı üreteçleri ve büyük veri
kümelerini parçalara bölmek hep aynı birkaç sayı fikrine dayanır: **en büyük
ortak bölen**, **asal sayılar**, **hızlı üs alma** ve **mod aritmetiği**. Bu
bölümde her birinin saf yolunu ve hızlı yolunu yan yana koyup adım sayarak
karşılaştırıyoruz.

## En büyük ortak bölen: Öklid

İki sayının en büyük ortak böleni (EBOB, greatest common divisor, gcd) için
saf yol: küçük sayıdan aşağı doğru her sayıyı dene. **Öklid algoritması** ise
tek bir gözleme dayanır: `a`'yı `b`'ye böldüğünde kalan `r` ise
`gcd(a, b) = gcd(b, r)`. Sayılar her adımda hızla küçülür.

```python
import math


def gcd_slow(a, b):
    steps = 0
    for d in range(min(a, b), 0, -1):
        steps += 1
        if a % d == 0 and b % d == 0:
            return d, steps


def gcd_euclid(a, b):
    steps = 0
    while b:
        a, b = b, a % b
        steps += 1
    return a, steps


print(gcd_slow(1071, 462), gcd_euclid(1071, 462))
print(gcd_slow(832_040, 514_229), gcd_euclid(832_040, 514_229))
print(math.gcd(1071, 462))
```

```text
(21, 442) (21, 3)
(1, 514229) (1, 28)
21
```

İkinci satırdaki sayılar art arda iki Fibonacci sayısı: Öklid için **en kötü
durum** bunlar, ama yine de yarım milyon yerine 28 adım. Öklid'in adım sayısı
küçük sayının basamak sayısıyla orantılıdır: `O(log min(a, b))`. Python'da
hazırı `math.gcd`.

<figure class="fig"><div class="flow"><span class="node">gcd(1071, 462)</span><span class="arrow">→</span><span class="node">gcd(462, 147)</span><span class="arrow">→</span><span class="node">gcd(147, 21)</span><span class="arrow">→</span><span class="node">gcd(21, 0)</span><span class="arrow">→</span><span class="node ok">21</span></div><figcaption>1071 = 2 × 462 + 147, 462 = 3 × 147 + 21, 147 = 7 × 21 + 0. Kalan 0 olunca diğer sayı EBOB.</figcaption></figure>

## Asal sayılar: Eratosthenes kalburu

Bir sayının asal olup olmadığını anlamak için karekökü kadar bölen denemek
yeter: `36 = 4 × 9` ise bölenlerden biri `√36 = 6`'yı geçemez.
Ama `n`'e kadar **bütün** asalları istiyorsan her sayıyı ayrı ayrı denemek
yerine **kalbur (sieve)** daha hızlıdır: her asalın katlarını işaretle,
işaretsiz kalanlar asaldır.

```python
def primes_trial(n):
    found, checks = [], 0
    for x in range(2, n + 1):
        prime = True
        d = 2
        while d * d <= x:                  # yalnızca kareköke kadar
            checks += 1
            if x % d == 0:
                prime = False
                break
            d += 1
        if prime:
            found.append(x)
    return found, checks


def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    marks = 0
    for p in range(2, math.isqrt(n) + 1):
        if is_prime[p]:
            for multiple in range(p * p, n + 1, p):   # p*p'den önceki katlar işaretli
                is_prime[multiple] = False
                marks += 1
    return [x for x in range(n + 1) if is_prime[x]], marks


print(sieve(30)[0])
for n in (10_000, 100_000):
    t, s = primes_trial(n), sieve(n)
    print(n, len(s[0]), t[1], s[1])
```

```text
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
10000 1229 117527 16981
100000 9592 2745694 193078
```

İki yol da aynı asalları buluyor (100 000'e kadar 9592 tane). Deneme bölmesi
yaklaşık 2,7 milyon bölme yaptı, kalbur yaklaşık 193 bin işaretleme: on dört
kat kadar az. Kalburun maliyeti `O(n log log n)`, pratikte `n`'e çok yakın.
Bedeli bellek: `n + 1` uzunlukta bir liste.

## Hızlı üs alma

`3¹⁰⁰⁰⁰⁰⁰`'u hesaplamak için 999 999 çarpma gerekmez. Üs çiftse
`aᵉ = (a²)^(e/2)`, tekse bir `a` ayrılır. Üs her adımda yarıya iner:
**kare alarak üs alma (exponentiation by squaring)**. Her adımda `mod` alınırsa
sayılar da büyümez.

```python
def fast_pow(base, exp, mod):
    result, mults = 1, 0
    base %= mod
    while exp > 0:
        if exp % 2 == 1:                   # üssün bu biti 1
            result = result * base % mod
            mults += 1
        base = base * base % mod           # bir sonraki bit için kare
        mults += 1
        exp //= 2
    return result, mults


MOD = 1_000_000_007
print(fast_pow(3, 1_000_000, MOD))
print(pow(3, 1_000_000, MOD))
print(fast_pow(2, 10, 1000))
```

```text
(64935414, 27)
64935414
(24, 6)
```

Bir milyon yerine 27 çarpma: `O(log e)`. Python'un üç argümanlı `pow`'u aynı
sonucu veriyor; Rabin-Karp'taki `pow(base, m - 1, mod)` de buydu. RSA
şifrelemesi yüzlerce basamaklı üslerle bu yöntem sayesinde çalışır.

## Mod aritmetiği

`a % m`, `a`'nın `m`'ye bölümünden kalandır ve sonuç her zaman `0`..`m − 1`
arasındadır. Toplama ve çarpma mod ile uyumludur:
`(a + b) % m = (a % m + b % m) % m`, çarpma için de aynısı. Bu yüzden ara
sonuçlarda mod alarak büyük sayılarla uğraşmadan doğru sonuca ulaşılır.
`1_000_000_007` gibi büyük bir asal, hash ve sayma problemlerinde sık
kullanılan moddur.

## Makine öğrenmesinde: hashing trick

Metni sayıya çevirirken her kelimeye bir sütun açmak, sözlük büyüdükçe belleği
şişirir. **Hashing trick** kelimenin hash'inin `mod`'unu sütun numarası yapar:
sütun sayısı sabit kalır, sözlük tutulmaz. Python'un `hash()`'i her çalıştırmada
değişebildiği için kararlı bir hash (`zlib.crc32`) kullanılır.

```python
import zlib


def hashed_counts(text, buckets):
    vector = [0] * buckets
    for word in text.lower().split():
        vector[zlib.crc32(word.encode()) % buckets] += 1
    return vector


print(hashed_counts("the cat sat on the mat", 8))
words = "the cat sat on mat".split()
print([zlib.crc32(w.encode()) % 8 for w in words])
```

```text
[3, 0, 1, 0, 0, 0, 2, 0]
[6, 0, 0, 0, 2]
```

`the` iki kez geçtiği için 6. sütunda 2 var. Ama `cat`, `sat` ve `on` aynı
sütuna (0) düştü: **çakışma**. Sütun sayısı artınca çakışma azalır;
scikit-learn'ün `HashingVectorizer`'ı varsayılan olarak 2²⁰ sütun kullanır.

## Özet

- Öklid: `gcd(a, b) = gcd(b, a % b)`, `O(log min(a, b))`; hazırı `math.gcd`.
- Asallık için kareköke kadar bölen yeter; bütün asallar için kalbur.
- Hızlı üs alma: üssü yarılayarak `O(log e)` çarpma; `pow(a, e, m)`.
- Mod aritmetiği: ara sonuçlarda mod almak sonucu değiştirmez.
- Hashing trick: `hash % sütun` ile sabit boyutlu öznitelik vektörü;
  çakışmaya dikkat.
