The most common mistakes when working with files, and their messages
(measured on this computer with Python 3.14). Read the **last line** of an
error message first.

## Reading a file that does not exist

The file is `names.txt`; the program says `name.txt`:

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

Check the name and the folder the program runs in. If the file name comes
from the user, catch it with `try` / `except FileNotFoundError` and give a
clear message with `sys.exit`.

## Writing in read mode

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

Without a mode, `open` opens for reading. Use `"w"` to write, `"a"` to
append.

## Splitting a field with a comma using split

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

`split(",")` knows nothing about quotes; `"Number Four, Privet Drive"`
becomes two pieces. Read a CSV with `csv.reader` or `csv.DictReader`.

## Calling the function you give to key

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

`key=get_name()` calls the function right away, with no argument. `sorted`
needs the function itself: `key=get_name`.

## Mistakes that raise no error

| Mistake | What happens | Instead |
|---|---|---|
| `"w"` when you meant to append | the old lines are silently erased | `"a"` |
| `file.write(name)` | the names stick together | `file.write(f"{name}\n")` |
| Printing a line you read without `rstrip` | blank lines appear in between | `line.rstrip()` |
| `csv.writer` on Windows without `newline=""` | blank lines between rows; `csv.reader` returns them as `[]` | `open(..., newline="")` |
| Forgetting `close` outside `with` | what you wrote may not reach the file | `with open(...) as file:` |
| Not keeping the result of `ImageOps.fit(photo, size)` | the image is not cropped | `photo = ImageOps.fit(photo, size)` |
