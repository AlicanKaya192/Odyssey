İstisnalarla çalışırken en sık yapılan hatalar ve mesajları (Python 3.14'te
ölçüldü). Hata mesajının **son satırı** önce okunur.

## Yakalanmayan ValueError

```python
x = int(input("What's x? "))
print(f"x is {x}")
```

```text
$ python number.py
What's x? cat
Traceback (most recent call last):
  File "number.py", line 1, in <module>
    x = int(input("What's x? "))
ValueError: invalid literal for int() with base 10: 'cat'
```

Kullanıcıdan gelen her `int(input(...))` bir gün `ValueError` verir.
`try` / `except ValueError` ile yakala.

## try'dan sonra atanmamış ad

```python
try:
    x = int(input("What's x? "))
except ValueError:
    print("x is not an integer")

print(f"x is {x}")
```

```text
$ python number.py
What's x? cat
x is not an integer
Traceback (most recent call last):
  File "number.py", line 6, in <module>
    print(f"x is {x}")
                  ^
NameError: name 'x' is not defined
```

`except` çalıştıysa `x` hiç atanmadı. Değeri kullanan satırı `else`'e taşı ya
da döngüyle doğru değer gelene kadar sor.

## Yakalanmayan sıfıra bölme

```python
x = int(input("x: "))
print(10 / x)
```

```text
$ python divide.py
x: Traceback (most recent call last):
  File "divide.py", line 2, in <module>
    print(10 / x)
          ~~~^~~
ZeroDivisionError: division by zero
```

Bölen kullanıcıdan geliyorsa `except ZeroDivisionError:` de yaz. Bölme işlemi
`try`'ın **içinde** olmalı.

## Kapanmamış tırnak

```python
print("hello, world)
```

```text
$ python hello.py
  File "hello.py", line 1
    print("hello, world)
          ^
SyntaxError: unterminated string literal (detected at line 1)
```

Sözdizimi hatası program başlamadan çıkar; `try` onu yakalayamaz. Kodu düzelt.

## Hata vermeyen yanlışlar

Bunlar mesaj üretmez; program çalışır ama istediğini yapmaz.

| Yazdığın | Ne olur | Yerine |
|---|---|---|
| bütün programı `try`'a koymak | başka hatalar da yanlış mesajla yakalanır | yalnızca riskli satır |
| çıplak `except:` | yazım yanlışların bile sessizce yutulur | `except ValueError:` |
| `except ValueError: pass` döngüsüz | program yanlış girdide sessizce biter | `while True` ile yeniden sor |
| `else`'te `break` yok | doğru girdiden sonra da sorulmaya devam eder | `else: break` ya da `return` |
| `except ValueError:` ama hata `ZeroDivisionError` | yakalanmaz, program durur | iki türü de yaz |
| `EOFError` beklenmeden `input()` döngüsü | girdi bitince program hatayla durur | `except EOFError: break` |
