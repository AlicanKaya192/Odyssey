# Hızlı Başvuru

Python Temelleri'nde öğrendiğin her şeyin tek sayfalık özeti. Ezberlemek için
değil, "şu nasıl yazılıyordu" diye bakmak için.

## Değişkenler ve tipler

```python
name = "Ada"          # str
age = 36              # int
ratio = 3.14          # float
active = True         # bool
nothing = None        # NoneType
```

```python
int("42")             # metinden sayiya
str(42)               # sayidan metne
float("3.5")          # ondaliga
type(age)             # tipi ogren
```

## Metin işlemleri

```python
text.strip()              # bas ve sondaki bosluklari at
text.lower()              # kucuk harf
text.upper()              # buyuk harf
text.split(",")           # ayiraca gore bol
text.split(",", 1)        # en fazla bir kez bol
"-".join(parts)           # listeyi metne birlestir
text.replace("a", "b")    # degistir
text.startswith("A")      # ile basliyor mu
len(text)                 # uzunluk
f"{name} is {age}"        # bicimlendirme
```

## Operatörler

```python
7 / 2       # 3.5   ondalikli bolme
7 // 2      # 3     tam bolme
7 % 2       # 1     kalan
2 ** 3      # 8     us
```

```python
==  !=  >  <  >=  <=
and  or  not
in  not in
is  is not          # yalnizca None, True, False ile
```

**Yuvarlamada bir sürpriz var.** Python tam yarımları en yakın **çift**
sayıya yuvarlıyor, yukarıya değil:

```python
round(0.5)     # 0
round(1.5)     # 2
round(2.5)     # 2
round(82.5)    # 82
```

Hata değil, kasıtlı: çok sayıda yuvarlama yapıldığında hep yukarı yuvarlamak
toplamı şişiriyor. Ama beklemiyorsan şaşırtıyor. Her zaman yukarı yuvarlamak
istiyorsan `math.ceil` var.

## Koşullar

```python
if score >= 90:
    grade = "A"
elif score >= 50:
    grade = "B"
else:
    grade = "F"
```

```python
if 18 <= age < 65:        # zincirleme
if not items:             # bos mu
if value is None:         # None kontrolu
```

## Döngüler

```python
for item in items:
    print(item)

for index, item in enumerate(items):
    print(index, item)

for key in scores:
    print(key, scores[key])

while count < 10:
    count = count + 1
```

```python
break          # donguyu bitir
continue       # bu adimi atla
range(5)       # 0 1 2 3 4
range(2, 8)    # 2 ... 7
range(0, 10, 2)   # 0 2 4 6 8
```

## Fonksiyonlar

```python
def greet(name, greeting="hello"):
    return greeting + " " + name

def stats(values):
    return min(values), max(values)     # iki deger doner

low, high = stats([3, 1, 5])
```

`print` gösterir, `return` verir. Karıştırma.

```python
def total(*numbers):        # kac tane gelirse demette toplanir
    return sum(numbers)


def describe(**details):    # adiyla gelenler sozlukte toplanir
    return details


sorted(people, key=lambda p: p["grade"], reverse=True)
```

## Liste üreteçleri

```python
[x * 2 for x in items]                  # her elemani donustur
[x for x in items if x > 0]             # suz
[x.upper() for x in names if len(x) < 5]   # ikisi birden
{k: v for k, v in scores.items()}       # sozluk uretir
```

Tek satıra sığmıyorsa üreteç değil, döngü yaz.

## Doğrulama

```python
assert total([1, 2]) == 3
assert total([]) == 0, "bos liste sifir vermeli"
```

`assert` koşul tutmazsa `AssertionError` çıkarıyor. Küçük betiklerde
"buraya kadar doğru mu" kontrolü için pratik.

## Listeler ve demetler

```python
items = [10, 20, 30]

items[0]          # ilk
items[-1]         # son
items[1:3]        # dilim
items.append(40)
items.insert(0, 5)
items.remove(20)
items.pop()
items.sort()
items.reverse()
len(items)
```

```python
point = (3, 7)        # demet: degistirilemez
single = ("only",)    # tek elemanli demette virgul sart
```

```python
sum(items)   max(items)   min(items)   sorted(items)
```

## Sözlükler

```python
scores = {"Ada": 90, "Alan": 70}

scores["Ada"]              # deger al
scores["Grace"] = 85       # ekle veya degistir
scores.get("Nobody")       # yoksa None, hata vermez
scores.get("Nobody", 0)    # yoksa 0
del scores["Alan"]

"Ada" in scores            # anahtar var mi
scores.keys()
scores.values()
scores.items()
```

```python
for name, value in scores.items():
    print(name, value)
```

## Modüller

```python
import math
from datetime import date
import statistics as stats

math.sqrt(16)
math.floor(3.7)
math.pi

date(2026, 1, 1)
```

```python
if __name__ == "__main__":
    main()
```

## Hata yakalama

```python
try:
    number = int(text)
except ValueError:
    number = 0
except (KeyError, IndexError):
    number = -1
else:
    print("worked")
finally:
    print("done")
```

```python
raise ValueError("age cannot be negative")

except ValueError as error:
    print(error)
```

| Hata | Ne zaman |
|---|---|
| `ValueError` | Tip doğru, değer olmaz |
| `TypeError` | Tip yanlış |
| `KeyError` | Sözlükte yok |
| `IndexError` | Listede yok |
| `FileNotFoundError` | Dosya yok |
| `ZeroDivisionError` | Sıfıra bölme |

## Tip belirtimleri

```python
def repeat(text: str, count: int) -> str:
    return text * count

scores: list[int] = []
ages: dict[str, int] = {}
point: tuple[int, int] = (3, 7)

def find(name: str) -> int | None:
    return None

def greet(name: str) -> None:
    print(name)
```

## Dosyalar

```python
with open("notes.txt", "w", encoding="utf-8") as file:
    file.write("line\n")

with open("notes.txt", "a", encoding="utf-8") as file:
    file.write("more\n")

with open("notes.txt", encoding="utf-8") as file:
    content = file.read()
    # ya da
    lines = file.read().splitlines()
    # ya da
    for line in file:
        print(line.strip())
```

| Kip | Ne yapar |
|---|---|
| `"r"` | Okur (varsayılan) |
| `"w"` | **Siler** ve yazar |
| `"a"` | Sona ekler |
| `"x"` | Dosya varsa hata verir |

## Sınıflar

```python
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def is_passing(self):
        return self.grade >= 50

    def __str__(self):
        return self.name + ": " + str(self.grade)

class Honours(Student):
    def __init__(self, name, grade):
        super().__init__(name, grade)
        self.honours = True
```

```python
ada = Student("Ada", 90)
ada.name
ada.is_passing()
```

## Veritabanı

```python
import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("CREATE TABLE students (name TEXT, grade INTEGER)")
cursor.execute("INSERT INTO students VALUES (?, ?)", ("Ada", 90))
cursor.executemany("INSERT INTO students VALUES (?, ?)", rows)
connection.commit()

cursor.execute("SELECT name, grade FROM students WHERE grade >= ?", (50,))
rows = cursor.fetchall()
row = cursor.fetchone()

connection.close()
```

```sql
SELECT name FROM students WHERE grade >= 50 ORDER BY grade DESC LIMIT 3
SELECT city, AVG(grade) FROM students GROUP BY city
UPDATE students SET grade = ? WHERE name = ?
DELETE FROM students WHERE grade < ?
```
