Bu haftanın araçlarıyla en sık yapılan hatalar ve mesajları (Python 3.14'te,
bu bilgisayarda ölçüldü). Hata mesajının **son satırı** önce okunur.

## Boş küme diye {} yazmak

Süslü parantez hem kümede hem sözlükte kullanılıyor; **boş** süslü parantez
sözlük:

```python
houses = {}
houses.add("Gryffindor")
```

```text
$ python houses.py
Traceback (most recent call last):
  File "houses.py", line 2, in <module>
    houses.add("Gryffindor")
    ^^^^^^^^^^
AttributeError: 'dict' object has no attribute 'add'
```

Boş küme `set()` ile yazılır.

## Kümeye indeksle bakmak

Kümenin sırası olmadığı için "sıfırıncı öğesi" de yok:

```python
houses = {"Gryffindor", "Slytherin"}
print(houses[0])
```

```text
$ python houses.py
Traceback (most recent call last):
  File "houses.py", line 2, in <module>
    print(houses[0])
          ~~~~~~^^^
TypeError: 'set' object is not subscriptable
```

Sırayla gezmek için `for house in sorted(houses):`; belirli bir değeri
aramak için `in`.

## global yazmadan genel değişkeni değiştirmek

Fonksiyonun içinde bir ada atama yapılınca o ad yerel sayılır; okumak
çalışır, `+=` çalışmaz:

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

Ya fonksiyonun başına `global balance` yazılır ya da değer bir nesnede
tutulur (`self._balance`).

## Tip belirtiminin korumasına güvenmek

Belirtim Python'a bir şey yaptırmaz; yanlış türdeki değer yine fonksiyona
girer ve hata fonksiyonun içinde çıkar:

```python
def meow(n: int) -> str:
    return "meow\n" * n


print(meow(2.5))
```

```text
$ python meows.py
Traceback (most recent call last):
  File "meows.py", line 5, in <module>
    print(meow(2.5))
          ~~~~^^^^^
  File "meows.py", line 2, in meow
    return "meow\n" * n
           ~~~~~~~~~^~~
TypeError: can't multiply sequence by non-int of type 'float'
```

Bu hatayı program çalışmadan yakalamak için kodun üzerinde mypy
çalıştırılır; kullanıcıdan gelen değeri yine sen denetlersin.

## map'e çağrılmış fonksiyon vermek

`map`'e fonksiyonun kendisi verilir; parantez onu hemen, argümansız çağırır:

```python
words = ["This", "is", "CS50"]
print(list(map(str.upper(), words)))
```

```text
$ python yell.py
Traceback (most recent call last):
  File "yell.py", line 2, in <module>
    print(list(map(str.upper(), words)))
                   ~~~~~~~~~^^
TypeError: unbound method str.upper() needs an argument
```

Doğrusu `map(str.upper, words)`.

## Üreteci iki kez gezmek

`map`, `filter` ve üreteçler değerleri bir kez verir; ikinci gezişte geriye
bir şey kalmamıştır ve hata da vermez:

```python
def evens(n):
    for i in range(0, n, 2):
        yield i


numbers = evens(7)
print(sum(numbers))
print(sum(numbers))
```

```text
$ python evens.py
12
0
```

Değerler birden çok kez gerekiyorsa bir kez `list(...)` ile listeye al ya da
üreteci yeniden çağır: `sum(evens(7))`.

## Açılan öğe sayısını tutturamamak

`*` listenin her öğesini bir argüman yapar; öğe sayısı parametre sayısından
fazla ya da azsa `TypeError`:

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

Dört öğeli bir listeyle de `TypeError: total() takes 3 positional arguments
but 4 were given`. Sözlükte fonksiyonun tanımadığı bir anahtar olursa
`TypeError: total() got an unexpected keyword argument 'pennies'`.

## Varsayılan değer olarak liste

Varsayılan değer fonksiyon **tanımlanırken bir kez** oluşturulur. Liste gibi
değiştirilebilen bir değer bütün çağrılar arasında paylaşılır:

```python
def add(name, names=[]):
    names.append(name)
    return names


print(add("Harry"))
print(add("Ron"))
```

```text
$ python names.py
['Harry']
['Harry', 'Ron']
```

Varsayılanı `None` yapıp listeyi fonksiyonun içinde kur:

```python
def add(name, names=None):
    if names is None:
        names = []
    names.append(name)
    return names


print(add("Harry"))
print(add("Ron"))
```

```text
$ python names.py
['Harry']
['Ron']
```
