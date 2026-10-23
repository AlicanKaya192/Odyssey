Kütüphanelerle çalışırken en sık yapılan hatalar ve mesajları (Python 3.14'te
ölçüldü). Hata mesajının **son satırı** önce okunur.

## Argüman verilmeden sys.argv[1]

```python
import sys

print("hello, my name is", sys.argv[1])
```

```text
$ python name.py
Traceback (most recent call last):
  File "name.py", line 3, in <module>
    print("hello, my name is", sys.argv[1])
                               ~~~~~~~~^^^
IndexError: list index out of range
```

Kullanıcı argüman yazmadıysa listede yalnızca programın adı var. Önce
`len(sys.argv)`'a bak, gerekirse `sys.exit` ile çık.

## Yanlış yazılmış ya da kurulmamış modül

```python
import cowsy
```

```text
$ python say.py
Traceback (most recent call last):
  File "say.py", line 1, in <module>
    import cowsy
ModuleNotFoundError: No module named 'cowsy'
```

Adı denetle; doğruysa paket kurulu değildir: `pip install ...`.

## Modülde olmayan ad

```python
import random

print(random.randomint(1, 10))
```

```text
$ python generate.py
Traceback (most recent call last):
  File "generate.py", line 3, in <module>
    print(random.randomint(1, 10))
          ^^^^^^^^^^^^^^^^
AttributeError: module 'random' has no attribute 'randomint'. Did you mean: 'randint'?
```

Fonksiyonun adı `randint`. Python yakın bir ad bulursa önerir; bulamazsa
modülün belgesine bak.

## Hata vermeyen yanlışlar

Bunlar mesaj üretmez; program çalışır ama istediğini yapmaz.

| Yazdığın | Ne olur | Yerine |
|---|---|---|
| `cards = random.shuffle(cards)` | `cards` `None` olur | yalnızca `random.shuffle(cards)` |
| `for arg in sys.argv:` | programın adı da işlenir | `sys.argv[1:]` |
| `sys.argv[1] + 1` | `TypeError`: argüman metin | `int(sys.argv[1])` |
| `len(sys.argv) == 1` ile "bir argüman var" | argüman yokken doğru | bir argüman: `len(sys.argv) == 2` |
| `random.randint(1, 10)` ile 1–9 beklemek | 10 da gelebilir | `randint`'in iki ucu dahil |
| kendi dosyana `random.py` adı vermek | `import random` seninkini alır | kütüphane adlarını kullanma |
