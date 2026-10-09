# collections

Liste, sözlük, küme ve demet çoğu işi görür. Ama bazı işler her projede
tekrar tekrar yazılır: bir şeyin kaç kez geçtiğini saymak, öğeleri bir
anahtara göre gruplamak, iki uçtan eleman eklenip çıkarılan bir kuyruk,
alanlarına adla erişilen küçük bir kayıt. **`collections`** modülü bunlar
için hazır, hızlı ve okunaklı yapılar verir.

## Counter: saymak

```python
from collections import Counter

words = "the cat and the dog and the bird".split()
counts = Counter(words)
print(counts)
print(counts["the"], counts["fish"])
print(counts.most_common(2))
counts.update(["cat", "cat"])
print(counts["cat"], counts.total())
print(Counter("mississippi").most_common(3))
```

```text
Counter({'the': 3, 'and': 2, 'cat': 1, 'dog': 1, 'bird': 1})
3 0
[('the', 3), ('and', 2)]
3 10
[('i', 4), ('s', 4), ('p', 2)]
```

- **`Counter(liste)`** her öğenin kaç kez geçtiğini sayar; bir sözlük gibi
  davranır.
- Olmayan bir öğe hata vermez, **0** döner (`counts["fish"]`).
- **`most_common(n)`** en sık `n` öğeyi, sayısıyla birlikte, çoktan aza
  verir. Kelime sıklığı, en çok satan ürün, en sık hata mesajı için tek satır.
- `update` yeni öğeleri ekleyip sayar; `total()` bütün sayıların toplamı.
- Metin de verilebilir: harfleri sayar. Eşit sayıda olanlar (`i` ve `s`)
  ilk görüldükleri sırada gelir.

Aynı işi düz sözlükle yapmak `counts[w] = counts.get(w, 0) + 1` döngüsü
isterdi.

## Counter ile hesap

```python
from collections import Counter

a = Counter(apples=3, pears=1)
b = Counter(apples=1, kiwis=2)
print(a + b)
print(a - b)
print(a & b, a | b)
```

```text
Counter({'apples': 4, 'kiwis': 2, 'pears': 1})
Counter({'apples': 2, 'pears': 1})
Counter({'apples': 1}) Counter({'apples': 3, 'kiwis': 2, 'pears': 1})
```

`+` sayıları toplar, `-` çıkarır ve **sıfır ya da eksiye düşenleri atar**
(`kiwis` yok oldu). `&` her öğenin küçük sayısını, `|` büyüğünü alır. İki
depo sayımını birleştirmek ya da "siparişte olup stokta olmayanı" bulmak
için kullanılır.

## defaultdict: eksik anahtarın varsayılanı

```python
from collections import defaultdict

pairs = [("fruit", "apple"), ("veg", "carrot"), ("fruit", "pear"),
         ("veg", "leek"), ("nut", "almond")]
groups = defaultdict(list)
for kind, name in pairs:
    groups[kind].append(name)
print(dict(groups))
counts = defaultdict(int)
for kind, _ in pairs:
    counts[kind] += 1
print(dict(counts))
plain = {}
try:
    plain["fruit"].append("apple")
except KeyError as error:
    print("KeyError:", error)
print(groups["missing"], "missing" in groups)
```

```text
{'fruit': ['apple', 'pear'], 'veg': ['carrot', 'leek'], 'nut': ['almond']}
{'fruit': 2, 'veg': 2, 'nut': 1}
KeyError: 'fruit'
[] True
```

- **`defaultdict(list)`**: olmayan bir anahtara ilk erişildiğinde onun için
  boş bir liste kurar; "anahtar var mı, yoksa boş liste koy" kodu ortadan
  kalkar. **Gruplamanın** kısa yolu.
- `defaultdict(int)`: varsayılan `0`, sayaç gibi.
- Düz sözlükte aynı satır `KeyError` verdi.
- **Dikkat:** yalnızca **okumak** bile anahtarı oluşturur: `groups["missing"]`
  sonrası `missing` artık sözlükte. Var mı diye bakmak için `in` kullan.

## namedtuple: adlı alanlı demet

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p, p.x, p[1])
x, y = p
print((x ** 2 + y ** 2) ** 0.5)
print(p._replace(x=10), p._asdict())
try:
    p.x = 5
except AttributeError as error:
    print("AttributeError:", error)
```

```text
Point(x=3, y=4) 3 4
5.0
Point(x=10, y=4) {'x': 3, 'y': 4}
AttributeError: can't set attribute
```

- **`namedtuple`** bir demet türü üretir: alanlara hem **adla** (`p.x`) hem
  **sırayla** (`p[1]`) erişilir, değişkenlere açılabilir.
- `point[0]` yerine `point.x` yazmak kodu kendi kendini anlatır hâle getirir;
  bir fonksiyondan birden çok değer döndürürken yararlıdır.
- Demet olduğu için **değişmez**: alan atanamaz. Değişmiş bir kopya
  `_replace` ile, sözlük hâli `_asdict()` ile alınır.

Alanları değişebilen, varsayılan değerli, metotlu kayıtlar için İleri Python
modülünde `dataclasses` var.

## deque: iki uçlu kuyruk

```python
from collections import deque

queue = deque(["a", "b", "c"])
queue.append("d")
queue.appendleft("z")
print(queue)
print(queue.popleft(), queue.pop(), queue)
last = deque(maxlen=3)
for n in range(1, 7):
    last.append(n)
print(last)
d = deque([1, 2, 3, 4, 5])
d.rotate(2)
print(d)
```

```text
deque(['z', 'a', 'b', 'c', 'd'])
z d deque(['a', 'b', 'c'])
deque([4, 5, 6], maxlen=3)
deque([4, 5, 1, 2, 3])
```

- **`deque`** (double-ended queue, "dek" okunur) iki uçtan da hızlıca eklenip
  çıkarılan bir listedir: `append` / `appendleft`, `pop` / `popleft`.
- Listede baştan çıkarmak (`list.pop(0)`) arkadaki bütün elemanları kaydırır;
  `deque.popleft()` kaydırmaz. Bu bilgisayarda 100 000 elemanı baştan
  çıkarmak listede yaklaşık 0,9 saniye, `deque`'de 0,005 saniye sürdü.
  Kuyruk (ilk giren ilk çıkar) için `deque` kullan.
- **`maxlen`** verilirse dolunca diğer uçtan eskiyi atar: "son 3 kayıt"
  gibi kayan pencereler için.
- `rotate(n)` elemanları sağa döndürür.

## ChainMap: katmanlı sözlükler

```python
from collections import ChainMap

defaults = {"theme": "dark", "lang": "en", "size": 14}
user = {"lang": "tr"}
settings = ChainMap(user, defaults)
print(settings["lang"], settings["theme"], len(settings))
user["size"] = 16
print(settings["size"], defaults["size"])
```

```text
tr dark 3
16 14
```

`ChainMap` birkaç sözlüğü sırayla arar: önce kullanıcı ayarı, yoksa
varsayılan. Sözlükler kopyalanmaz; `user` değişince `settings` da değişir,
`defaults` olduğu gibi kalır. Ayar katmanları (komut satırı > ortam
değişkeni > dosya > varsayılan) için uygundur.

## Özet

- `Counter`: saymak, `most_common`, `+ - & |`.
- `defaultdict(list)` gruplamak, `defaultdict(int)` saymak; okumak da
  anahtarı oluşturur.
- `namedtuple`: adla erişilen değişmez kayıt.
- `deque`: iki uçtan hızlı ekleme/çıkarma, `maxlen` ile kayan pencere.
- `ChainMap`: sözlükleri katman katman aramak.
