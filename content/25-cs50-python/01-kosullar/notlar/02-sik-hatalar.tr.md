Koşullu programlarda en sık karşılaşılan hatalar ve mesajları (Python 3.14'te
ölçüldü). Hata mesajının **son satırı** önce okunur.

## Karşılaştırmada tek `=`

```python
x = int(input("What's x? "))
if x = 1:
    print("one")
```

```text
$ python compare.py
  File "compare.py", line 2
    if x = 1:
       ^^^^^
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```

Tek `=` atama, karşılaştırma `==`. Python burada ne demek istediğini tahmin
edip söylüyor.

## Koşulun sonunda `:` yok

```python
x = int(input("What's x? "))
if x == 1
    print("one")
```

```text
$ python compare.py
  File "compare.py", line 2
    if x == 1
             ^
SyntaxError: expected ':'
```

`if`, `elif`, `else`, `match` ve `case` satırlarının hepsi `:` ile biter.

## `else if` yazmak

```python
x = int(input("What's x? "))
if x == 1:
    print("one")
else if x == 2:
    print("two")
```

```text
$ python compare.py
  File "compare.py", line 4
    else if x == 2:
         ^^
SyntaxError: expected ':'
```

Başka dillerdeki `else if` Python'da `elif`. Python `else`'ten hemen sonra `:`
bekliyor, o yüzden mesaj eksik iki nokta diyor.

## Metinle sayıyı karşılaştırmak

```python
x = input("What's x? ")
if x > 3:
    print("big")
```

```text
$ python compare.py
What's x? 5
Traceback (most recent call last):
  File "compare.py", line 2, in <module>
    if x > 3:
       ^^^^^
TypeError: '>' not supported between instances of 'str' and 'int'
```

`input` metin döndürür; `>` ve `<` metinle sayıyı karşılaştıramaz. Önce
çevir: `x = int(input(...))`. Dikkat: `==` hata vermez, yalnızca hep `False`
olur (`"5" == 5` → `False`).

## Hata vermeyen yanlışlar

Bunlar mesaj üretmez; program çalışır ama istediğini yapmaz.

```python
name = input("What's your name? ")

# Yanlış: "Hermione" tek başına her zaman doğru sayılır
if name == "Harry" or "Hermione":
    print("Gryffindor")
else:
    print("Who?")
```

```text
$ python house.py
What's your name? Draco
Gryffindor
```

| Yazdığın | Ne olur | Yerine |
|---|---|---|
| `name == "Harry" or "Ron"` | her isim doğru sayılır | `name == "Harry" or name == "Ron"` |
| üç ayrı `if` | koşullar birbirini dışlamıyorsa birden çok blok çalışır | `if` / `elif` / `else` |
| önce `if score >= 80`, sonra `elif score >= 90` | 95 alan `B` olur | büyükten küçüğe sırala |
| `case _:` en üstte | altındaki durumlara hiç gelinmez | `case _:` en sona |
| `"7:30" < "10:00"` | metinler harf harf karşılaştırılır: `False` | önce sayıya çevir |
