# Son Dokunuşlar

CS50 Python'un onuncu ve son haftası. Videoyu **Video** sekmesinden
izleyebilirsin; bu sayfa dersin yazılı hâli. Şimdiye kadar fonksiyonlar,
koşullar, döngüler, istisnalar, kütüphaneler, testler, dosyalar, düzenli
ifadeler ve sınıflar gördük; bunlarla pek çok problemi çözebilirsin. Bu hafta
tek bir büyük konu yok: daha önceki başlıkların hiçbirine tam oturmayan ama
kodu daha kısa, daha okunur ve daha sağlam yapan küçük araçlar var. İngilizce
adı "Et Cetera", yani "ve benzerleri".

## Küme

Birkaç Hogwarts öğrencisinden hangi binaların geçtiğini, her biri bir kez
olacak şekilde yazdıralım, `houses.py`. Bildiğimiz yol: boş bir liste,
listede yoksa ekle.

```python
students = [
    {"name": "Hermione", "house": "Gryffindor"},
    {"name": "Harry", "house": "Gryffindor"},
    {"name": "Ron", "house": "Gryffindor"},
    {"name": "Draco", "house": "Slytherin"},
    {"name": "Padma", "house": "Ravenclaw"},
]

houses = []
for student in students:
    if student["house"] not in houses:
        houses.append(student["house"])

for house in sorted(houses):
    print(house)
```

```text
$ python houses.py
Gryffindor
Ravenclaw
Slytherin
```

Çalışıyor, ama "zaten var mı" denetimini kendimiz yazdık. Python'da bunu
kendisi yapan bir veri türü var: **küme** (set). Kümede bir değer en fazla
bir kez bulunur; aynı değeri ikinci kez eklemek hiçbir şeyi değiştirmez.

```python
students = [
    {"name": "Hermione", "house": "Gryffindor"},
    {"name": "Harry", "house": "Gryffindor"},
    {"name": "Ron", "house": "Gryffindor"},
    {"name": "Draco", "house": "Slytherin"},
    {"name": "Padma", "house": "Ravenclaw"},
]

houses = set()
for student in students:
    houses.add(student["house"])

for house in sorted(houses):
    print(house)
```

```text
$ python houses.py
Gryffindor
Ravenclaw
Slytherin
```

- Boş küme `set()` ile kurulur, ekleme `add` ile yapılır (listedeki
  `append` gibi, ama "sona" diye bir yer yok).
- Kümenin sırası yok. Çıktıyı abece sırasıyla istediğimiz için `sorted`
  kullandık.

Birkaç küçük ayrıntı:

```python
houses = {"Gryffindor", "Slytherin"}
houses.add("Gryffindor")
print(len(houses))
print("Ravenclaw" in houses)
print(set() == {})
print(type({}))
```

```text
$ python houses.py
2
False
False
<class 'dict'>
```

Değerleri olan küme süslü parantezle yazılabilir: `{"Gryffindor",
"Slytherin"}`. Ama **boş** süslü parantez `{}` küme değil, boş bir
sözlüktür; son iki satır bunu gösteriyor. `in` kümede çok hızlıdır: bir
değerin içinde olup olmadığını sormak, uzun bir listede baştan sona aramaya
göre neredeyse anında biter.

## Genel değişkenler

Bir banka hesabı, `bank.py`. Bakiye dosyanın en üstünde, her fonksiyonun
dışında tanımlanmış bir **genel değişken** (global variable). Fonksiyonun
içinden onu okumak sorun değil:

```python
balance = 0


def main():
    print("Balance:", balance)


if __name__ == "__main__":
    main()
```

```text
$ python bank.py
Balance: 0
```

Şimdi para yatıran ve çeken iki fonksiyon ekleyelim:

```python
balance = 0

def main():
    print("Balance:", balance)
    deposit(100)
    withdraw(50)
    print("Balance:", balance)


def deposit(n):
    balance += n


def withdraw(n):
    balance -= n


if __name__ == "__main__":
    main()
```

```text
$ python bank.py
Balance: 0
Traceback (most recent call last):
  File "bank.py", line 19, in <module>
    main()
    ~~~~^^
  File "bank.py", line 5, in main
    deposit(100)
    ~~~~~~~^^^^^
  File "bank.py", line 11, in deposit
    balance += n
    ^^^^^^^
UnboundLocalError: cannot access local variable 'balance' where it is not
associated with a value
```

Python bir fonksiyonun içinde bir **ada değer atandığını** görünce o adı o
fonksiyonun **yerel değişkeni** sayar. `balance += n`, `balance = balance + n`
demek; yani `deposit`'in kendi `balance`'ı var ve ona henüz bir değer
verilmedi. Hata da tam bunu söylüyor: yerel değişkene, değeri olmadan
ulaşılamaz.

Fonksiyona "bu ad, dosyanın en üstündeki değişken" demenin yolu `global`
anahtar kelimesi:

```python
balance = 0

def main():
    print("Balance:", balance)
    deposit(100)
    withdraw(50)
    print("Balance:", balance)


def deposit(n):
    global balance
    balance += n


def withdraw(n):
    global balance
    balance -= n


if __name__ == "__main__":
    main()
```

```text
$ python bank.py
Balance: 0
Balance: 50
```

`global` çalışır, ama dikkatli kullanılır: genel değişkeni değiştiren
fonksiyon sayısı arttıkça kimin neyi ne zaman değiştirdiğini izlemek
zorlaşır. Geçen haftaki nesne yönelimli programlama burada daha derli toplu
bir çözüm veriyor: bakiyeyi bir nesnenin içine koymak.

```python
class Account:
    def __init__(self):
        self._balance = 0

    @property
    def balance(self):
        return self._balance

    def deposit(self, n):
        self._balance += n

    def withdraw(self, n):
        self._balance -= n


def main():
    account = Account()
    print("Balance:", account.balance)
    account.deposit(100)
    account.withdraw(50)
    print("Balance:", account.balance)


if __name__ == "__main__":
    main()
```

```text
$ python bank.py
Balance: 0
Balance: 50
```

Bakiye artık `self._balance`'ta; ona her metot `self` üzerinden ulaşıyor,
`global` gerekmiyor. `balance` bir özellik (`@property`), ayarlayıcısı yok:
dışarıdan okunabiliyor ama yalnızca `deposit` ve `withdraw` değiştiriyor.

## Sabitler

Kodun içine gömülmüş `3` gibi bir sayıya **sihirli sayı** (magic number)
denir: neyi temsil ettiği belli değil, değişmesi gerekince yerini bulmak
zor. Onu dosyanın başına, adı olan bir değişkene çıkarmak iyi bir alışkanlık.
Değişmemesi gereken değişkenlerin adı geleneksel olarak **büyük harfle**
yazılır; bunlara **sabit** (constant) denir.

```python
MEOWS = 3

for _ in range(MEOWS):
    print("meow")
```

```text
$ python meows.py
meow
meow
meow
```

Ama Python sabitleri korumaz. Büyük harf yalnızca okuyana "buna dokunma"
diyen bir gelenek; aşağıdaki kod hiçbir uyarı vermeden dört kez miyavlıyor.
Başka bazı dillerde böyle bir satır hata verirdi.

```python
MEOWS = 3
MEOWS = 4

for _ in range(MEOWS):
    print("meow")
```

```text
$ python meows.py
meow
meow
meow
meow
```

Sınıfın içinde de sabit olabilir: sınıf değişkeni, büyük harfle. Ona sınıfın
adıyla ulaşılır, `Cat.MEOWS`:

```python
class Cat:
    MEOWS = 3

    def meow(self):
        for _ in range(Cat.MEOWS):
            print("meow")


cat = Cat()
cat.meow()
```

```text
$ python meows.py
meow
meow
meow
```

## Tip belirtimleri

Python **dinamik tipli** (dynamically typed) bir dil: bir değişkenin türünü
yazmazsın, Python ona verilen değerden anlar. Bazı diller ise türün açıkça
yazılmasını ister; bunun artısı, yanlış türü kullandığında hatanın program
çalışmadan yakalanması. Python'da da bir değerin hangi türde olması
gerektiğini yazabilirsin: **tip belirtimi** (type hint).

```python
def meow(n: int):
    for _ in range(n):
        print("meow")


number: int = input("Number: ")
meow(number)
```

```text
$ python meows.py
Number: 3
Traceback (most recent call last):
  File "meows.py", line 7, in <module>
    meow(number)
    ~~~~^^^^^^^^
  File "meows.py", line 2, in meow
    for _ in range(n):
             ~~~~~^^^
TypeError: 'str' object cannot be interpreted as an integer
```

- `n: int`, `meow`'un `n` parametresinin bir int olması beklendiğini
  söyler.
- `number: int = ...` aynı notu bir değişkene düşer.

Ama program yine aynı `TypeError` ile düştü: `input` dize döndürüyor ve
Python belirtimlere **bakmıyor**. Belirtimi okuyup denetleyen ayrı bir
program gerekiyor; en bilineni **mypy** (`pip install mypy`, sonra
`mypy meows.py`). mypy programı çalıştırmaz, yalnızca okur. Bu kodda
`number: int = input(...)` satırında durur: `input`'un döndürdüğü `str`,
`int` diye belirtilmiş bir değişkene atanıyor. Yani hata, kullanıcı programı
çalıştırmadan önce, kodu yazan kişiye gösterilir. Odyssey mypy'yi
çalıştırmıyor; burada yalnızca ne yaptığını anlatıyoruz.

Python'un belirtimleri yalnızca sakladığını görmek için:

```python
def double(n: int) -> int:
    return n * 2


print(double.__annotations__)
print(double(21))
print(double("ha"))
```

```text
$ python meows.py
{'n': <class 'int'>, 'return': <class 'int'>}
42
haha
```

Belirtim `__annotations__`'ta duruyor, ama `double("ha")` hiçbir uyarı
olmadan `haha` döndürdü. Belirtim bir not; zorunluluk değil.

Dönüş değerinin türü `->` ile yazılır. Şu kodda bir yanlış var:

```python
def meow(n: int):
    for _ in range(n):
        print("meow")


number: int = int(input("Number: "))
meows: str = meow(number)
print(meows)
```

```text
$ python meows.py
Number: 3
meow
meow
meow
None
```

`meow` yazdırıyor ama hiçbir şey **döndürmüyor**. `return` olmayan bir
fonksiyon `None` döndürür; son satır o yüzden `None` yazdı. `def meow(n: int)
-> None:` yazsaydık mypy `meows: str = meow(number)` satırında "bu fonksiyon
değer döndürmüyor" diye uyarırdı. Düzeltmesi, `meow`'un dizeyi yazdırmak
yerine döndürmesi:

```python
def meow(n: int) -> str:
    return "meow\n" * n


number: int = int(input("Number: "))
meows: str = meow(number)
print(meows, end="")
```

```text
$ python meows.py
Number: 3
meow
meow
meow
```

- `-> str`: `meow` bir dize döndürür.
- `"meow\n" * n`: dize ile tam sayının çarpımı dizeyi o kadar kez yan yana
  koyar; döngü gerekmiyor.
- Dize zaten satır sonuyla bittiği için `print`'e `end=""` verdik; yoksa
  sonda boş bir satır kalırdı.

Döndüren fonksiyon birim testi için de daha uygun: `assert meow(3) ==
"meow\nmeow\nmeow\n"` yazılabilir.

## Belge dizeleri

Bir fonksiyonun ne yaptığını `#` ile üstüne yazmak yerine Python'un bir
standardı var (PEP 257): fonksiyonun gövdesinin **ilk satırına**, üçlü
tırnak içinde yazılan **belge dizesi** (docstring).

```python
def meow(n: int) -> str:
    """
    Meow n times.

    :param n: Number of times to meow
    :type n: int
    :raise TypeError: If n is not an int
    :return: A string of n meows, one per line
    :rtype: str
    """
    return "meow\n" * n


print(meow.__doc__.splitlines()[1].strip())
```

```text
$ python meows.py
Meow n times.
```

Python belge dizesini `meow.__doc__`'ta saklıyor; belge üreten araçlar
kodu okuyup bunlardan web sayfası ya da PDF hazırlayabiliyor. İçindeki
`:param n:`, `:type n:`, `:raise TypeError:`, `:return:`, `:rtype:`
satırları Python'un değil, **reStructuredText** denen bir yazım biçiminin
geleneği; bazı popüler belgeleme araçları bu biçimi tanıyor.

## Komut satırı argümanları: argparse

`meows.py`'ın kaç kez miyavlayacağını kullanıcıya sormak yerine komut
satırından alalım: `python meows.py -n 3`. Komut satırı programlarında
böyle `-n` gibi seçeneklere **anahtar** (switch) ya da **bayrak** (flag)
denir. Kütüphaneler haftasındaki `sys.argv` ile:

```python
import sys

if len(sys.argv) == 1:
    print("meow")
elif len(sys.argv) == 3 and sys.argv[1] == "-n":
    n = int(sys.argv[2])
    for _ in range(n):
        print("meow")
else:
    print("usage: meows.py [-n NUMBER]")
```

```text
$ python meows.py
meow
```

```text
$ python meows.py -n 3
meow
meow
meow
```

```text
$ python meows.py 3
usage: meows.py [-n NUMBER]
```

Çalışıyor, ama seçenekler çoğaldıkça (`-n`, `-a`, `-b`... hem de her
sırada) bu `if` zinciri çok çabuk içinden çıkılmaz hâle gelir. Python'un
kendi kütüphanesinde bu işi yapan bir modül var: **argparse** (argument
parser, argüman ayrıştırıcı).

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n")
args = parser.parse_args()

for _ in range(int(args.n)):
    print("meow")
```

```text
$ python meows.py -n 3
meow
meow
meow
```

- `argparse.ArgumentParser()` bir ayrıştırıcı nesnesi kurar.
- `add_argument("-n")` hangi seçeneği tanıyacağını söyler.
- `parse_args()` `sys.argv`'yi kendisi okur ve seçenekleri, hangi sırada
  gelirse gelsin, `args` nesnesine koyar: `args.n`.

Ama `-n` verilmezse `args.n` `None` olur:

```text
$ python meows.py
Traceback (most recent call last):
  File "meows.py", line 7, in <module>
    for _ in range(int(args.n)):
                   ~~~^^^^^^^^
TypeError: int() argument must be a string, a bytes-like object or a real
number, not 'NoneType'
```

`add_argument`'ın birkaç adlandırılmış argümanı bunu ve daha fazlasını
çözüyor:

```python
import argparse

parser = argparse.ArgumentParser(description="Meow like a cat")
parser.add_argument("-n", default=1, help="number of times to meow", type=int)
args = parser.parse_args()

for _ in range(args.n):
    print("meow")
```

```text
$ python meows.py
meow
```

```text
$ python meows.py -n 2
meow
meow
```

- `default=1`: seçenek verilmezse değer.
- `type=int`: değeri tam sayıya argparse çevirir; `int(...)` yazmaya gerek
  yok.
- `description` ve `help`: kullanım bilgisinde görünen açıklamalar.

Komut satırı programlarında `-h` ya da `--help` neredeyse her zaman
kullanım bilgisini yazar; argparse bunu kendiliğinden ekliyor:

```text
$ python meows.py -h
usage: meows.py [-h] [-n N]

Meow like a cat

options:
  -h, --help  show this help message and exit
  -n N        number of times to meow
```

Köşeli parantez belgelerde "isteğe bağlı" demek: `-h` ya da `-n N`
yazmak zorunda değilsin. Kullanıcı geçersiz bir değer verirse argparse
kullanımı ve sorunu yazıp programı bitiriyor:

```text
$ python meows.py -n dog
usage: meows.py [-h] [-n N]
meows.py: error: argument -n: invalid int value: 'dog'
```

## Açmak: tek ve çift yıldız

Bir değeri birden çok değişkene **açmayı** (unpacking) daha önce gördük:

```python
first, _ = input("What's your name? ").split(" ")
print(f"hello, {first}")
```

```text
$ python unpack.py
What's your name? David Malan
hello, David
```

`split` iki öğeli bir liste döndürüyor ve virgül onu iki değişkene açıyor.
Soyadını kullanmadığımız için ona `_` adını verdik. Açmanın fonksiyon
çağırırken de işe yarayan iki biçimi var. Harry Potter dünyasında bir
Galleon 17 Sickle, bir Sickle 29 Knut ediyor; bir kasanın değerini Knut
olarak hesaplayan bir fonksiyon, `unpack.py`:

```python
def total(galleons, sickles, knuts):
    return (galleons * 17 + sickles) * 29 + knuts


print(total(100, 50, 25), "Knuts")
```

```text
$ python unpack.py
50775 Knuts
```

Sikkeler bir listede duruyorsa, öğeleri tek tek vermek uzun ve hataya açık:

```python
def total(galleons, sickles, knuts):
    return (galleons * 17 + sickles) * 29 + knuts


coins = [100, 50, 25]
print(total(coins[0], coins[1], coins[2]), "Knuts")
```

Listeyi olduğu gibi vermek ise işe yaramaz; `galleons` listenin kendisi
olur, öteki ikisi boş kalır:

```python
def total(galleons, sickles, knuts):
    return (galleons * 17 + sickles) * 29 + knuts


coins = [100, 50, 25]
print(total(coins), "Knuts")
```

```text
$ python unpack.py
Traceback (most recent call last):
  File "unpack.py", line 6, in <module>
    print(total(coins), "Knuts")
          ~~~~~^^^^^^^
TypeError: total() missing 2 required positional arguments: 'sickles' and 'knuts'
```

Listenin önüne konan **tek yıldız** onu açar: `total(*coins)`,
`total(100, 50, 25)` yazmakla aynı.

```python
def total(galleons, sickles, knuts):
    return (galleons * 17 + sickles) * 29 + knuts


coins = [100, 50, 25]
print(total(*coins), "Knuts")
```

```text
$ python unpack.py
50775 Knuts
```

Öğe sayısı parametre sayısını tutmalı; dört öğeli bir listeyi açmak
`TypeError: total() takes 3 positional arguments but 4 were given` verir.

Argümanları adlarıyla da verebiliriz; o zaman sıra önemli değil:

```python
def total(galleons, sickles, knuts):
    return (galleons * 17 + sickles) * 29 + knuts


print(total(galleons=100, sickles=50, knuts=25), "Knuts")
```

Ad ve değer çiftleri bir sözlüğü hatırlatıyor. Sözlüğün önüne konan **çift
yıldız** onu `anahtar=değer` argümanlarına açar:

```python
def total(galleons, sickles, knuts):
    return (galleons * 17 + sickles) * 29 + knuts


coins = {"galleons": 100, "sickles": 50, "knuts": 25}
print(total(**coins), "Knuts")
```

```text
$ python unpack.py
50775 Knuts
```

`total(**coins)` tam olarak `total(galleons=100, sickles=50, knuts=25)`
demek. Sözlükte fonksiyonun tanımadığı bir anahtar varsa hata verir:

```text
$ python unpack.py
Traceback (most recent call last):
  File "unpack.py", line 6, in <module>
    print(total(**coins), "Knuts")
          ~~~~~^^^^^^^^^
TypeError: total() got an unexpected keyword argument 'pennies'
```

## Değişken sayıda argüman: args ve kwargs

Yıldızlar fonksiyon **tanımlarken** de kullanılır, bu kez tersine: dağınık
argümanları toplamak için. Böyle istenen sayıda argüman alan fonksiyona
**değişken sayıda argümanlı** (variadic) fonksiyon denir.

```python
def f(*args, **kwargs):
    print("Positional:", args)
    print("Named:", kwargs)


f(100, 50, 25)
f(galleons=100, sickles=50, knuts=25)
f(5)
```

```text
$ python unpack.py
Positional: (100, 50, 25)
Named: {}
Positional: ()
Named: {'galleons': 100, 'sickles': 50, 'knuts': 25}
Positional: (5,)
Named: {}
```

- `*args` bütün konumsal argümanları bir **demette** toplar.
- `**kwargs` bütün adlandırılmış argümanları (keyword arguments) bir
  **sözlükte** toplar.
- `args` ve `kwargs` yalnızca gelenek; önemli olan yıldızlar.
- `(5,)` tek öğeli bir demet: sondaki virgül onu düz bir sayıdan ayırıyor.

Haftalardır kullandığımız `print` de böyle bir fonksiyon. Belgesindeki
imzası `print(*objects, sep=' ', end='\n', ...)`: `print()`,
`print("hello")` ve `print("hello", "world")` bu yüzden hepsi geçerli.

## map

Kendisine verilen kelimeleri büyük harfle "bağıran" bir program, `yell.py`.
Önce bir liste alsın:

```python
def main():
    yell(["This", "is", "CS50"])


def yell(words):
    uppercased = []
    for word in words:
        uppercased.append(word.upper())
    print(uppercased)


if __name__ == "__main__":
    main()
```

```text
$ python yell.py
['THIS', 'IS', 'CS50']
```

Liste olduğu gibi, köşeli parantez ve tırnaklarıyla yazıldı. Açmak burada da
işe yarıyor: `print(*uppercased)`, öğeleri `print`'e ayrı argümanlar olarak
veriyor.

```text
$ python yell.py
THIS IS CS50
```

`yell`'i bir liste yerine, `print` gibi istenen sayıda argümanla çağırmak
daha doğal; `*words` ile:

```python
def main():
    yell("This", "is", "CS50")


def yell(*words):
    uppercased = []
    for word in words:
        uppercased.append(word.upper())
    print(*uppercased)


if __name__ == "__main__":
    main()
```

```text
$ python yell.py
THIS IS CS50
```

Döngüyü ve `append`'i Python'un hazır bir fonksiyonu kaldırıyor: **map**.
`map(fonksiyon, dizi)` verilen fonksiyonu dizinin her öğesine uygular
(eşler).

```python
def main():
    yell("This", "is", "CS50")


def yell(*words):
    uppercased = map(str.upper, words)
    print(*uppercased)


if __name__ == "__main__":
    main()
```

```text
$ python yell.py
THIS IS CS50
```

`str.upper`'dan sonra parantez yok: fonksiyonu **çağırmıyoruz**, `map`'e
**veriyoruz**; her kelimede `map` çağırıyor. Bir fonksiyonu başka bir
fonksiyona değer gibi vermek **fonksiyonel programlamanın** (functional
programming) bir özelliği; Dosya İşlemleri haftasındaki `sorted(...,
key=...)` da böyleydi.

`map` bir liste değil, sonuçları istendikçe hesaplayan bir `map` nesnesi
döndürür ve bir kez tüketilir:

```python
words = ["This", "is", "CS50"]
uppercased = map(str.upper, words)
print(uppercased)
print(list(uppercased))
print(list(uppercased))
```

```text
$ python yell.py
<map object at 0x...>
['THIS', 'IS', 'CS50']
[]
```

Liste gerekiyorsa `list(map(...))`.

## Liste kavraması

Aynı işin Python'a özgü (Pythonic) sayılan, çok yaygın bir yazımı daha var:
**liste kavraması** (list comprehension). Köşeli parantezin içinde, döngü
yazmadan, bir listenin nasıl kurulacağını tek satırda söylersin:

```python
def main():
    yell("This", "is", "CS50")


def yell(*words):
    uppercased = [word.upper() for word in words]
    print(*uppercased)


if __name__ == "__main__":
    main()
```

```text
$ python yell.py
THIS IS CS50
```

Soldan sağa okunuyor: "`words`'teki her `word` için `word.upper()`".
Kavramanın sonuna bir koşul da eklenebilir. Gryffindor öğrencilerinin
adları, `gryffindors.py`:

```python
students = [
    {"name": "Hermione", "house": "Gryffindor"},
    {"name": "Harry", "house": "Gryffindor"},
    {"name": "Ron", "house": "Gryffindor"},
    {"name": "Draco", "house": "Slytherin"},
]

gryffindors = [
    student["name"] for student in students if student["house"] == "Gryffindor"
]

for gryffindor in sorted(gryffindors):
    print(gryffindor)
```

```text
$ python gryffindors.py
Harry
Hermione
Ron
```

`if` kısmı yalnızca koşulu tutan öğeleri listeye alır. Satır uzayınca köşeli
parantezleri ayrı satırlara taşıdık; okuması kolaylaşıyor.

## filter

Aynı süzmenin fonksiyonel yolu **filter**: `filter(fonksiyon, dizi)`
fonksiyonu her öğede çağırır ve yalnızca `True` döndürdüğü öğeleri bırakır.
`map` her öğeyi **dönüştürür**, `filter` bazılarını **eler**.

```python
students = [
    {"name": "Hermione", "house": "Gryffindor"},
    {"name": "Harry", "house": "Gryffindor"},
    {"name": "Ron", "house": "Gryffindor"},
    {"name": "Draco", "house": "Slytherin"},
]


def is_gryffindor(s):
    return s["house"] == "Gryffindor"


gryffindors = filter(is_gryffindor, students)

for gryffindor in gryffindors:
    print(gryffindor["name"])
```

```text
$ python gryffindors.py
Hermione
Harry
Ron
```

`is_gryffindor` yalnızca burada kullanılıyor; ona ad vermek yerine adsız bir
`lambda` fonksiyonu yazabiliriz. Sıralamak için de Dosya İşlemleri
haftasındaki `sorted(..., key=lambda ...)`:

```python
students = [
    {"name": "Hermione", "house": "Gryffindor"},
    {"name": "Harry", "house": "Gryffindor"},
    {"name": "Ron", "house": "Gryffindor"},
    {"name": "Draco", "house": "Slytherin"},
]

gryffindors = filter(lambda s: s["house"] == "Gryffindor", students)

for gryffindor in sorted(gryffindors, key=lambda s: s["name"]):
    print(gryffindor["name"])
```

```text
$ python gryffindors.py
Harry
Hermione
Ron
```

## Sözlük kavraması

Bu kez yalnızca adlar elimizde ve her öğrenci için bir sözlük kurmak
istiyoruz. Döngüyle:

```python
students = ["Hermione", "Harry", "Ron"]

gryffindors = []
for student in students:
    gryffindors.append({"name": student, "house": "Gryffindor"})

for gryffindor in gryffindors:
    print(gryffindor)
```

```text
$ python gryffindors.py
{'name': 'Hermione', 'house': 'Gryffindor'}
{'name': 'Harry', 'house': 'Gryffindor'}
{'name': 'Ron', 'house': 'Gryffindor'}
```

Liste kavramasıyla aynı liste tek satırda:

```python
students = ["Hermione", "Harry", "Ron"]

gryffindors = [{"name": student, "house": "Gryffindor"} for student in students]

for gryffindor in gryffindors:
    print(gryffindor)
```

Ama belki sözlüklerden oluşan bir listeye gerek yok: anahtarı öğrencinin adı,
değeri binası olan **tek** bir sözlük yeter. Bunu kuran yazım **sözlük
kavraması** (dictionary comprehension): köşeli değil süslü parantez,
içinde `anahtar: değer`.

```python
students = ["Hermione", "Harry", "Ron"]

gryffindors = {student: "Gryffindor" for student in students}

print(gryffindors)
```

```text
$ python gryffindors.py
{'Hermione': 'Gryffindor', 'Harry': 'Gryffindor', 'Ron': 'Gryffindor'}
```

## enumerate

Öğrencileri sıra numarasıyla yazdıralım. `range` ve `len` ile:

```python
students = ["Hermione", "Harry", "Ron"]

for i in range(len(students)):
    print(i + 1, students[i])
```

```text
$ python gryffindors.py
1 Hermione
2 Harry
3 Ron
```

İnsanlar sıfırdan saymadığı için `i + 1` yazdık. **enumerate** bir dizinin
üzerinden geçerken her turda iki şey verir: o anki sıra (sıfırdan) ve o
sıradaki öğe. `range`, `len` ve `students[i]` gerekmiyor:

```python
students = ["Hermione", "Harry", "Ron"]

for i, student in enumerate(students):
    print(i + 1, student)
```

```text
$ python gryffindors.py
1 Hermione
2 Harry
3 Ron
```

Saymaya bir'den başlamak istersen `enumerate(students, start=1)`.

## Üreteçler ve yield

Uyuyamayınca koyun saymak, `sleep.py`. Her satırda bir koyun fazla:

```python
n = int(input("What's n? "))
for i in range(n):
    print("🐑" * i)
```

```text
$ python sleep.py
What's n? 3

🐑
🐑🐑
```

Öğrendiklerimizi uygulayıp koyunları üreten kısmı ayrı bir fonksiyona
alalım; yazdırmak yerine bütün sürüyü bir listede döndürsün, test edilebilir
olsun:

```python
def main():
    n = int(input("What's n? "))
    for s in sheep(n):
        print(s)


def sheep(n):
    flock = []
    for i in range(n):
        flock.append("🐑" * i)
    return flock


if __name__ == "__main__":
    main()
```

```text
$ python sleep.py
What's n? 3

🐑
🐑🐑
```

Derste David Malan bunu 10 000 koyunla sorunsuz çalıştırıyor; bir milyonda
ise program hiçbir şey yazmadan bekliyor ve sonunda işletim sistemi onu
**öldürüyor** (killed). `sheep` bir milyon satırın hepsini **bir kerede**
belleğe kurmaya çalışıyor ve bellek yetmiyor. Bu bilgisayarda 2000 koyunla
tepe belleği ölçtük:

```python
import tracemalloc


def sheep_list(n):
    flock = []
    for i in range(n):
        flock.append("🐑" * i)
    return flock


def sheep_gen(n):
    for i in range(n):
        yield "🐑" * i


for f in (sheep_list, sheep_gen):
    tracemalloc.start()
    for s in f(2000):
        pass
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    print(f.__name__, round(peak / 1_000_000, 1), "MB")
```

```text
$ python sleep.py
sheep_list 8.1 MB
sheep_gen 0.0 MB
```

Liste 2000 koyunda bile megabaytlarca yer tutuyor ve satır sayısıyla
birlikte hızla büyüyor. Çözüm, `sheep`'i bir **üretece** (generator)
çevirmek: `return` yerine `yield`.

```python
def main():
    n = int(input("What's n? "))
    for s in sheep(n):
        print(s)


def sheep(n):
    for i in range(n):
        yield "🐑" * i


if __name__ == "__main__":
    main()
```

```text
$ python sleep.py
What's n? 3

🐑
🐑🐑
```

`yield` bir değer verir ama fonksiyonu bitirmez; fonksiyon o noktada
**durur** ve kaldığı yeri hatırlar. `main`'deki döngü bir sonraki değeri
istediğinde kaldığı yerden devam eder. Yani bellekte her an yalnızca bir sıra
koyun var; bir milyonda da çıktı hemen başlıyor. Yukarıdaki ölçümde üretecin
tepe belleği bu yüzden neredeyse sıfır.

Üreteç fonksiyonu çağırınca gövde hemen çalışmaz, bir **üreteç nesnesi**
döner. Döngü değerleri ondan `next` ile birer birer ister; değer kalmayınca
`StopIteration` gelir ve `for` bunu "bitti" diye anlar:

```python
def sheep(n):
    for i in range(n):
        yield "🐑" * i


flock = sheep(3)
print(flock)
print(repr(next(flock)))
print(next(flock))
print(next(flock))
print(next(flock))
```

```text
$ python sleep.py
<generator object sheep at 0x...>
''
🐑
🐑🐑
Traceback (most recent call last):
  File "sleep.py", line 11, in <module>
    print(next(flock))
          ~~~~^^^^^^^
StopIteration
```

Değerleri birer birer veren bu tür nesnelere **yineleyici** (iterator) denir.

## Bitirirken

Videonun sonunda David Malan dersi, yazdığını sesli okuyan bir metinden sese
kütüphanesiyle (pyttsx3) ve `cowsay` ile bitiriyor. pyttsx3 Odyssey'de
kurulu değil; o programı burada çalıştırmıyoruz.

Bu haftanın araçlarının hiçbiri şart değil; hepsiyle yapılan işi önceki
haftaların araçlarıyla da yapabilirsin. Ama başkalarının kodunda sık
karşına çıkacaklar ve aynı problemleri daha kısa, daha okunur çözmeni
sağlıyorlar.

## Özet

- Küme: `set()`, `add`, her değer bir kez; boş `{}` sözlük
- Genel değişkeni değiştirmek için `global`; çoğu zaman sınıf daha derli toplu
- Sabitler büyük harfle; Python korumaz
- Tip belirtimleri `n: int`, `-> str`; Python denetlemez, mypy denetler
- Belge dizesi: gövdenin ilk satırında `"""..."""`
- argparse: `add_argument("-n", default=1, type=int, help=...)`, `-h`
- Açmak: `f(*liste)`, `f(**sözlük)`; toplamak: `def f(*args, **kwargs)`
- `map` dönüştürür, `filter` eler; liste ve sözlük kavramaları
- `enumerate`: sıra ve öğe birlikte
- Üreteç: `yield` değerleri birer birer verir, bütün veriyi bellekte tutmaz

---

*Bu bölüm, Harvard Üniversitesi'nin [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) dersinin 9. haftasının ders notundan çevrilip uyarlanmıştır; örnekler ve alıştırmalar değiştirildi. Özgün içerik ve bu uyarlama [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) lisanslıdır. Harvard bu uyarlamayı onaylamış değildir.*
