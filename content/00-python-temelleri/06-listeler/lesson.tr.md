# Listeler ve Demetler

Şimdiye kadar her değeri ayrı bir değişkende tuttun. Üç şehir adı için üç
değişken yazdın. Peki yüz şehir olsaydı?

Listeler tam bunun için var: **birden fazla değeri tek bir değişkende**
tutmanı sağlıyorlar.

## Liste oluşturmak

Köşeli parantez açıyorsun, değerleri virgülle ayırıyorsun:

```python
cities = ["Istanbul", "Ankara", "Izmir"]
numbers = [10, 20, 30, 40]
empty = []
```

Bir liste **her türden** değer tutabilir, hatta karışık olabilir:

```python
mixed = ["Python", 1991, True, 3.9]
```

Pratikte aynı türden şeyler koymak işini kolaylaştırır — puan listesi, isim
listesi gibi.

## Sıra numarası

Listedeki her elemanın bir **sıra numarası** (index) var. Ve burada dikkat:
**sıfırdan başlıyor.**

```python
cities = ["Istanbul", "Ankara", "Izmir"]

print(cities[0])     # Istanbul
print(cities[1])     # Ankara
print(cities[2])     # Izmir
```

Üç elemanlı bir listede son elemanın numarası 2. Olmayan bir numara istersen
hata alırsın:

```python
print(cities[3])
# IndexError: list index out of range
```

## Sondan saymak

Negatif numara sondan sayar. Bu, listenin uzunluğunu bilmediğin durumlarda
çok işine yarar:

```python
print(cities[-1])    # Izmir      son eleman
print(cities[-2])    # Ankara     sondan ikinci
```

`cities[-1]` yazmak, `cities[len(cities) - 1]` yazmaktan hem kısa hem okunaklı.

## Dilim almak

İki nokta üst üste ile bir **aralık** alabilirsin:

```python
numbers = [10, 20, 30, 40, 50]

print(numbers[1:3])     # [20, 30]
print(numbers[:2])      # [10, 20]     bastan itibaren
print(numbers[2:])      # [30, 40, 50] sonuna kadar
```

Buradaki kural şu: **başlangıç dâhil, bitiş hariç.** `numbers[1:3]` 1. ve 2.
elemanı verir, 3. elemanı vermez. `range()` fonksiyonundaki mantığın aynısı.

Dilim almak yeni bir liste üretir; asıl listeye dokunmaz.

## Eleman değiştirmek

Listeler **değiştirilebilir**. Bir elemanı sıra numarasıyla yenisiyle
değiştirebilirsin:

```python
cities = ["Istanbul", "Ankara", "Izmir"]
cities[1] = "Bursa"

print(cities)     # ['Istanbul', 'Bursa', 'Izmir']
```

## Eleman eklemek ve çıkarmak

En sık kullanacağın metot `append` — listenin **sonuna** ekler:

```python
cities = ["Istanbul", "Ankara"]
cities.append("Izmir")

print(cities)     # ['Istanbul', 'Ankara', 'Izmir']
```

Çıkarmak için `remove` (değere göre) veya `pop` (sıra numarasına göre):

```python
cities.remove("Ankara")     # degeri silen
cities.pop(0)               # numarasi verilen elemani silen
```

## Uzunluk ve arama

`len()` eleman sayısını verir, `in` bir şeyin listede olup olmadığını söyler:

```python
cities = ["Istanbul", "Ankara", "Izmir"]

print(len(cities))              # 3
print("Ankara" in cities)       # True
print("Konya" in cities)        # False
```

`in` bir **doğruluk değeri** ürettiği için doğrudan `if` içinde kullanılır:

```python
if "Ankara" in cities:
    print("listede var")
```

## Liste üzerinde dönmek

Döngüler bölümünde gördüğün yapı burada da geçerli:

```python
for city in cities:
    print(city)
```

Sıra numarası da lazımsa `enumerate` kullanılır, ama şimdilik buna gerek yok.

## Demetler (tuple)

Demet, listenin **değiştirilemeyen** hâli. Köşeli parantez yerine normal
parantez kullanılır:

```python
point = (3, 5)
colors = ("red", "green", "blue")

print(point[0])     # 3
```

Okumanın her yolu listedekiyle aynı: sıra numarası, negatif numara, dilim,
`len`, `in`, döngü. Ama değiştiremezsin:

```python
point[0] = 10
# TypeError: 'tuple' object does not support item assignment
```

**Neden böyle bir şey isteyelim?** İki sebebi var. Birincisi, değişmemesi
gereken şeyleri demet yaparsan yanlışlıkla değiştiremezsin — bir koordinat,
bir tarih, bir ayar. İkincisi, okuyan kişi demet görünce "bu değişmeyecek"
bilgisini bedavaya alır.

---

## Özet

- Liste birden fazla değeri tek değişkende tutar: `[1, 2, 3]`.
- Sıra numarası **sıfırdan** başlar; `-1` son elemanı verir.
- Dilim alırken **başlangıç dâhil, bitiş hariç**: `numbers[1:3]`.
- Listeler değiştirilebilir; `append`, `remove`, `pop` ile büyüyüp küçülür.
- `len()` uzunluğu, `in` içerip içermediğini söyler.
- Demet `( )` ile yazılır ve değiştirilemez; okuma tarafı listeyle aynıdır.
