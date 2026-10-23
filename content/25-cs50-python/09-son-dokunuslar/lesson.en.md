# Et Cetera

The tenth and last week of CS50 Python. You can watch the video in the
**Video** tab; this page is the lecture in writing. So far we have seen
functions, conditionals, loops, exceptions, libraries, tests, files, regular
expressions and classes; with them you can solve a great many problems. This
week has no single big topic: instead there are small tools that don't quite
fit under any of the earlier headings but make code shorter, more readable and
more robust. Hence the name: "et cetera".

## Sets

Let's print which houses appear among a few Hogwarts students, each one once,
`houses.py`. The way we know: an empty list, and add a house if it isn't in
the list yet.

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

It works, but we wrote the "is it already there?" check ourselves. Python has
a data type that does this by itself: the **set**. A value appears in a set
at most once; adding the same value a second time changes nothing.

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

- An empty set is created with `set()` and you add with `add` (like a list's
  `append`, but there is no "end" to add to).
- A set has no order. We want the output in alphabetical order, so we used
  `sorted`.

A few small details:

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

A set with values can be written with curly braces: `{"Gryffindor",
"Slytherin"}`. But **empty** curly braces `{}` are not a set, they are an
empty dictionary; the last two lines show it. `in` is very fast on a set:
asking whether a value is in it finishes almost at once, compared with
searching a long list from start to end.

## Global variables

A bank account, `bank.py`. The balance is a **global variable**, defined at
the top of the file, outside every function. Reading it from inside a function
is no problem:

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

Now let's add two functions that deposit and withdraw money:

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

When Python sees that a **name is assigned to** inside a function, it treats
that name as a **local variable** of that function. `balance += n` means
`balance = balance + n`; so `deposit` has its own `balance`, and it has not
been given a value yet. The error says exactly that: a local variable can't
be used before it has a value.

The way to tell a function "this name is the variable at the top of the file"
is the `global` keyword:

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

`global` works, but use it with care: the more functions change a global
variable, the harder it is to follow who changed what and when. Last week's
object-oriented programming gives a tidier solution here: put the balance
inside an object.

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

The balance now lives in `self._balance`; every method reaches it through
`self`, and no `global` is needed. `balance` is a property (`@property`) with
no setter: it can be read from outside, but only `deposit` and `withdraw`
change it.

## Constants

A number like `3` buried in the code is called a **magic number**: it is not
clear what it stands for, and when it has to change it is hard to find. Moving
it to the top of the file, into a variable with a name, is a good habit. By
convention, variables that should not change are written in **capital
letters**; they are called **constants**.

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

But Python does not protect constants. The capital letters are only a
convention telling the reader "don't touch this"; the code below meows four
times without any warning. In some other languages a line like that would be
an error.

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

A class can have a constant too: a class variable, in capital letters. You
reach it through the class's name, `Cat.MEOWS`:

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

## Type hints

Python is a **dynamically typed** language: you don't write a variable's
type, Python works it out from the value it is given. Some languages want the
type written out; the upside is that using the wrong type is caught before the
program runs. In Python too you can write which type a value should have: a
**type hint**.

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

- `n: int` says that `meow`'s parameter `n` is expected to be an int.
- `number: int = ...` makes the same note about a variable.

But the program still failed with the same `TypeError`: `input` returns a
string, and Python **does not look** at the hints. You need a separate
program that reads and checks them; the best known is **mypy** (`pip install
mypy`, then `mypy meows.py`). mypy does not run the program, it only reads it.
In this code it stops at the line `number: int = input(...)`: the `str` that
`input` returns is assigned to a variable hinted as `int`. So the mistake is
shown to the person writing the code, before any user runs the program.
Odyssey does not run mypy; here we only describe what it does.

To see that Python only stores the hints:

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

The hint sits in `__annotations__`, but `double("ha")` returned `haha` with no
warning. A hint is a note, not a requirement.

The type of the return value is written with `->`. This code has a mistake:

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

`meow` prints but does not **return** anything. A function without `return`
returns `None`; that is why the last line printed `None`. Had we written
`def meow(n: int) -> None:`, mypy would have warned at `meows: str =
meow(number)` that the function returns no value. The fix is for `meow` to
return the string instead of printing it:

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

- `-> str`: `meow` returns a string.
- `"meow\n" * n`: a string times an integer puts the string next to itself
  that many times; no loop needed.
- The string already ends with a newline, so we gave `print` `end=""`;
  otherwise an empty line would be left at the end.

A function that returns is also better for unit tests: you can write
`assert meow(3) == "meow\nmeow\nmeow\n"`.

## Docstrings

Instead of writing what a function does above it with `#`, Python has a
standard (PEP 257): the **docstring**, written in triple quotes on the
**first line** of the function's body.

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

Python keeps the docstring in `meow.__doc__`; documentation tools can read the
code and turn these into web pages or PDFs. The `:param n:`, `:type n:`,
`:raise TypeError:`, `:return:` and `:rtype:` lines are not Python's own but
a convention of a format called **reStructuredText**; some popular
documentation tools understand it.

## Command-line arguments: argparse

Instead of asking the user how many times `meows.py` should meow, let's take
it from the command line: `python meows.py -n 3`. Options like `-n` in
command-line programs are called **switches** or **flags**. With `sys.argv`
from the libraries week:

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

It works, but as options multiply (`-n`, `-a`, `-b`... and in any order) this
chain of `if`s quickly gets out of hand. Python's own library has a module
for this job: **argparse** (argument parser).

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

- `argparse.ArgumentParser()` creates a parser object.
- `add_argument("-n")` tells it which option to recognize.
- `parse_args()` reads `sys.argv` by itself and puts the options, in whatever
  order they come, into the `args` object: `args.n`.

But if `-n` is not given, `args.n` is `None`:

```text
$ python meows.py
Traceback (most recent call last):
  File "meows.py", line 7, in <module>
    for _ in range(int(args.n)):
                   ~~~^^^^^^^^
TypeError: int() argument must be a string, a bytes-like object or a real
number, not 'NoneType'
```

A few named arguments of `add_argument` solve this and more:

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

- `default=1`: the value when the option is not given.
- `type=int`: argparse converts the value to an integer; no need to write
  `int(...)`.
- `description` and `help`: explanations shown in the usage information.

In command-line programs `-h` or `--help` almost always prints the usage
information; argparse adds it by itself:

```text
$ python meows.py -h
usage: meows.py [-h] [-n N]

Meow like a cat

options:
  -h, --help  show this help message and exit
  -n N        number of times to meow
```

Square brackets in documentation mean "optional": you don't have to write
`-h` or `-n N`. If the user gives an invalid value, argparse prints the usage
and the problem and ends the program:

```text
$ python meows.py -n dog
usage: meows.py [-h] [-n N]
meows.py: error: argument -n: invalid int value: 'dog'
```

## Unpacking: one star and two

We have seen **unpacking** one value into several variables before:

```python
first, _ = input("What's your name? ").split(" ")
print(f"hello, {first}")
```

```text
$ python unpack.py
What's your name? David Malan
hello, David
```

`split` returns a list of two items and the comma unpacks it into two
variables. We don't use the last name, so we named it `_`. Unpacking has two
forms that also help when calling a function. In the world of Harry Potter a
Galleon is 17 Sickles and a Sickle is 29 Knuts; a function that works out the
value of a vault in Knuts, `unpack.py`:

```python
def total(galleons, sickles, knuts):
    return (galleons * 17 + sickles) * 29 + knuts


print(total(100, 50, 25), "Knuts")
```

```text
$ python unpack.py
50775 Knuts
```

If the coins are in a list, passing the items one by one is long-winded and
error-prone:

```python
def total(galleons, sickles, knuts):
    return (galleons * 17 + sickles) * 29 + knuts


coins = [100, 50, 25]
print(total(coins[0], coins[1], coins[2]), "Knuts")
```

Passing the list as it is does not work; `galleons` becomes the list itself
and the other two are left empty:

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

A **single star** in front of the list unpacks it: `total(*coins)` is the
same as writing `total(100, 50, 25)`.

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

The number of items must match the number of parameters; unpacking a list of
four gives `TypeError: total() takes 3 positional arguments but 4 were
given`.

We can also pass the arguments by name; then the order does not matter:

```python
def total(galleons, sickles, knuts):
    return (galleons * 17 + sickles) * 29 + knuts


print(total(galleons=100, sickles=50, knuts=25), "Knuts")
```

Pairs of names and values bring a dictionary to mind. A **double star** in
front of a dictionary unpacks it into `key=value` arguments:

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

`total(**coins)` means exactly `total(galleons=100, sickles=50, knuts=25)`.
If the dictionary has a key the function does not know, it fails:

```text
$ python unpack.py
Traceback (most recent call last):
  File "unpack.py", line 6, in <module>
    print(total(**coins), "Knuts")
          ~~~~~^^^^^^^^^
TypeError: total() got an unexpected keyword argument 'pennies'
```

## Any number of arguments: args and kwargs

The stars are also used when **defining** a function, this time the other way
round: to gather scattered arguments. A function that takes any number of
arguments like this is called **variadic**.

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

- `*args` gathers all positional arguments in a **tuple**.
- `**kwargs` gathers all named (keyword) arguments in a **dictionary**.
- `args` and `kwargs` are only a convention; the stars are what matter.
- `(5,)` is a tuple of one item: the trailing comma sets it apart from a
  plain number.

`print`, which we have used for weeks, is such a function. Its signature in
the documentation is `print(*objects, sep=' ', end='\n', ...)`: that is why
`print()`, `print("hello")` and `print("hello", "world")` are all valid.

## map

A program that "yells" the words it is given in capital letters, `yell.py`.
First it takes a list:

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

The list was printed as it is, with its square brackets and quotes. Unpacking
helps here too: `print(*uppercased)` passes the items to `print` as separate
arguments.

```text
$ python yell.py
THIS IS CS50
```

It is more natural to call `yell` with any number of arguments, like `print`,
rather than with a list; with `*words`:

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

One of Python's built-in functions removes the loop and the `append`:
**map**. `map(function, sequence)` applies (maps) the function to every item
of the sequence.

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

There are no parentheses after `str.upper`: we are not **calling** the
function, we are **handing it** to `map`; `map` calls it on each word. Passing
a function to another function like a value is a feature of **functional
programming**; `sorted(..., key=...)` in the File I/O week was like this too.

`map` does not return a list but a `map` object that computes the results as
they are asked for, and it can be used up only once:

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

If you need a list, `list(map(...))`.

## List comprehensions

There is another very common way to write the same thing, considered
"Pythonic": the **list comprehension**. Inside square brackets, without
writing a loop, you say in one line how a list is built:

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

It reads left to right: "`word.upper()` for each `word` in `words`". A
condition can be added at the end of a comprehension too. The names of the
Gryffindor students, `gryffindors.py`:

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

The `if` part takes into the list only the items that meet the condition. The
line grew long, so we moved the square brackets onto their own lines; it is
easier to read.

## filter

The functional way of doing the same filtering is **filter**:
`filter(function, sequence)` calls the function on each item and keeps only
the items for which it returns `True`. `map` **transforms** every item,
`filter` **drops** some.

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

`is_gryffindor` is used only here; instead of naming it we can write an
anonymous `lambda` function. And to sort, `sorted(..., key=lambda ...)` from
the File I/O week:

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

## Dictionary comprehensions

This time we only have the names, and we want to build a dictionary for each
student. With a loop:

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

The same list in one line with a list comprehension:

```python
students = ["Hermione", "Harry", "Ron"]

gryffindors = [{"name": student, "house": "Gryffindor"} for student in students]

for gryffindor in gryffindors:
    print(gryffindor)
```

But maybe a list of dictionaries is not needed: a **single** dictionary whose
keys are the students' names and whose values are their houses is enough. The
syntax that builds it is the **dictionary comprehension**: curly braces
instead of square ones, with `key: value` inside.

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

Let's print the students with a rank number. With `range` and `len`:

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

People don't count from zero, so we wrote `i + 1`. **enumerate** gives two
things on each pass over a sequence: the current position (from zero) and the
item at that position. No `range`, `len` or `students[i]` needed:

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

If you want to start counting from one, `enumerate(students, start=1)`.

## Generators and yield

Counting sheep when you can't sleep, `sleep.py`. One more sheep on each line:

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

Let's apply what we've learned and move the part that makes the sheep into
its own function; instead of printing, it returns the whole flock in a list,
so it can be tested:

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

In the lecture David Malan runs this with 10,000 sheep without trouble; with
a million, though, the program waits without printing anything and in the end
the operating system **kills** it. `sheep` tries to build all million rows in
memory **at once**, and there isn't enough memory. On this computer we
measured the peak memory with 2,000 sheep:

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

Even with 2,000 sheep the list takes megabytes, and it grows fast with the
number of rows. The solution is to turn `sheep` into a **generator**: `yield`
instead of `return`.

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

`yield` hands out a value but does not end the function; the function
**pauses** at that point and remembers where it was. When the loop in `main`
asks for the next value, it carries on from there. So at any moment there is
only one row of sheep in memory; with a million, the output starts right away.
That is why the generator's peak memory in the measurement above is almost
zero.

Calling a generator function does not run its body right away; it returns a
**generator object**. The loop asks it for values one at a time with `next`;
when there are none left, `StopIteration` comes, and `for` takes that as
"done":

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

Objects like this that hand out values one at a time are called
**iterators**.

## To finish

At the end of the video David Malan closes the course with a text-to-speech
library (pyttsx3) that reads out what you type, together with `cowsay`.
pyttsx3 is not installed in Odyssey; we don't run that program here.

None of this week's tools is required; whatever you do with them you can also
do with the tools of the earlier weeks. But you will meet them often in other
people's code, and they let you solve the same problems in shorter, more
readable ways.

## Summary

- Sets: `set()`, `add`, each value once; empty `{}` is a dictionary
- `global` to change a global variable; often a class is tidier
- Constants in capital letters; Python does not protect them
- Type hints `n: int`, `-> str`; Python does not check them, mypy does
- Docstring: `"""..."""` on the first line of the body
- argparse: `add_argument("-n", default=1, type=int, help=...)`, `-h`
- Unpacking: `f(*list)`, `f(**dict)`; gathering: `def f(*args, **kwargs)`
- `map` transforms, `filter` drops; list and dictionary comprehensions
- `enumerate`: position and item together
- Generators: `yield` hands out values one at a time without holding all the
  data in memory

---

*This section is translated and adapted from the lecture notes of week 9 of Harvard University's [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/); examples and exercises were changed. The original and this adaptation are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Harvard does not endorse this adaptation.*
