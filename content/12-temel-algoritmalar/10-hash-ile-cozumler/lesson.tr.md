# Hash ile Çözümler

Önceki bölümlerde küme ve sözlüğün "içinde var mı?" sorusunu ortalama `O(1)`'de
cevapladığını ölçtük ve birçok algoritmayı bu sayede `O(n²)`'den `O(n)`'e
indirdik. Bu bölümde bunun **nasıl** mümkün olduğunu görecek, sonra en sık
kullanılan **hash kalıplarını** toplayacağız.

## Hash fonksiyonu: değerden adrese

**Hash fonksiyonu** bir değeri alıp ondan bir **tam sayı** üretir. Python'da
yerleşik `hash()` fonksiyonu bunu yapar:

```python
print(hash(42), hash(42) == hash(42))
print(hash((1, 2)) == hash((1, 2)))
try:
    hash([1, 2])
except TypeError as error:
    print(type(error).__name__, "-", error)
```

```text
42 True
True
TypeError - unhashable type: 'list'
```

İki kural var: **aynı değer her zaman aynı hash'i** verir; ve yalnızca
**değiştirilemeyen** değerlerin (sayı, metin, demet) hash'i alınır. Liste
değişebildiği için hash'lenemez: listenin içeriği değişseydi hash'i de
değişir, sözlükteki yerini kaybederdi.

## Sözlüğün içi: kovalar

Sözlük, içinde bir dizi **kova** tutar. Bir anahtarı yerleştirirken hash'ini
alıp kova sayısına böler; **kalan**, anahtarın kovasıdır. Aramada da aynı
hesap yapılır ve doğrudan o kovaya bakılır; bütün sözlüğü gezmeye gerek yok.

Bunu 8 kovalı küçük bir tabloyla kendimiz yazalım (anahtarlar öğrenci
numarası, değerler yaş):

```python
class TinyMap:
    def __init__(self, size=8):
        self.buckets = [[] for _ in range(size)]

    def _bucket(self, key):
        return self.buckets[hash(key) % len(self.buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:          # anahtar zaten varsa değeri güncelle
                pair[1] = value
                return
        bucket.append([key, value])

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

ages = TinyMap()
for student_id, age in [(10, 31), (3, 25), (18, 40), (26, 19), (7, 52)]:
    ages.put(student_id, age)
for i, bucket in enumerate(ages.buckets):
    print(i, bucket)
print(ages.get(18), ages.get(99))
```

```text
0 []
1 []
2 [[10, 31], [18, 40], [26, 19]]
3 [[3, 25]]
4 []
5 []
6 []
7 [[7, 52]]
40 None
```

Tam sayının hash'i kendisi olduğu için 10, 18 ve 26'nın 8'e bölümünden kalan
aynı (2): üçü **aynı kovaya** düştü. Buna **çakışma (collision)** denir. Çakışma
olunca kovanın içindeki birkaç elemana tek tek bakılır; kovalar kısa kaldıkça
bu birkaç adım sabittir: **ortalama `O(1)`**.

<figure class="fig">
  <div class="flow">
    <span class="node">Anahtar: 18</span><span class="arrow">→</span>
    <span class="node">hash(18) = 18</span><span class="arrow">→</span>
    <span class="node">18 % 8 = 2</span><span class="arrow">→</span>
    <span class="node acc">Kova 2</span>
  </div>
  <figcaption>Aramada aynı hesap yapılır; yalnızca 2. kovadaki üç çifte bakılır, öbür yedi kovaya hiç dokunulmaz.</figcaption>
</figure>

Gerçek sözlük çakışmaları başka bir yöntemle (boş yer arayarak) çözer ve
doldukça **kova sayısını büyütüp** her şeyi yeniden yerleştirir; listedeki
`append` gibi, bu yeniden kurma seyrek olduğu için ortalaması sabit kalır.

## Kendi sınıfın sözlükte

Kendi sınıfının nesnelerini küme ya da sözlükte kullanırken Python varsayılan
olarak **nesnenin kimliğine** bakar: içeriği aynı iki nesne farklı sayılır.
"Aynı içerik aynı nesne" demek için hem `__eq__` hem `__hash__` yazılır:

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

class Point2:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    def __hash__(self):
        return hash((self.x, self.y))

a, b = Point(1, 2), Point(1, 2)
c, d = Point2(1, 2), Point2(1, 2)
print(a == b, len({a, b}))
print(c == d, len({c, d}))
```

```text
False 2
True 1
```

Kural: **eşit olan iki nesnenin hash'i de eşit olmalı.** `__eq__` yazıp
`__hash__`'i unutursan Python nesneyi hash'lenemez yapar. Kolay yol: `x` ve
`y`'yi bir **demet** olarak hash'lemek.

## Hash kalıpları

Aşağıdaki kalıpların hepsi listeyi **bir kez** gezer ve her adımda bir küme
ya da sözlüğe sorar: `O(n)`.

**1. Görüldü mü? (küme)** İlk tekrar eden eleman, tekrarları ayıklamak, iki
listenin ortakları. Önceki bölümlerde yaptık.

**2. Kaç kez? (sayaç sözlüğü)** Kelime sıklığı, en sık değer.
`collections.Counter` hazırı.

**3. Tümleyeni ara (two-sum).** Sırasız bir listede toplamı `target` olan iki
elemanın **indeksleri**. Her `x` için tümleyeni `target - x` daha önce görüldü
mü?

```python
def two_sum(numbers, target):
    seen = {}                          # değer → indeks
    for i, x in enumerate(numbers):
        if target - x in seen:
            return seen[target - x], i
        seen[x] = i
    return None

print(two_sum([8, 3, 11, 5, 7], 12))
print(two_sum([8, 3, 11, 5, 7], 100))
```

```text
(3, 4)
None
```

`3 + 9`? 9 yok. `5 + 7 = 12`: 5 indeks 3'te, 7 indeks 4'te. İki işaretçi
**sıralı** liste istiyordu; hash sırasız listede de `O(n)`. Bedeli `O(n)` ek
bellek.

**4. Ortak anahtarla grupla.** Aynı harflerden oluşan kelimeleri (anagram)
gruplamak: her kelimenin **sıralı harfleri** ortak anahtar olur.

```python
def group_anagrams(words):
    groups = {}
    for w in words:
        key = "".join(sorted(w))       # "listen" → "eilnst"
        groups.setdefault(key, []).append(w)
    return list(groups.values())

print(group_anagrams(["listen", "silent", "enlist", "google", "gogole", "cat"]))
```

```text
[['listen', 'silent', 'enlist'], ['google', 'gogole'], ['cat']]
```

İyi bir anahtar seçmek, hash çözümünün asıl ustalığıdır: "hangi bilgiyi
anahtar yaparsam aynı gruptakiler aynı anahtara düşer?"

## Dikkat edilecekler

- **Metinlerin hash'i her çalıştırmada değişir.** Python güvenlik için
  metin hash'ine her süreçte farklı bir rastgele tohum ekler (Büyük Veri
  patikasının MapReduce bölümünde ölçmüştük). Hash değerini dosyaya yazıp
  sonra kullanma; kararlı bir sayı gerekiyorsa `zlib.crc32` ya da `hashlib`.
- **Kümenin sırası yok.** Sıraya ihtiyacın varsa kümeyi yalnızca "görüldü
  mü?" için kullan, sırayı ayrı bir listede tut.
- **Değiştirilebilir anahtar yok.** Liste anahtar olamaz; demete çevir
  (`tuple(items)`).

## Özet

- Hash fonksiyonu değerden tam sayı üretir; eşit değerler eşit hash verir.
- Sözlük ve küme anahtarı `hash % kova_sayısı` kovasına koyar; arama doğrudan
  o kovaya bakar: ortalama `O(1)`.
- Çakışmada kovadaki birkaç eleman denetlenir; tablo doldukça büyütülür.
- Kendi sınıfını anahtar yapmak için `__eq__` ve `__hash__` birlikte.
- Kalıplar: görüldü mü (küme), kaç kez (sayaç), tümleyeni ara (two-sum), ortak
  anahtarla grupla (anagram); hepsi `O(n)` süre, `O(n)` ek bellek.
