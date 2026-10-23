# Genel Tekrar

CS50 Python'un on haftasının sonuna geldin. İlk hafta `print` ile bir satır
yazdırıyordun; şimdi dosya okuyan, komut satırından seçenek alan, girdiyi
düzenli ifadeyle denetleyen, kendi sınıflarını kuran ve testlerini yazdığın
programlar yazabiliyorsun. Bu bölüm yolu bir kez daha yürüyor; sonunda
haftaların araçlarını birlikte kullanan bir program var. Sınavda her
haftadan dört soru, alıştırmalarda birkaç haftayı birleştiren beş problem
seni bekliyor.

<figure class="fig">
  <div class="flow">
    <span class="node">Temeller<br><small>0–3</small></span><span class="arrow">→</span>
    <span class="node">Araçlar<br><small>4–5</small></span><span class="arrow">→</span>
    <span class="node">Veri<br><small>6–7</small></span><span class="arrow">→</span>
    <span class="node">Sınıflar<br><small>8</small></span><span class="arrow">→</span>
    <span class="node acc">Son Dokunuşlar<br><small>9</small></span>
  </div>
  <figcaption>Dersin yolu: önce dilin temelleri, sonra başkalarının kodunu kullanmak ve kendi kodunu sınamak, sonra dosyalar ve metin, en sonda kendi türlerin ve küçük araçlar.</figcaption>
</figure>

## Hafta 0: Fonksiyonlar ve değişkenler

| Yazım | Ne yapar |
|---|---|
| `name = input("What's your name? ")` | kullanıcıdan bir **dize** alır |
| `int(...)`, `float(...)` | dizeyi sayıya çevirir |
| `print("a", "b", sep="-", end="")` | ayraç ve satır sonu seçilebilir |
| `f"{x:.2f}"` | f-string, virgülden sonra iki basamak |
| `def hello(to="world"):` | varsayılan değerli parametre |
| `return` | fonksiyonun sonucu; yoksa `None` |

## Hafta 1: Koşullar

| Yazım | Ne yapar |
|---|---|
| `if` / `elif` / `else` | ilk tutan dal çalışır |
| `and`, `or`, `not` | koşulları birleştirir; `name == "a" or name == "b"` |
| `n % 2 == 0` | çift mi |
| `match name:` / <code>case "Harry" &#124; "Ron":</code> / `case _:` | değere göre dallanma |

## Hafta 2: Döngüler

| Yazım | Ne yapar |
|---|---|
| `for i in range(3):` | 0, 1, 2 |
| `while True:` ... `break` | geçerli girdi gelene kadar sor |
| `for x in liste:` | listenin öğeleri |
| `for key in sozluk:` / `sozluk[key]` | sözlüğün anahtarları ve değerleri |
| `liste[-1]`, `len(liste)` | son öğe, uzunluk |

## Hafta 3: İstisnalar

```python
while True:
    try:
        x = int(input("What's x? "))
    except ValueError:
        print("x is not an integer")
    else:
        break
```

- `try` yalnızca hata verebilecek satırı sarar; `else` hata çıkmazsa çalışır.
- `except ValueError: pass` hatayı yakalayıp hiçbir şey yapmaz.
- `raise ValueError("...")` kendi kodunda hata yükseltir.

## Hafta 4: Kütüphaneler

| Yazım | Ne yapar |
|---|---|
| `import random` / `random.choice(...)` | modülü getirir |
| `from random import choice` | yalnızca bir adı getirir |
| `sys.argv` | komut satırı argümanları; `[0]` programın adı |
| `sys.exit("mesaj")` | iletiyi yazıp 1 koduyla çıkar |
| `pip install cowsay` | PyPI'dan paket kurar |
| `requests.get(url).json()` | bir API'den JSON |

## Hafta 5: Birim testleri

```python
import pytest
from calculator import square


def test_square():
    assert square(2) == 4
    assert square(-3) == 9


def test_str():
    with pytest.raises(TypeError):
        square("cat")
```

- Dosya ve fonksiyon adları `test_` ile başlar; `pytest test_calculator.py`.
- Test edilen fonksiyon yazdırmaz, **döndürür**.
- `if __name__ == "__main__": main()` modülü içe aktarınca `main`'in
  çalışmasını önler.

## Hafta 6: Dosya işlemleri

| Yazım | Ne yapar |
|---|---|
| `with open("names.txt") as file:` | okur, sonunda kendiliğinden kapatır |
| `open(..., "w")` / `open(..., "a")` | baştan yazar / sonuna ekler |
| `line.rstrip()` | satır sonunu atar |
| `csv.DictReader(file)` | her satır başlık adlarıyla bir sözlük |
| `csv.DictWriter(file, fieldnames=[...])` | sözlükleri CSV'ye yazar |
| `sorted(rows, key=lambda r: r["name"])` | anahtara göre sıralar |
| `Image.open(...)` (Pillow) | resim dosyaları |

## Hafta 7: Düzenli ifadeler

| Kalıp | Anlamı |
|---|---|
| `.` / `\.` | herhangi bir karakter / gerçek nokta |
| `*`, `+`, `?`, `{2}`, `{2,4}` | tekrar sayısı |
| `^`, `$` | metnin başı ve sonu |
| `[A-Z]`, `[^@]`, `\d`, `\w`, `\s` | karakter kümeleri |
| `(...)`, `(?:...)`, <code>&#124;</code> | grup, yakalamayan grup, ya da |

- `re.search` metnin bir yerinde, `re.fullmatch` metnin tamamında arar.
- `matches.group(1)` birinci grubu verir; tutmazsa `re.search` `None` döndürür.
- `re.sub(kalıp, yeni, metin)` değiştirir; kalıplar `r"..."` ham dize.

## Hafta 8: Nesne yönelimli programlama

| Yazım | Ne yapar |
|---|---|
| `class Student:` / `Student("Harry", "Gryffindor")` | yeni tür / nesne |
| `def __init__(self, name):` / `self.name = name` | nesneyi başlatır |
| `def __str__(self): return ...` | `print(nesne)` bunu kullanır |
| `@property` / `@house.setter` | atamada denetim |
| `@classmethod` / `cls` | nesnesiz çağrılan metot |
| `class Student(Wizard):` / `super().__init__(name)` | kalıtım |
| `def __add__(self, other):` | `+` işlecine anlam verir |

## Hafta 9: Son dokunuşlar

| Yazım | Ne yapar |
|---|---|
| `set()`, `add` | her değer bir kez |
| `global balance` | genel değişkeni değiştirmek |
| `def meow(n: int) -> str:` | tip belirtimi; mypy denetler |
| `argparse` | komut satırı seçenekleri, `-h` |
| `f(*liste)`, `f(**sozluk)`, `def f(*args, **kwargs)` | açmak ve toplamak |
| `map`, `filter`, `[... for ... if ...]`, `{k: v for ...}` | dönüştürmek, elemek, kavramalar |
| `enumerate(liste, start=1)` | sıra ve öğe |
| `yield` | değerleri birer birer veren üreteç |

## Hepsi bir arada

Bir öğrenci listesi, `students.csv`:

```text
name,house
Hermione,Gryffindor
Harry,Gryffindor
ron,Gryffindor
Draco,Slytherin
Luna,Ravenclaw
Cedric,Hufflepuff
```

Aşağıdaki program dosyanın adını komut satırından alıyor (hafta 4), CSV'yi
okuyor (hafta 6), her adı bir düzenli ifadeyle denetleyen bir sınıfla
öğrenci kuruyor (haftalar 7 ve 8), geçersiz satırı istisnayla yakalayıp
atlıyor (hafta 3), öğrencileri bir üreteçle veriyor, `enumerate` ile
numaralıyor ve binaları bir küme kavramasıyla topluyor (hafta 9):

```python
import csv
import re
import sys


class Student:
    def __init__(self, name, house):
        if not re.fullmatch(r"[A-Z][a-z]+", name):
            raise ValueError(f"Invalid name: {name}")
        self.name = name
        self.house = house

    def __str__(self):
        return f"{self.name} from {self.house}"


def read_students(path):
    with open(path) as file:
        for row in csv.DictReader(file):
            try:
                yield Student(row["name"], row["house"])
            except ValueError as e:
                print(e)


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python roster.py FILE")
    students = list(read_students(sys.argv[1]))
    for i, student in enumerate(sorted(students, key=lambda s: s.name), start=1):
        print(i, student)
    houses = {student.house for student in students}
    print(*sorted(houses), sep=", ")


if __name__ == "__main__":
    main()
```

```text
$ python roster.py students.csv
Invalid name: ron
1 Cedric from Hufflepuff
2 Draco from Slytherin
3 Harry from Gryffindor
4 Hermione from Gryffindor
5 Luna from Ravenclaw
Gryffindor, Hufflepuff, Ravenclaw, Slytherin
```

`ron` küçük harfle başladığı için `Student` onu reddetti ve program onu
atlayıp devam etti. Dosya adı verilmezse:

```text
$ python roster.py
Usage: python roster.py FILE
```

Bu kodun her satırı on haftanın birinden. `{student.house for student in
students}` bir **küme kavraması**: süslü parantez ama `anahtar: değer`
yok; aynı bina bir kez giriyor.

## Bundan sonra

CS50'de dersin son adımı bir **final projesi**: kendi seçtiğin, seni
ilgilendiren bir problemi Python'la çözmek. Buradan Sonrası notunda
Odyssey'de devam edebileceğin yollar var.

---

*Bu bölüm, Harvard Üniversitesi'nin [CS50's Introduction to Programming
with Python](https://cs50.harvard.edu/python/) dersinin bütününden
uyarlanmıştır; sorular ve alıştırmalar Odyssey'ye aittir. Özgün içerik ve
bu uyarlama [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
lisanslıdır. Harvard bu uyarlamayı onaylamış değildir.*
