Adı iki alt çizgiyle başlayıp biten metotlara **özel metot** deniyor:
`__init__`, `__str__`, `__len__`. Bunları doğrudan çağırmıyorsun; Python
belirli durumlarda kendisi çağırıyor.

Konuşma dilinde "dunder" deniyor — *double underscore* kısaltması.

## Nasıl çalışıyorlar?

Yazdığın şey soldaki, Python'un çağırdığı sağdaki:

| Sen ne yazarsın | Python ne çağırır |
|---|---|
| `Student("Ada")` | `__init__` |
| `print(ada)` | `__str__` |
| `len(basket)` | `__len__` |
| `a == b` | `__eq__` |
| `a < b` | `__lt__` |
| `item in basket` | `__contains__` |
| `basket[0]` | `__getitem__` |
| `for x in basket` | `__iter__` |

Yani Python'un yerleşik işlevlerini kendi sınıfına **öğretiyorsun.**

## `__init__` — kurucu

Zaten biliyorsun. Nesne kurulurken çalışıyor ve başlangıç verisini
yerleştiriyor.

```python
class Basket:
    def __init__(self):
        self.items = []
```

Bir şey döndürmüyor. `return` yazmak hata veriyor.

## `__str__` — insana görünen hâli

```python
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __str__(self):
        return self.name + " (" + str(self.grade) + ")"


print(Student("Ada", 90))
```

```
Ada (90)
```

Metin **döndürüyor.** İçinde `print` yazmak yaygın bir hata.

### `__repr__` ile farkı

`__str__` insan için, `__repr__` geliştirici için:

```python
class Student:
    def __str__(self):
        return self.name

    def __repr__(self):
        return "Student(" + repr(self.name) + ")"


ada = Student("Ada")

print(ada)
print([ada])
```

```
Ada
[Student('Ada')]
```

Dikkat: bir nesne **liste içindeyken** `__str__` değil `__repr__`
kullanılıyor. Bu yüzden yalnızca `__str__` yazdıysan listeler hâlâ
`<__main__.Student object at ...>` gösteriyor.

Tek bir tane yazacaksan `__repr__` yaz — `__str__` tanımlı değilse Python
onun yerine `__repr__` kullanıyor. Tersi geçerli değil.

## `__len__` — uzunluk

```python
class Basket:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def __len__(self):
        return len(self.items)


basket = Basket()
basket.add("apple")
basket.add("bread")

print(len(basket))
```

```
2
```

`__len__` bir **tam sayı** döndürmek zorunda. Metin ya da ondalıklı sayı
döndürürsen `TypeError` alıyorsun.

Bir yan etkisi var: `__len__` tanımlıysa nesne doğruluk değeri de kazanıyor.
Uzunluk sıfırsa nesne `False` sayılıyor:

```python
if basket:
    print("not empty")
```

## `__eq__` — eşitlik

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


print(Point(1, 2) == Point(1, 2))
```

```
True
```

Yazmasaydın `False` gelirdi — Python varsayılan olarak "aynı nesne mi" diye
bakıyor.

**Dikkat:** `__eq__` yazdığın anda nesnen sözlük anahtarı ya da küme elemanı
olamıyor. Olmasını istiyorsan `__hash__` da yazman gerekiyor:

```python
    def __hash__(self):
        return hash((self.x, self.y))
```

## `__contains__` — `in` operatörü

```python
class Basket:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def __contains__(self, item):
        return item in self.items


basket = Basket()
basket.add("apple")

print("apple" in basket)
print("bread" in basket)
```

```
True
False
```

## Ne kadarını yazmalı?

Hepsini değil. Pratikte sıralama şöyle:

- **`__init__`** — neredeyse her sınıfta.
- **`__repr__`** — hata ayıklarken çok işe yarıyor, yazmaya değer.
- **`__str__`** — nesne kullanıcıya gösterilecekse.
- **`__eq__`** — nesneleri değere göre karşılaştıracaksan.
- **`__len__`, `__contains__`, `__getitem__`** — nesnen bir **kap** gibi
  davranacaksa.

Gerisi ileri seviye ve nadiren gerekiyor.

## Nerede karşına çıkacak?

Bunlar Python'un her yerinde. `len("abc")` çalışıyor çünkü `str` sınıfının
`__len__` metodu var. `[1, 2] + [3]` çalışıyor çünkü `list` sınıfının
`__add__` metodu var.

Veri bilimine geçtiğinde pandas'ın `table["score"]` yazımını göreceksin — o
da `__getitem__`. Yani öğrendiğin şey, kütüphanelerin nasıl yazıldığı.
