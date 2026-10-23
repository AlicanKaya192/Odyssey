# Libraries

The fifth week of CS50 Python. You can watch the video in the **Video** tab;
this page is the written version of the lecture. **Libraries** are bits of code
written by you or others that you can use in your program. Python lets you
share functions and features with others as **modules**. If you copy and paste
code from an old project, chances are you could make it a module to bring into
your new project.

## random

`random` is a library that comes with Python and that you can import into your
own project. As a coder, it is easier to stand on the shoulders of those who
came before. To load a module into your program you write `import`. Inside the
`random` module there is a function called `random.choice(seq)`: `random` is
the module you import, `choice` the function inside it, and `seq` a sequence
(such as a list). `generate.py`:

```python
import random

coin = random.choice(["heads", "tails"])
print(coin)
```

```text
$ python generate.py
heads
```

Since the list has two items, Python gives heads and tails a 50% chance each.
The result can change on every run; the outputs here are examples, yours may
differ.

With `from` you can take just the part of a module you want. `import random`
brought all of the module's functions; to take only `choice`:

```python
from random import choice

coin = choice(["heads", "tails"])
print(coin)
```

Now you no longer need to write `random.choice`, just `choice`. The code is
shorter and easier to read.

`random.randint(a, b)` generates a random integer between `a` and `b` (both
included):

```python
import random

number = random.randint(1, 10)
print(number)
```

```text
$ python generate.py
3
```

`random.shuffle(x)` shuffles a list into a random order:

```python
import random

cards = ["jack", "queen", "king"]
random.shuffle(cards)
for card in cards:
    print(card)
```

```text
$ python generate.py
queen
king
jack
```

`random.shuffle` shuffles the cards **in place**: unlike the other functions
it does not return a value, it changes the `cards` list itself. Run it a few
times to see the order change.

## statistics

Python also comes with a `statistics` library. `mean` takes a list of values
and gives their average. `average.py`:

```python
import statistics

print(statistics.mean([100, 90]))
```

```text
$ python average.py
95
```

## Command-line arguments

So far we have given every value inside the program or asked for it with
`input`. What if we wanted to take input **from the command line**? For
example, typing `python average.py 100 90` rather than `python average.py` and
getting the average of 100 and 90.

`sys` is a module that lets us take arguments at the command line. Its `argv`
is a list recording what the user typed on the command line. `name.py`:

```python
import sys

print("hello, my name is", sys.argv[1])
```

```text
$ python name.py David
hello, my name is David
```

Why is `David` in `sys.argv[1]`? Remember that lists start at 0. If you guessed
that `sys.argv[0]` holds the program's name, `name.py`, you are right.

There is a small problem: what if the user does not type a name?

```text
$ python name.py
Traceback (most recent call last):
  File "name.py", line 3, in <module>
    print("hello, my name is", sys.argv[1])
                               ~~~~~~~~^^^
IndexError: list index out of range
```

There is nothing at `sys.argv[1]`, because nothing was typed. Let us protect the
program from this kind of error:

```python
import sys

try:
    print("hello, my name is", sys.argv[1])
except IndexError:
    print("Too few arguments")
```

```text
$ python name.py
Too few arguments
```

If the user forgets the name, they now get a hint about how to run the program.
We can be more defensive and catch too many arguments as well:

```python
import sys

if len(sys.argv) < 2:
    print("Too few arguments")
elif len(sys.argv) > 2:
    print("Too many arguments")
else:
    print("hello, my name is", sys.argv[1])
```

```text
$ python name.py David Malan
Too many arguments
```

That is logically correct. But there is something nice about keeping the error
checking apart from the rest of the code. `sys`'s `exit` function lets the
program exit when the user makes a mistake:

```python
import sys

if len(sys.argv) < 2:
    sys.exit("Too few arguments")
elif len(sys.argv) > 2:
    sys.exit("Too many arguments")

print("hello, my name is", sys.argv[1])
```

```text
$ python name.py David
hello, my name is David
```

```text
$ python name.py
Too few arguments
```

If the program finds an error, it never reaches the last line. `sys.argv` is
how users give information from the command line, and `sys.exit` is how the
program leaves when an error comes up.

## Slices

A **slice** is a way of saying where a list should start and end. Let us greet
several names:

```python
import sys

if len(sys.argv) < 2:
    sys.exit("Too few arguments")

for arg in sys.argv:
    print("hello, my name is", arg)
```

```text
$ python name.py David Carter Rongxin
hello, my name is name.py
hello, my name is David
hello, my name is Carter
hello, my name is Rongxin
```

Besides the names we wanted, it also printed `hello, my name is name.py`. To
skip the list's first item, the program's name, let us start the list at 1:

```python
import sys

if len(sys.argv) < 2:
    sys.exit("Too few arguments")

for arg in sys.argv[1:]:
    print("hello, my name is", arg)
```

```text
$ python name.py David Carter Rongxin
hello, my name is David
hello, my name is Carter
hello, my name is Rongxin
```

`[1:]` means "from position 1 to the end". Slices work on any list; the start
is included, the end is not:

```python
students = ["Hermione", "Harry", "Ron", "Draco"]

print(students[1:])
print(students[:2])
print(students[1:3])
print(students[-1])
```

```text
$ python slices.py
['Harry', 'Ron', 'Draco']
['Hermione', 'Harry']
['Harry', 'Ron']
Draco
```

## Packages

One reason Python is so popular is its many powerful **third-party** libraries
that add functionality. These libraries, which come as a folder, are called
**packages**. **PyPI** is a directory of all the third-party packages available
today. Python's package manager, `pip`, installs a package quickly:

```text
pip install cowsay
```

`cowsay` is a well-known package that lets a cow talk to the user. It comes
installed in Odyssey; on your own computer, for your own projects, the command
above is all you need. `say.py`:

```python
import cowsay
import sys

if len(sys.argv) == 2:
    cowsay.cow("hello, " + sys.argv[1])
```

```text
$ python say.py David
  ____________
| hello, David |
  ============
            \
             \
               ^__^
               (oo)\_______
               (__)\       )\/\
                   ||----w |
                   ||     ||
```

The program first checks that the user typed exactly one argument at the
command line (`sys.argv` has two items: the program's name and that argument),
then the cow speaks. Write `cowsay.trex` instead of `cowsay.cow` and a T-rex
speaks.

## APIs

**APIs** (application programming interfaces) let you connect to other
people's code. The `requests` package lets your program behave as a web browser
would. Apple's iTunes has an API; in the lecture David shows that this address
searches for a song and returns the answer as **JSON**:
`https://itunes.apple.com/search?entity=song&limit=1&term=weezer`. JSON is a
text-based format for exchanging data between applications; Python can turn
it into dicts and lists.

```python
import json
import requests
import sys

if len(sys.argv) != 2:
    sys.exit()

url = "https://itunes.apple.com/search?entity=song&limit=50&term="
response = requests.get(url + sys.argv[1])

o = response.json()
for result in o["results"]:
    print(result["trackName"])
```

This code connects to the internet, so it was not run here; you can see its
output in the video. `response.json()` turns the response into a dict; under
the `results` key there is a list of dicts, each with a `trackName`.

Python's built-in `json` library makes this data easier to read:
`json.dumps(..., indent=2)` turns it into indented, readable text. With local
sample data of the same shape:

```python
import json

data = {
    "resultCount": 2,
    "results": [
        {"trackName": "Track One", "artistName": "Band"},
        {"trackName": "Track Two", "artistName": "Band"},
    ],
}

print(json.dumps(data["results"][0], indent=2))

for result in data["results"]:
    print(result["trackName"])
```

```text
$ python itunes.py
{
  "trackName": "Track One",
  "artistName": "Band"
}
Track One
Track Two
```

Odyssey does exercises that go out to the internet with its own **exercise
server**: this week's Bitcoin price problem sends its request to an address
that answers like a real API but never leaves your computer.

## Making your own libraries

As a Python programmer you can make your own library too, whenever you want to
reuse a piece of code again and again or share it with others. A module that
says "hello" and "goodbye", `sayings.py`:

```python
def hello(name):
    print(f"hello, {name}")


def goodbye(name):
    print(f"goodbye, {name}")
```

On its own this code does nothing for the user. But if another programmer
imports it, they can use these functions in their own code. `say.py`:

```python
import sys

from sayings import goodbye

if len(sys.argv) == 2:
    goodbye(sys.argv[1])
```

```text
$ python say.py David
goodbye, David
```

`from sayings import goodbye` takes `goodbye` from the `sayings` module; the
module's name is the file's name without `.py`.

## Summing up

Libraries extend what Python can do. Some come with Python and only need
importing; others are third-party packages installed with `pip`; and you can
make your own:

- `import` and `from ... import ...`
- `random`: `choice`, `randint`, `shuffle`
- `statistics.mean`
- `sys.argv`, `sys.exit` and command-line arguments
- Slices: `[1:]`, `[:2]`, `[1:3]`
- Packages, PyPI and `pip`
- APIs, `requests` and JSON
- Your own module

## This week's problem set

The seven exercises in the **Exercise** tab practise this lecture's topics one
by one. The six in the **Problem Set** tab are CS50's assignment for the week
(Problem Set 4):

| Problem | What it asks | Topic in the lecture |
|---|---|---|
| Emojize | `:thumbs_up:` → an emoji | a package (`emoji`) |
| Frank, Ian and Glen's Letters | large letters | a package (`pyfiglet`), `sys.argv`, `sys.exit` |
| Adieu, Adieu | join names as `a, b, and c` | a package (`inflect`), `EOFError` |
| Guessing Game | find the random number | `random.randint`, asking again |
| Little Professor | ten addition problems | `random`, functions |
| Bitcoin Price Index | get a price from an API | `requests`, JSON, `sys.argv` |

Each package is explained with a hint in its prompt; CS50 also sends students
to the package's documentation.

---

*This section is translated and adapted from week 4 of Harvard University's [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) (lecture notes and problem set); examples and exercises were changed, and the problem set is checked by Odyssey, not by CS50's check50. The original and this adaptation are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Harvard does not endorse this adaptation.*
