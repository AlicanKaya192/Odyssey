# File I/O

Week 6 of CS50 Python. You can watch the lecture in the **Video** tab; this
page is its written form. Every program we have written so far kept its
information in **memory**: variables, lists, dicts. When the program ends,
all of it is gone. **File I/O** (input/output) means a program reading from
a file or writing to one. What is written to a file stays after the program
closes.

## A list that lives in memory

A program that asks for three names, sorts them and greets each, `names.py`:

```python
names = []

for _ in range(3):
    names.append(input("What's your name? "))

for name in sorted(names):
    print(f"hello, {name}")
```

```text
$ python names.py
What's your name? Hermione
What's your name? Harry
What's your name? Ron
hello, Harry
hello, Hermione
hello, Ron
```

`sorted` puts the list in alphabetical order. The program works, but it has
a flaw: the moment it closes, all three names are lost. Run it again
tomorrow and it has to ask all over. Let's keep the names in a file.

## open

`open` is a built-in Python function: it opens a file for reading, writing
or appending. As a first try, let's ask for a single name and write it to a
file:

```python
name = input("What's your name? ")

file = open("names.txt", "w")
file.write(name)
file.close()
```

`open("names.txt", "w")` takes two arguments: the file's name and a
**mode**. `"w"` is write mode: if the file does not exist, it creates it.
`file.write(name)` writes the name into the file and `file.close()` closes
the file. Let's run the program twice and look inside the file (`cat` prints
a file's contents in the terminal; in the Windows command prompt `type` does
the same, or you can open the file in an editor):

```text
$ python names.py
What's your name? Hermione
$ python names.py
What's your name? Harry
$ cat names.txt
Harry
```

Where is `Hermione`? `"w"` mode writes the file **from scratch** every time
it opens it; the second run erased what the first one wrote. To add to the
end of what is already there, use **append** mode, `"a"`:

```python
name = input("What's your name? ")

file = open("names.txt", "a")
file.write(name)
file.close()
```

```text
$ python names.py
What's your name? Hermione
$ python names.py
What's your name? Harry
$ python names.py
What's your name? Ron
$ cat names.txt
HermioneHarryRon
```

All three names are in the file, but stuck together. `write` writes only
what it is given; unlike `print`, it adds no line ending of its own. Let's
add the line ending (`\n`) ourselves:

```python
name = input("What's your name? ")

file = open("names.txt", "a")
file.write(f"{name}\n")
file.close()
```

```text
$ python names.py
What's your name? Hermione
$ python names.py
What's your name? Harry
$ python names.py
What's your name? Ron
$ cat names.txt
Hermione
Harry
Ron
```

Each name is now on its own line.

## with

It is easy to forget `file.close()`, and what you write to a file that is
never closed can be lost. Python offers the `with` keyword for this: it opens
the file and closes it **automatically** when the indented block ends.

```python
name = input("What's your name? ")

with open("names.txt", "a") as file:
    file.write(f"{name}\n")
```

`as file` gives the opened file a name. When the block ends, Python closes
the file; there is no need to write `close`.

## Reading from a file

Let's read what we wrote. `"r"` is read mode; `readlines` gives every line
of the file as a list:

```python
with open("names.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    print("hello,", line)
```

```text
$ python names.py
hello, Hermione

hello, Harry

hello, Ron
```

Why are there blank lines in between? Each line in the file ends with `\n`,
and `print` adds its own line ending too: two line endings. Let's remove the
whitespace and the line ending at the end of the text with `rstrip`:

```python
with open("names.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    print("hello,", line.rstrip())
```

```text
$ python names.py
hello, Hermione
hello, Harry
hello, Ron
```

There is an even shorter way. You can loop over the file directly; each turn
gives one line, so `readlines` is not needed. Reading is also the default
mode, so `"r"` can be left out:

```python
with open("names.txt") as file:
    for line in file:
        print("hello,", line.rstrip())
```

```text
$ python names.py
hello, Hermione
hello, Harry
hello, Ron
```

To show the names in order, let's first collect them in a list, then sort
it:

```python
names = []

with open("names.txt") as file:
    for line in file:
        names.append(line.rstrip())

for name in sorted(names):
    print(f"hello, {name}")
```

```text
$ python names.py
hello, Draco
hello, Harry
hello, Hermione
hello, Ron
```

Since a file can be looped over, it can also go straight into `sorted`:
`for line in sorted(file):`. For reverse order, `sorted(names,
reverse=True)`.

## CSV

What if we want to keep more than a name? Let's store students' names and
houses. A common way is **CSV** (comma-separated values): each line is a
record and the fields are separated by commas. `students.csv`:

```text
Hermione,Gryffindor
Harry,Gryffindor
Ron,Gryffindor
Draco,Slytherin
```

Let's split each line at the comma (`split(",")`):

```python
with open("students.csv") as file:
    for line in file:
        row = line.rstrip().split(",")
        print(f"{row[0]} is in {row[1]}")
```

```text
$ python students.py
Hermione is in Gryffindor
Harry is in Gryffindor
Ron is in Gryffindor
Draco is in Slytherin
```

`row` is a list of two items: `row[0]` is the name, `row[1]` the house. In
Python we can **unpack** a list straight into two variables: `name, house =
line.rstrip().split(",")`. The code becomes easier to read:

```python
with open("students.csv") as file:
    for line in file:
        name, house = line.rstrip().split(",")
        print(f"{name} is in {house}")
```

```text
$ python students.py
Hermione is in Gryffindor
Harry is in Gryffindor
Ron is in Gryffindor
Draco is in Slytherin
```

### Sorting dicts

If we want the sentences sorted by the student's name, we need to sort the
students, not the strings. Let's make each student a dict and put them in a
list. Python does not know how to compare dicts; we tell `sorted` what to
sort by with the `key` argument. We give `key` a **function**: it takes a
student and returns the value to sort by:

```python
students = []

with open("students.csv") as file:
    for line in file:
        name, house = line.rstrip().split(",")
        student = {"name": name, "house": house}
        students.append(student)


def get_name(student):
    return student["name"]


for student in sorted(students, key=get_name):
    print(f"{student['name']} is in {student['house']}")
```

```text
$ python students.py
Draco is in Slytherin
Harry is in Gryffindor
Hermione is in Gryffindor
Ron is in Gryffindor
```

Note that we wrote `key=get_name`, not `get_name()`: we are not calling the
function, we are handing it to `sorted`, which calls it for each student. If
writing a named function just for this feels long, there is **lambda**: a
nameless, one-expression function. `lambda student: student["name"]` means
"take a student, return their name":

```python
students = []

with open("students.csv") as file:
    for line in file:
        name, house = line.rstrip().split(",")
        students.append({"name": name, "house": house})

for student in sorted(students, key=lambda student: student["name"]):
    print(f"{student['name']} is in {student['house']}")
```

The output is the same. To sort by house, `student["house"]` is enough.

### A comma inside a field

Now let's store each student's home instead of their house. Harry's home is
"Number Four, Privet Drive"; the address has a comma. In that case CSV puts
the field in quotes:

```text
Harry,"Number Four, Privet Drive"
Ron,The Burrow
Draco,Malfoy Manor
```

`split(",")` does not know about quotes and splits Harry's line into three
pieces:

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

Instead of solving this by hand, let's use Python's **`csv`** library.
`csv.reader` reads quotes and the commas inside them correctly and gives
each row as a list:

```python
import csv

students = []

with open("students.csv") as file:
    reader = csv.reader(file)
    for name, home in reader:
        students.append({"name": name, "home": home})

for student in sorted(students, key=lambda student: student["name"]):
    print(f"{student['name']} is from {student['home']}")
```

```text
$ python students.py
Draco is from Malfoy Manor
Harry is from Number Four, Privet Drive
Ron is from The Burrow
```

### DictReader

The first line of most CSV files is a **header**: the names of the columns.
Let's add `name,home` to the top of `students.csv`:

```text
name,home
Harry,"Number Four, Privet Drive"
Ron,The Burrow
Draco,Malfoy Manor
```

`csv.DictReader` reads the header and gives each row as a dict keyed by the
column names:

```python
import csv

students = []

with open("students.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        students.append({"name": row["name"], "home": row["home"]})

for student in sorted(students, key=lambda student: student["name"]):
    print(f"{student['name']} is from {student['home']}")
```

```text
$ python students.py
Draco is from Malfoy Manor
Harry is from Number Four, Privet Drive
Ron is from The Burrow
```

There is another benefit: if someone swaps the columns in the file
(`home,name`), the program still works, because we read the columns by
name, not by position.

## Writing a CSV

Let's take a name and a home from the user and add them to the end of
`students.csv`. `csv.writer` writes each row from a list and puts a field
that contains a comma in quotes by itself:

```python
import csv

name = input("What's your name? ")
home = input("Where's your home? ")

with open("students.csv", "a") as file:
    writer = csv.writer(file)
    writer.writerow([name, home])
```

On this computer (Windows), let's run it twice and look at the file:

```text
$ python students.py
What's your name? Harry
Where's your home? Number Four, Privet Drive
$ python students.py
What's your name? Ron
Where's your home? The Burrow
$ cat students.csv
Harry,"Number Four, Privet Drive"

Ron,The Burrow
```

The quotes are right, but there is a blank line between the rows. The cause
is Windows: `csv.writer` ends each row with `\r\n`, and on Windows a file
opened in text mode also turns every `\n` into `\r\n`; the row ends with
`\r\r\n`, and whoever reads it sees two line endings. Python's documentation
says to open a CSV file with `newline=""`: the file leaves line endings
alone and lets `csv` handle them. CS50 runs on Linux, so it never sees this
problem; since we run on Windows, we will always write `newline=""` when
writing a CSV:

```python
import csv

name = input("What's your name? ")
home = input("Where's your home? ")

with open("students.csv", "a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([name, home])
```

```text
$ python students.py
What's your name? Harry
Where's your home? Number Four, Privet Drive
$ python students.py
What's your name? Ron
Where's your home? The Burrow
$ cat students.csv
Harry,"Number Four, Privet Drive"
Ron,The Burrow
```

The blank lines are not just cosmetic. When `csv.reader` reads this file
written without `newline=""`, the blank lines come back as empty lists
(`[]`) and `for name, home in reader:` raises a `ValueError` at the first
one; `DictReader` skips blank lines, so it shows no problem. Fixing it when
writing is cleanest.

### DictWriter

`csv.DictWriter` writes a row from a dict; `fieldnames` sets the order of
the columns. The order of the keys in the dict does not matter:

```python
import csv

name = input("What's your name? ")
home = input("Where's your home? ")

with open("students.csv", "a", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "home"])
    writer.writerow({"home": home, "name": name})
```

```text
$ python students.py
What's your name? Harry
Where's your home? Number Four, Privet Drive
$ python students.py
What's your name? Ron
Where's your home? The Burrow
$ cat students.csv
Harry,"Number Four, Privet Drive"
Ron,The Burrow
```

If the file is empty, `writer.writeheader()` writes the header row first;
you will use it in the problem set.

## Binary files and PIL

Text files are made of readable characters. **Binary** files are just ones
and zeros: images, audio, video. We can read and write those too, but
understanding what is inside takes a library that knows the format. The
common one for images is **Pillow**; in a program it is imported as `PIL`
(`pip install Pillow`, installed in Odyssey).

Say we have two **costumes** of a character: `costume1.gif` and
`costume2.gif`. Let's make one animated GIF that flips between them. We take
the file names from the command line, `costumes.py`:

```python
import sys

from PIL import Image

images = []

for arg in sys.argv[1:]:
    image = Image.open(arg)
    images.append(image)

images[0].save(
    "costumes.gif", save_all=True, append_images=[images[1]], duration=200, loop=0
)
```

```text
$ python costumes.py costume1.gif costume2.gif
```

`Image.open` opens an image. The animated GIF is written by the first
image's `save` method: `save_all=True` means several frames, `append_images`
the frames added after the first, `duration=200` how long each frame stays
on screen (milliseconds), `loop=0` loop forever. The result:

<figure class="fig"><div class="versus"><div><h5>costume1.gif</h5><img src="data:image/gif;base64,R0lGODdheAB4AIIAAP////r27Hxc3FpAtB4eKAAAAAAAAAAAACwAAAAAeAB4AEAI/wADCBxIsKDBgwgTKlzIsKHDhxAjSpxIsaLFiw4FaNzIsaNHjCBDQvRIsqRJkiJTYjwJoCUAAjAJuNzo8mXMmSZV6hx5sqfPnjuDPvwZk0DHoj+FKkX4s6nTnEtDPp1KtWlUhlWzaq2q1CfBrWCffvV6EWXDsGg/nj159WBarW3jDphLt65dk3bz1o3Ld6DevAv/2u1LuLDhw4gTS3zLUXHUnjUBmIwM1LFIyC5h4qSZWWbLypZBMk4aeuXoqaUjnkabeuzq12rjwp6dVSpog7TDJiRLOLdTihtLd7xLlXjw1iAF/yWpXC/y59CjS59Ovbp1w1CvP06r3TTs7jx9a/8Ev5Bl5M0az6OPTb6geZtFP6dvWVSz5OztB/6kXJL/7fwCidcRgG71FJOBRvFGoH5T1QcTVQsGICBb5E1IGnUW1tZahm8pxuFrfX0ooFCkiSiWhApalGKAJq6IIoUT/Ydbi/gxJeNQ44VHY444DogdjRFyGKFBzc3VU5EDDEkkknQxx+RcShL0ZEJTRonQYBJhaeWWXHbp5ZdghinmmGSWuaFVZioEVpoMdkjmd2D65uWIW1poJWb+caTejflNVpN98gkQGaD3mRWkn/DdVGhn8RVqKIHvJbrZn4o6yh6APu3pkaYwQvqhkkKCmuGdE3Lp04ElodqpqEQ5iBSaQ4qguOCOfe4oQIW28mhdro1Vx+ujyP26qmXCXuhYsb8lhixqPy4LIV/OrrldtLoFlRS1txprG4zYtjkscDJGO+O3OpZk47Ln1pgRn97+Wh67apr7brFYuVjvcWu5uy6wiy3Gq7/49mZrRbcqC6SnocZaqqkCCOaUwwVz+SReTEr85ABOVhnlxRh7xPGWHy+p8cYVX1myl4I9lDKbLLfsckoBAQA7" alt="costume1.gif" width="120" height="120"></div><div><h5>costume2.gif</h5><img src="data:image/gif;base64,R0lGODdheAB4AIIAAP////r27Hxc3FpAtB4eKAAAAAAAAAAAACwAAAAAeAB4AEAI/wADCBxIsKDBgwgTKlzIsKHDhxAjSpxIsaLFiw4FaNzIsaNHjCBDQvRIsqRJkiJTYjwJoCUAAjAJuNzo8mXMmSYtnlSZ8aTPnz4f/uRZEWhMAh2PAl04lChFoFCjSt3o9OnUq1hRVo2YtatXrVsPNhX4tSzUsAbBMjXLlipap22zvp0rcIDdu3jzmszLFy/dvwP78l0oOC/gw4gTK17MWGJct423+qwJwCTloCEhJ57sEiZOmp1ltsQ8kvTmx6YTjm2MeurApZFft44bm+zs24tv61YbdnXB3WVr9wQOW3hRjnqvJtds/GJhwSSf921Ovbr169iza99uPCf3uW2/g//cLZ4rceblxVqm/Fkj+/YfL/L+y7LlUc+V3du/P9q749Tg/XRZSQMCqFBxp52HHkK+MfZTTD7BhCCDBjo41X0SupZWhRYqWFIADcbmoVzUjUhidyZ2hWKKX7HGYniIwfaiVICFOOOEve104I3+Hbbgjjz+qF2Q6ak3YpEMSWeXT0oOgGSSTd4VXZR2PakQlQlhaaVDhknU5ZZghinmmGSWaeaZaKap5po+nsWmUF69SSGMcuK2JnFpKnjmkSIJEBlnBXL0HoelCRkgSZTh158AiYq2aHw6zXcoovsdtWholub3oVU60rdepY6CBip8HU0U4lsCskdpoJvCSWiOKRay2mOCHro6q2KxMnQqrrWu9SqtJUEYbIadqvYrsCdheF9UxhYr3Iu/HRsjjyDu2mGQzj6Lbbbabitpbd7eCm643/5JbqsrngvpuOqKi2y76/IKr7RVzevmtEHZ6ye+/unbZrbz1lhhwJOiayS5/8Z7cLjA2rqtg/89nJ7ERRK5JbRj8mmmRoVF1fG+Z1K5V5QhUznAlFqSafLJHq1spssGwVxmyjGTrGZhD+Es584899xYQAA7" alt="costume2.gif" width="120" height="120"></div><div><h5>costumes.gif</h5><img src="data:image/gif;base64,R0lGODlheAB4AIIAAP////r27Hxc3FpAtB4eKAAAAAAAAAAAACH/C05FVFNDQVBFMi4wAwEAAAAh+QQAFAAAACwAAAAAeAB4AAAI/wADCBxIsKDBgwgTKlzIsKHDhxAjSpxIsaLFixgzatzIsaPHjyBDihxJsqTJkyhTqlzJsqXLlzBjypxJs6bNmzhz6swooKdPnztj/hxKNKhKokiTGi2ZtGnRpSCdSn0KdePUqz+rasTKtafWi13DfqUYtuzYiGXTnn2Y1uxahm3Vvk0Yt+1chHXl3i0oFYBfv03/Ana6l69TwX+RIh7ctPDAw4sZ94wsmWrhwIIJEBDsE7FmzkodQ/ar+TPjzKUTN76MGUDp1AA6k369OfbqvaNp15btmnbloaJb9zZtWwBq4oRZC0f+E7Xq23enRla8eGrwvqCpP0+OO2/c697dKv8Pz9WxQPJizaPvav78euvtA7yH335qaamar8Z37/R+Uv/cxXfVa0MRSF99WOlGW3kIdqWgeN3Np1+EEk74VoXprYUhexpuyOFYHn6oVYgZVkWiiEudWKJRKqKoU4t65QSjXTLOSKNNNtaFY446zsSjdz7+mJdQQg75UpHhuYQkeSwtid5RTj55UpTvmUTlfCRdKaFIWlYYlXVdAmehVfCFmZV8B/Ik1WNmesVfgGCtyWabBI1ZUZpohmkQnhLxSeeecpIVqGF6HsRnQ4fm2SVdgzqU6JtULvQoXnACqiVcjSIamkKFcjqpoZZ5Gqmm0EEEnKNXsrXpRECZGiVaobKT2uersLa6kpOCCqDkknfChORcvwL743gwqjejgC3up6gAAzTbbFrOPnumsj1Fay1X1kbrprIBZOutVN5my2234WbbVLniKovutUmtG6267mpLVLzvxkevs0jd2+x++g6Qr7786vvvvQETbFC/8MabkMEFu7swveMqrJDE45Lr7UPlVnxwvRFZq/HHIIcs8sgkkxQQACH5BAEUAAgALFYAGwAeAEMAgv////r27Hxc3FpAtB4eKAAAAAAAAAAAAAjMABEIHEiwoEGBAg4qXEhQgEOGEAs6nBgx4sSLFRlexJjR4MaNHRt+BBlyJMmOJjmiTPmwJMuWGV/CjPkyJAKZNnG6ZJmz5s6UPX2u5PnTZFCgRUceNZr041KmNIVGRdpUZdWZT7FmtXnwJFeRFL92TSi2bMgAAcwaRJtW7UC2bd3CjWt2Lt2yc90isCuXb127d20CRot3cOCMhglzTaz4LOPDEB9DZih58WPLjDEb/npZ82DOmT0DBp1Y9GjBpUn7FXv6L1u9exvrhRwQADs=" alt="costumes.gif" width="120" height="120"></div></div><figcaption>The two costumes and the animated GIF made from them (the one on the right waves).</figcaption></figure>

## Summing up

This week we saw programs talk to files:

- `open` and its modes: `"r"` read, `"w"` write from scratch, `"a"` append
- `with`: the file closes by itself when the block ends
- The `\n` on lines you read: `rstrip`
- CSV: `csv.reader`, `csv.DictReader`, `csv.writer`, `csv.DictWriter`;
  `newline=""` when writing on Windows
- `sorted(..., key=...)` and `lambda`
- Binary files and images with `PIL`

---

*This section is translated and adapted from week 6 of Harvard University's [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) (lecture notes and problem set); examples and exercises were changed, and the problem set is checked by Odyssey, not by CS50's check50. The original and this adaptation are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Harvard does not endorse this adaptation.*
