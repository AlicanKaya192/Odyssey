Dosyalarla çalışırken en sık yapılan hatalar ve mesajları (Python 3.14'te,
bu bilgisayarda ölçüldü). Hata mesajının **son satırı** önce okunur.

## Olmayan dosyayı okumak

Dosya `names.txt`, programda `name.txt` yazılmış:

```python
with open("name.txt") as file:
    for line in file:
        print(line.rstrip())
```

```text
$ python names.py
Traceback (most recent call last):
  File "names.py", line 1, in <module>
    with open("name.txt") as file:
         ~~~~^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'name.txt'
```

Adı ve programın çalıştığı klasörü denetle. Kullanıcıdan gelen bir dosya
adıysa `try` / `except FileNotFoundError` ile yakala ve `sys.exit` ile
anlaşılır bir mesaj ver.

## Okuma kipinde yazmak

```python
with open("names.txt") as file:
    file.write("Ron\n")
```

```text
$ python names.py
Traceback (most recent call last):
  File "names.py", line 2, in <module>
    file.write("Ron\n")
    ~~~~~~~~~~^^^^^^^^^
io.UnsupportedOperation: not writable
```

`open` kip verilmeden okumak için açar. Yazmak için `"w"`, eklemek için `"a"`.

## Virgüllü alanı split ile bölmek

```python
with open("students.csv") as file:
    for line in file:
        name, home = line.rstrip().split(",")
        print(f"{name} is from {home}")
```

```text
$ python students.py
Traceback (most recent call last):
  File "students.py", line 3, in <module>
    name, home = line.rstrip().split(",")
    ^^^^^^^^^^
ValueError: too many values to unpack (expected 2, got 3)
```

`split(",")` tırnağı bilmiyor; `"Number Four, Privet Drive"` iki parça
oluyor. CSV'yi `csv.reader` ya da `csv.DictReader` ile oku.

## key'e fonksiyonu çağırarak vermek

```python
students = []

with open("students.csv") as file:
    for line in file:
        name, house = line.rstrip().split(",")
        student = {"name": name, "house": house}
        students.append(student)


def get_name(student):
    return student["name"]


for student in sorted(students, key=get_name()):
    print(f"{student['name']} is in {student['house']}")
```

```text
$ python students.py
Traceback (most recent call last):
  File "students.py", line 14, in <module>
    for student in sorted(students, key=get_name()):
                                        ~~~~~~~~^^
TypeError: get_name() missing 1 required positional argument: 'student'
```

`key=get_name()` fonksiyonu hemen, argümansız çağırıyor. `sorted`'a
fonksiyonun kendisi verilir: `key=get_name`.

## Hata vermeyen yanlışlar

| Yanlış | Ne olur | Doğrusu |
|---|---|---|
| Eklemek isterken `"w"` | eski satırlar sessizce silinir | `"a"` |
| `file.write(name)` | isimler yan yana yapışır | `file.write(f"{name}\n")` |
| Okunan satırı `rstrip`'siz yazmak | araya boş satırlar girer | `line.rstrip()` |
| Windows'ta `newline=""` olmadan `csv.writer` | satır aralarında boş satır; `csv.reader` onları `[]` diye verir | `open(..., newline="")` |
| `with` dışında `close`'u unutmak | yazılanlar dosyaya geçmeyebilir | `with open(...) as file:` |
| `ImageOps.fit(photo, size)`'ın sonucunu atmamak | resim kırpılmaz | `photo = ImageOps.fit(photo, size)` |
