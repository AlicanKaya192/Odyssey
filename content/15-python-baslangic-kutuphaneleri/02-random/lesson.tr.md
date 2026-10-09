# random

Zar atmak, bir listeden rastgele eleman seçmek, kartları karıştırmak, deney
için örneklem çekmek, bir benzetim (simülasyon) kurmak... Bunların hepsi
**`random`** modülüyle yapılır. Bu bölümde rastgele sayının aslında nereden
geldiğini, aynı sonucu tekrar üretmeyi (**tohum**, seed) ve en çok kullanılan
fonksiyonları görüyoruz.

## Tohum: aynı rastgeleliği tekrar üretmek

Bilgisayardaki rastgele sayılar **sözde rastgeledir** (pseudo-random): bir
başlangıç sayısından (tohum) belirli bir hesapla üretilirler. Aynı tohumla
başlarsan aynı diziyi alırsın.

```python
import random

random.seed(42)
x = random.random()
die = random.randint(1, 6)
y = random.uniform(10, 20)
print(round(x, 4), die, round(y, 2))
random.seed(42)
print(round(random.random(), 4))
```

```text
0.6394 1 17.42
0.6394
```

`random()` 0 ile 1 arasında bir ondalık, `randint(1, 6)` 1 ile 6 arasında
(ikisi de dahil) bir tam sayı, `uniform(10, 20)` aralıkta bir ondalık verir.
Tohumu yeniden 42 yapınca ilk sayı yine 0,6394. Bu, deneyleri ve testleri
**tekrarlanabilir** yapar: bir hatayı bulduğunda aynı tohumla aynı durumu
yeniden kurabilirsin.

## Kendi üretecin: random.Random

`random.seed` bütün programın paylaştığı tek bir üreteci ayarlar; başka bir
fonksiyon araya `random` çağırırsa diziniz kayar. Kendi işin için ayrı bir
üreteç kurmak daha güvenlidir:

```python
import random

r = random.Random(7)
colors = ["red", "green", "blue"]
print(r.choice(colors))
print(r.choices(colors, k=5))
print(r.sample(range(1, 50), 6))
deck = list(range(1, 11))
r.shuffle(deck)
print(deck)
```

```text
green
['blue', 'green', 'red', 'blue', 'red']
[38, 4, 33, 14, 3, 6]
[9, 3, 6, 4, 5, 1, 8, 2, 10, 7]
```

- `choice` tek bir eleman seçer.
- `choices(k=5)` **yerine koyarak** beş seçim yapar: aynı eleman tekrar
  gelebilir.
- `sample(…, 6)` **yerine koymadan** altı farklı eleman seçer (piyango gibi).
- `shuffle` listeyi **yerinde** karıştırır ve `None` döndürür; özgün sıra
  kaybolur.

## Ağırlıklı seçim

```python
import random

r = random.Random(7)
counts = {"red": 0, "green": 0, "blue": 0}
for c in r.choices(["red", "green", "blue"], weights=[70, 20, 10], k=10000):
    counts[c] += 1
print(counts)
```

```text
{'red': 6992, 'green': 2012, 'blue': 996}
```

`weights` her seçeneğin olasılık payını verir: 70/20/10 ağırlıkla 10 000
seçimde kırmızı 6992 kez geldi, beklenen 7000'e çok yakın. Ağırlıkların
toplamının 100 olması gerekmez; oranları önemlidir.

## Dağılımlar ve büyük sayılar yasası

```python
import random
import statistics as st

r = random.Random(1)
heights = [r.gauss(170, 10) for _ in range(10000)]
print(round(st.mean(heights), 2), round(st.stdev(heights), 2))
r = random.Random(3)
print(sum(r.randint(1, 6) == 6 for _ in range(60000)))
```

```text
170.03 9.92
9915
```

`gauss(170, 10)` ortalaması 170, standart sapması 10 olan normal dağılımdan
sayı çeker; 10 000 sayının ortalaması 170,03, standart sapması 9,92 çıktı.
60 000 zarda altı 9915 kez geldi; beklenen 10 000. Deneme sayısı arttıkça
oran beklenen değere yaklaşır: **büyük sayılar yasası**.

## Sık hatalar

```python
import random

a = random.Random(5)
b = random.Random(5)
print([a.randint(1, 100) for _ in range(3)], [b.randint(1, 100) for _ in range(3)])
try:
    random.Random(1).sample([1, 2, 3], 5)
except ValueError as error:
    print("ValueError:", error)
```

```text
[80, 33, 95] [80, 33, 95]
ValueError: Sample larger than population or is negative
```

Aynı tohumlu iki üreteç aynı diziyi verir; "iki farklı rastgele dizi"
istiyorsan farklı tohum ver. `sample` popülasyondan fazla eleman isteyince
hata verir; yerine koyarak seçmek gerekiyorsa `choices` kullanılır.

**`random` güvenlik için değildir.** Tohumu bilen herkes diziyi tahmin
edebilir. Parola, jeton, doğrulama kodu üretirken `secrets` modülü kullanılır
(İleri Python modülünde).

## Özet

- Rastgele sayılar bir tohumdan üretilir; aynı tohum aynı dizi.
- Kendi işin için `random.Random(tohum)` ile ayrı üreteç kur.
- `random`, `randint`, `uniform`; `choice`, `choices` (yerine koyarak,
  `weights`), `sample` (yerine koymadan), `shuffle` (yerinde).
- `gauss` normal dağılım; deneme arttıkça oranlar beklenene yaklaşır.
- Güvenlik gerektiren yerde `random` değil `secrets`.
