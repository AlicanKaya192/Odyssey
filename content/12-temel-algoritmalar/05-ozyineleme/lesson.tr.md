# Özyineleme

Bazı problemler kendi küçük kopyalarından oluşur. Bir klasörün boyutu, içindeki
dosyaların ve **alt klasörlerin boyutlarının** toplamıdır; alt klasörün boyutu
da aynı şekilde bulunur. `5!` (5 faktöriyel) `5 × 4!`'tür; `4!` de `4 × 3!`.
Böyle problemleri çözmenin doğal yolu, bir fonksiyonun **kendini
çağırmasıdır**. Buna **özyineleme (recursion)** denir.

## İki parça: temel durum ve özyinelemeli adım

Her özyinelemeli fonksiyonun iki parçası olmalı:

- **Temel durum (base case):** cevabı doğrudan bilinen en küçük problem.
  Burada fonksiyon kendini **çağırmaz**. `1! = 1`.
- **Özyinelemeli adım (recursive case):** problemi **daha küçük** bir
  kopyasına indirip kendini onunla çağırmak. `n! = n × (n−1)!`.

```python
def factorial(n):
    if n <= 1:                     # temel durum
        return 1
    return n * factorial(n - 1)    # özyinelemeli adım: n küçülüyor
```

Her çağrıda `n` bir azalıyor ve sonunda temel duruma varıyor. Bu iki şart
(temel durum var ve her adım ona yaklaşıyor) sağlanmazsa fonksiyon hiç
bitmez.

## Çağrı yığını

Bir fonksiyon başka bir fonksiyonu çağırınca, Python yarım kalan işi (hangi
satırda kaldı, değişkenleri ne) bir kenara koyar ve çağrılanı çalıştırır.
Bu kenara koyma yerine **çağrı yığını (call stack)** denir: tabak yığını
gibi, en son konan en önce alınır. Özyinelemede aynı fonksiyonun birçok
kopyası yığında üst üste durur. Bunu görmek için her çağrıyı girintiyle
yazdıralım:

```python
def factorial(n, depth=0):
    print("  " * depth + f"factorial({n}) cagrildi")
    if n <= 1:
        result = 1
    else:
        result = n * factorial(n - 1, depth + 1)
    print("  " * depth + f"factorial({n}) = {result}")
    return result

factorial(4)
```

```text
factorial(4) cagrildi
  factorial(3) cagrildi
    factorial(2) cagrildi
      factorial(1) cagrildi
      factorial(1) = 1
    factorial(2) = 2
  factorial(3) = 6
factorial(4) = 24
```

Önce dört çağrı üst üste yığıldı (her biri bir öncekinin cevabını
bekliyor). `factorial(1)` temel durumdu ve hemen döndü; sonra yığın tersten
çözüldü: 1, 2, 6, 24. Bu iki yönlü hareketi (inerken bekleyen çağrılar,
çıkarken birleşen sonuçlar) görmek özyinelemeyi anlamanın anahtarı.
Alıştırmalarda **Adım adım** düğmesi yığını değişkenler bölümünde katman
katman gösteriyor.

## Temel durumu unutursan

Temel durumu olmayan bir fonksiyon kendini sonsuza kadar çağırmaya çalışır.
Python yığını korumak için bir sınır koyar:

```python
import sys
print(sys.getrecursionlimit())

def countdown(n):
    return countdown(n - 1)       # temel durum yok

try:
    countdown(5)
except RecursionError as error:
    print(type(error).__name__, "-", error)
```

```text
1000
RecursionError - maximum recursion depth exceeded
```

Sınır yaklaşık **1000** çağrı derinliği. Bu yüzden Python'da
derinliği on binlere çıkabilecek işler (uzun bir listeyi elemanı elemanına
özyinelemeyle gezmek gibi) döngüyle yazılır. Bu bir hatanın değil, Python'un
bir tercihinin sonucu: bazı dillerin aksine Python özyinelemeli çağrıları
döngüye çevirerek hızlandırmaz.

## Özyinelemeyle düşünmek

Bir problemi özyinelemeyle çözmek için kendine üç soru sor:

1. **En küçük hâli ne, cevabı ne?** (Boş liste → toplam 0.)
2. **Bir adım küçültürsem ne kalır?** (İlk eleman ve geri kalan liste.)
3. **Küçüğün cevabını bilseydim, büyüğünkini nasıl kurardım?**
   (İlk eleman + geri kalanın toplamı.)

```python
def total(items):
    if not items:                        # 1. boş liste
        return 0
    return items[0] + total(items[1:])   # 2-3. ilk + geri kalanın toplamı
```

Üçüncü soruda **küçüğün cevabının doğru geldiğine güvenmek** gerekir; her
katı kafanda tek tek izlemeye çalışmak yerine "fonksiyon küçük girdide doğru
çalışıyor, ben yalnızca son adımı kuruyorum" diye düşün. Buna bazen
**özyinelemeli inanç sıçraması** denir.

Not: `items[1:]` her çağrıda listenin kopyasını kurar; bu örnek fikri
göstermek için. Uzun listede indeksle ilerlemek (`total(items, i + 1)`) daha
ucuzdur.

## Özyinelemenin parladığı yerler

Bir döngüyle de yazılabilen işlerde özyineleme çoğu zaman gereksizdir. Ama
**iç içe yapılarda** özyineleme en doğal yoldur, çünkü yapının kendisi
özyinelemelidir:

```python
def deep_sum(items):
    result = 0
    for item in items:
        if isinstance(item, list):
            result += deep_sum(item)      # alt liste: aynı problem, daha küçük
        else:
            result += item
    return result

print(deep_sum([1, [2, 3], [4, [5, [6]]]]))
```

```text
21
```

Listenin kaç kat iç içe olduğunu önceden bilmiyoruz; döngüyle yazmak için
kendi yığınımızı tutmamız gerekirdi. Klasör ağaçları, JSON belgeleri, karar
ağaçları ve sonraki bölümlerdeki **ağaçlar** hep böyle.

Aynı fikir algoritmalarda da var: bir sonraki bölümdeki **merge sort**
listeyi ikiye bölüp her yarıyı kendisiyle sıralar. İkili arama da
özyinelemeyle yazılabilir: "ortadakine bak, sonra yarıda aynısını yap".

## Dikkat: aynı işi tekrar tekrar yapmak

Fibonacci sayılarının tanımı özyinelemeli: `fib(n) = fib(n−1) + fib(n−2)`,
`fib(0) = 0`, `fib(1) = 1`. Tanımı doğrudan koda çevirip **kaç kez
çağrıldığını** sayalım:

```python
calls = 0

def fib(n):
    global calls
    calls += 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

for n in [10, 20, 25, 30]:
    calls = 0
    print(n, fib(n), calls)
```

```text
10 55 177
20 6765 21891
25 75025 242785
30 832040 2692537
```

`fib(30)` için **milyonlarca** çağrı. Sebep: `fib(30)`, `fib(29)` ve
`fib(28)`'i çağırıyor; `fib(29)` da yine `fib(28)`'i çağırıyor; aynı değerler
defalarca baştan hesaplanıyor. Çağrı sayısı `n` her 1 arttığında yaklaşık
1,6 katına çıkıyor: üstel büyüme. Çözümü (her sonucu bir kez hesaplayıp
saklamak) ALG 2'nin **Dinamik Programlama** bölümünde göreceğiz.

## Özet

- Özyinelemeli fonksiyon kendini **daha küçük** bir girdiyle çağırır.
- Her zaman bir **temel durum** olmalı ve her adım ona yaklaşmalı.
- Çağrılar **çağrı yığınında** birikir; Python'da derinlik sınırı yaklaşık
  1000, aşılınca `RecursionError`.
- Özyinelemeyle düşünmek: en küçük hâl, bir adım küçültme, küçüğün
  cevabından büyüğünkini kurma.
- İç içe yapılarda (ağaçlar, iç içe listeler, klasörler) özyineleme en doğal
  yol; düz bir döngüyle yazılabiliyorsa çoğu zaman döngü daha iyi.
- Aynı alt problemi tekrar tekrar çözen özyineleme üstel büyüyebilir.
