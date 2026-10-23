Döngülü programlarda en sık karşılaşılan hatalar ve mesajları (Python
3.14'te ölçüldü). Hata mesajının **son satırı** önce okunur.

## Listenin sonunu aşmak

```python
students = ["Hermione", "Harry", "Ron"]
print(students[3])
```

```text
$ python hogwarts.py
Traceback (most recent call last):
  File "hogwarts.py", line 2, in <module>
    print(students[3])
          ~~~~~~~~^^^
IndexError: list index out of range
```

Üç elemanlı listenin konumları 0, 1, 2. Son elemana ulaşmanın güvenli yolu
`len(students) - 1` ya da doğrudan `for student in students:`.

## Sözlükte olmayan anahtar

```python
students = {
    "Hermione": "Gryffindor",
    "Harry": "Gryffindor",
    "Ron": "Gryffindor",
    "Draco": "Slytherin",
}
print(students["Luna"])
```

```text
$ python hogwarts.py
Traceback (most recent call last):
  File "hogwarts.py", line 7, in <module>
    print(students["Luna"])
          ~~~~~~~~^^^^^^^^
KeyError: 'Luna'
```

Sözlükte yalnızca tanımladığın anahtarlar var. Anahtarın yazımı da birebir
tutmalı: `"harry"` ile `"Harry"` farklı anahtarlar.

## range'e metin vermek

```python
n = input("What's n? ")
for _ in range(n):
    print("meow")
```

```text
$ python cat.py
What's n? 3
Traceback (most recent call last):
  File "cat.py", line 2, in <module>
    for _ in range(n):
             ~~~~~^^^
TypeError: 'str' object cannot be interpreted as an integer
```

`input` metin döndürür, `range` tam sayı ister: `n = int(input(...))`.

## Döngü satırında `:` yok

```python
for _ in range(3)
    print("meow")
```

```text
$ python cat.py
  File "cat.py", line 1
    for _ in range(3)
                     ^
SyntaxError: expected ':'
```

`for` ve `while` satırları da `if` gibi `:` ile biter.

## Hata vermeyen yanlışlar

Bunlar mesaj üretmez; program çalışır ama istediğini yapmaz.

| Yazdığın | Ne olur | Yerine |
|---|---|---|
| `while` gövdesinde `i += 1` yok | program durmaz (`Ctrl+C`) | koşulu değiştiren satırı ekle |
| `while i <= 3` ve `i = 0` | dört kez döner | `i < 3` ya da `i = 1` |
| `range(n)` ile 1'den `n`'e saymak | 0'dan `n - 1`'e sayar | `range(1, n + 1)` |
| `print("#")` iç döngüde | her tuğla ayrı satırda | `print("#", end="")` |
| boş `print()` iç döngünün içinde | her tuğladan sonra satır biter | `print()` dış döngüde |
| `for student in students:` sözlükte, `print(student)` | yalnızca anahtarlar yazılır | değer için `students[student]` |
| `total = 0` döngünün içinde | toplam her turda sıfırlanır | sayacı döngüden **önce** başlat |
