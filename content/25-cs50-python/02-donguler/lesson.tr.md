# Döngüler

CS50 Python'un üçüncü haftası. Videoyu **Video** sekmesinden izleyebilirsin;
bu sayfa dersin yazılı hâli. Döngü (loop), bir işi tekrar tekrar yapmanın
yolu: aynı satırı defalarca yazmak yerine bir bloğu istediğin kadar
çalıştırırsın.

## Aynı satırı üç kez yazmak

`cat.py` adında bir dosya açalım; kedimiz üç kez miyavlasın:

```python
print("meow")
print("meow")
print("meow")
```

```text
$ python cat.py
meow
meow
meow
```

Çalışıyor, ama 500 kez miyavlamak istesek 500 satır mı yazacağız? Programcı
olarak aynı şeyi tekrar tekrar yazdığın her yer, kodu iyileştirebileceğin bir
yer demek.

## while döngüsü

`while` (-dığı sürece) hemen her programlama dilinde bulunan bir döngüdür:
koşul doğru olduğu sürece bloğu yeniden çalıştırır. İlk deneme:

```python
i = 3
while i != 0:
    print("meow")
```

Bu kod **hiç durmaz**: Python her turda "`i` sıfırdan farklı mı?" diye sorar,
`i` hep 3 kaldığı için cevap hep evettir. Böyle bir **sonsuz döngüye**
takılırsan terminalde `Ctrl+C` programı keser. Düzeltmek için her turda `i`'yi
bir azaltalım:

```python
i = 3
while i != 0:
    print("meow")
    i = i - 1
```

```text
$ python cat.py
meow
meow
meow
```

Döngünün bir kez dönmesine **yineleme** (iteration) denir. İnsanların saydığı
gibi 1'den de sayabiliriz:

```python
i = 1
while i <= 3:
    print("meow")
    i = i + 1
```

```text
$ python cat.py
meow
meow
meow
```

`i = i + 1` sağdaki işlemi yapıp sonucu soldaki ada atar. Programcılar ise
saymaya **0'dan** başlar; `i += 1` aynı şeyin kısa yazımıdır:

```python
i = 0
while i < 3:
    print("meow")
    i += 1
```

<figure class="fig"><div class="flow"><span class="node">i = 0</span><span class="arrow">→</span><span class="node">i &lt; 3 ?</span><span class="arrow">→</span><span class="node ok">evetse "meow"</span><span class="arrow">→</span><span class="node">i += 1</span><span class="arrow">→</span><span class="node">yeniden i &lt; 3 ?</span></div><figcaption>Döngü her turda koşulu yeniden sorar; <code>i</code> 3 olunca cevap <b>hayır</b> olur ve döngü biter. <code>i</code> 0, 1, 2 değerlerini alır, 3'e kadar gelir ama 3'te çalışmaz.</figcaption></figure>

(CS50'nin notunda `i = 1` ile başlayan örneğin bütün satırları fazladan
girintili yazılmış; o hâliyle Python `IndentationError` verir. Burada
çalıştırılarak doğrulanmış hâli var.)

## for döngüsü

`for` döngüsünü anlamak için önce yeni bir türe bakalım: **liste** (list).
Alışveriş listesi, yapılacaklar listesi gibi; köşeli parantez içinde,
virgülle ayrılmış değerler: `[0, 1, 2]`. `for` bir listenin elemanlarını
sırayla gezer:

```python
for i in [0, 1, 2]:
    print("meow")
```

```text
$ python cat.py
meow
meow
meow
```

`i` önce 0 olur ve miyavlar, sonra 1, sonra 2. `while` sürümünden çok daha
temiz. Ama bir milyon kez miyavlamak istesek? Listeyi elle yazmak yerine
`range` (aralık) kullanırız; `range(3)` 0, 1, 2 değerlerini kendisi üretir:

```python
for i in range(3):
    print("meow")
```

```text
$ python cat.py
meow
meow
meow
```

`i`'nin aldığı değerleri görmek için onu yazdıralım:

```python
for i in range(3):
    print(i)
```

```text
$ python cat.py
0
1
2
```

Miyavlayan sürümde `i`'yi hiç kullanmıyoruz; Python'a yalnızca sayacı
tutacak bir yer lazım. Böyle bir değişkenin adı geleneksel olarak `_` (alt
çizgi) yazılır; "bu değere ihtiyacım yok" demektir ve programın davranışı
değişmez:

```python
for _ in range(3):
    print("meow")
```

Aklını biraz zorlayalım: bir dizeyi sayıyla çarpmak onu tekrarlar.

```python
print("meow" * 3)
```

```text
$ python cat.py
meowmeowmeow
```

Her `meow` ayrı satırda olsun diye sonuna satır sonu (`\n`) ekleriz; `end=""`
ise `print`'in kendi satır sonunu kapatır, yoksa en sonda fazladan bir boş
satır kalırdı:

```python
print("meow\n" * 3, end="")
```

```text
$ python cat.py
meow
meow
meow
```

## Kullanıcının girdisini döngüyle denetlemek

Döngüler kullanıcının girdisini **denetlemek** için de kullanılır: istenen
türden bir değer gelene kadar yeniden sormak. Python'da yaygın kalıp
`while True` ile kurulur. Kullanıcıdan 0 ya da daha büyük bir sayı isteyelim:

```python
while True:
    n = int(input("What's n? "))
    if n < 0:
        continue
    else:
        break

print("n is", n)
```

```text
$ python cat.py
What's n? -2
What's n? 5
n is 5
```

İki yeni anahtar kelime var. `continue` (devam et) döngünün geri kalanını
atlayıp bir sonraki tura geçer; `break` (kır) döngüden hemen çıkar. `n`
negatifse `continue` ile yeniden sorulur, değilse `break` ile döngüden
çıkılır.

Burada `continue` aslında gereksiz: koşul tutmazsa döngü zaten başa döner.
Bu kez 0'dan **büyük** bir sayı isteyip o kadar miyavlayalım:

```python
while True:
    n = int(input("What's n? "))
    if n > 0:
        break

for _ in range(n):
    print("meow")
```

```text
$ python cat.py
What's n? -1
What's n? 0
What's n? 2
meow
meow
```

`while True` ilk bakışta sonsuza kadar sürecek gibi görünür, çünkü `True` hep
doğrudur. Ama `n` sıfırdan büyük olunca `break` döngüyü kırar.

Geçen haftalardan öğrendiklerimizle işi fonksiyonlara bölelim:

```python
def main():
    meow(get_number())


def get_number():
    while True:
        n = int(input("What's n? "))
        if n > 0:
            return n


def meow(n):
    for _ in range(n):
        print("meow")


main()
```

```text
$ python cat.py
What's n? 3
meow
meow
meow
```

`get_number` içindeki `return n` hem döngüyü hem fonksiyonu bitirir ve değeri
`main`'e geri verir; ayrıca `break` yazmaya gerek kalmaz.

## Listeler üzerine

*Harry Potter*'daki Hogwarts'a dönelim. `hogwarts.py`:

```python
students = ["Hermione", "Harry", "Ron"]

print(students[0])
print(students[1])
print(students[2])
```

```text
$ python hogwarts.py
Hermione
Harry
Ron
```

Listenin elemanlarına konumla erişilir ve konum **0'dan** başlar:
`students[0]` Hermione. Aynı listeyi döngüyle gezmek daha temiz:

```python
students = ["Hermione", "Harry", "Ron"]

for student in students:
    print(student)
```

```text
$ python hogwarts.py
Hermione
Harry
Ron
```

Burada `_` yerine `student` yazdık, çünkü değişkeni gövdede kullanıyoruz.

## Uzunluk

`len` (length, uzunluk) bir listenin kaç elemanlı olduğunu verir. Her
öğrencinin adının yanında sırasını da yazmak istersek:

```python
students = ["Hermione", "Harry", "Ron"]

for i in range(len(students)):
    print(i + 1, students[i])
```

```text
$ python hogwarts.py
1 Hermione
2 Harry
3 Ron
```

`range(len(students))` konumları (0, 1, 2) verir; insanlar 1'den saydığı
için `i + 1` yazdık. `len` sayesinde liste büyüse de kod değişmez.

## Sözlükler

**Sözlük** (`dict`, dictionary) anahtarları (key) değerlere (value) bağlayan
bir veri yapısıdır. Liste birden çok değeri sırayla tutar; sözlük her anahtarı
bir değerle eşleştirir. Öğrencileri binalarına bağlamak için iki liste
kullanabilirdik:

```python
students = ["Hermione", "Harry", "Ron", "Draco"]
houses = ["Gryffindor", "Gryffindor", "Gryffindor", "Slytherin"]
```

Bu, iki listenin hep aynı sırada kalacağına söz vermek demek; listeler
büyüdükçe zahmetli olur. Sözlükle, süslü parantezler `{}` içinde:

```python
students = {
    "Hermione": "Gryffindor",
    "Harry": "Gryffindor",
    "Ron": "Gryffindor",
    "Draco": "Slytherin",
}

print(students["Hermione"])
print(students["Draco"])
```

```text
$ python hogwarts.py
Gryffindor
Slytherin
```

Listede konumla (sayıyla), sözlükte anahtarla (burada bir adla) erişilir. Bir
sözlüğü `for` ile gezersek **anahtarları** alırız:

```python
students = {
    "Hermione": "Gryffindor",
    "Harry": "Gryffindor",
    "Ron": "Gryffindor",
    "Draco": "Slytherin",
}

for student in students:
    print(student)
```

Hem adı hem binayı yazmak için değere `students[student]` ile ulaşırız;
`sep=", "` de araya virgül ve boşluk koyar:

```python
students = {
    "Hermione": "Gryffindor",
    "Harry": "Gryffindor",
    "Ron": "Gryffindor",
    "Draco": "Slytherin",
}

for student in students:
    print(student, students[student], sep=", ")
```

```text
$ python hogwarts.py
Hermione, Gryffindor
Harry, Gryffindor
Ron, Gryffindor
Draco, Slytherin
```

Her öğrenci için daha fazla bilgi tutmak istersek bir **sözlükler listesi**
kurarız. Draco'nun patronusu yok; Python'da "değer yok" `None` ile gösterilir:

```python
students = [
    {"name": "Hermione", "house": "Gryffindor", "patronus": "Otter"},
    {"name": "Harry", "house": "Gryffindor", "patronus": "Stag"},
    {"name": "Ron", "house": "Gryffindor", "patronus": "Jack Russell terrier"},
    {"name": "Draco", "house": "Slytherin", "patronus": None},
]

for student in students:
    print(student["name"], student["house"], student["patronus"], sep=", ")
```

```text
$ python hogwarts.py
Hermione, Gryffindor, Otter
Harry, Gryffindor, Stag
Ron, Gryffindor, Jack Russell terrier
Draco, Slytherin, None
```

## Mario

Klasik *Mario* oyununda kahraman tuğlaların üstünden atlar. Bunun metin
hâlini çizelim. Üç tuğlalık bir sütun, kopyala yapıştır yerine döngüyle ve
bir fonksiyonla:

```python
def main():
    print_column(3)


def print_column(height):
    for _ in range(height):
        print("#")


main()
```

```text
$ python mario.py
#
#
#
```

Sütun istediğimiz kadar uzayabilir; sayıyı koda gömmedik. Yatay bir sıra:

```python
def main():
    print_row(4)


def print_row(width):
    print("?" * width)


main()
```

```text
$ python mario.py
????
```

Oyundaki blokların hem satırı hem sütunu var. İkisini birden çizmek için
**iç içe** döngü: dış döngü her satır için, iç döngü satırdaki her tuğla için
döner. İçteki `print("#", end="")` tuğlaları yan yana dizer, dıştaki boş
`print()` satırı bitirir:

```python
def main():
    print_square(3)


def print_square(size):

    # Her satır için
    for i in range(size):

        # Satırdaki her tuğla için
        for j in range(size):

            # Tuğlayı yaz
            print("#", end="")

        # Satırı bitir
        print()


main()
```

```text
$ python mario.py
###
###
###
```

Bir adım daha soyutlayalım: satırı çizen işi `print_row`'a verelim:

```python
def main():
    print_square(3)


def print_square(size):
    for i in range(size):
        print_row(size)


def print_row(width):
    print("#" * width)


main()
```

```text
$ python mario.py
###
###
###
```

## Özet

Python becerilerine bir yenisi daha eklendi:

- `while` döngüsü, sonsuz döngü ve `Ctrl+C`
- `for` döngüsü, `range` ve `_`
- `while True`, `break` ve `continue` ile girdi denetimi
- Listeler, konumlar (0'dan) ve `len`
- Sözlükler, anahtarlar ve `None`
- İç içe döngüler

## Bu haftanın problem seti

**Alıştırma** sekmesindeki yedi alıştırma bu dersin konularını tek tek
çalıştırıyor. **Problem Seti** sekmesindekiler CS50'nin bu haftaki ödevi
(Problem Set 2):

| Problem | Ne istiyor | Dersteki konu |
|---|---|---|
| camelCase | `firstName` → `first_name` | dizeyi `for` ile gezmek |
| Kola Makinesi | 50 sent dolana kadar para istemek | `while`, sayaç |
| Just setting up my twttr | sesli harfleri atmak | `for`, `in` |
| Kişisel Plakalar | plakanın şartlara uyup uymadığı | `bool` döndüren fonksiyon, `len` |
| Besin Değerleri | meyvenin kalorisi | sözlük, anahtarla erişim |

Bazı problemler dersin göstermediği küçük bir metodu (`isupper`, `isalpha`,
`isdigit`) kullanıyor; yönergelerde ipucu olarak yazılı.

---

*Bu bölüm, Harvard Üniversitesi'nin [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) dersinin 2. haftasından (ders notu ve problem seti) çevrilip uyarlanmıştır; örnekler ve alıştırmalar değiştirildi, problem seti CS50'nin check50'siyle değil Odyssey'nin denetimiyle sınanıyor. Özgün içerik ve bu uyarlama [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) lisanslıdır. Harvard bu uyarlamayı onaylamış değildir.*
