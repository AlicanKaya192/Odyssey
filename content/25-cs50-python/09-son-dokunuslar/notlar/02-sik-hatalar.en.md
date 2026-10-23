The most common mistakes with this week's tools and their messages (measured
on this computer with Python 3.14). Read the **last line** of an error message
first.

## Writing {} for an empty set

Curly braces are used for both sets and dictionaries; **empty** curly braces
are a dictionary:

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

An empty set is written `set()`.

## Indexing into a set

A set has no order, so it has no "item zero" either:

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

To go through it in order, `for house in sorted(houses):`; to look for a
particular value, `in`.

## Changing a global variable without global

When a name is assigned to inside a function, it counts as local; reading
works, `+=` does not:

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

Either write `global balance` at the start of the function or keep the value
in an object (`self._balance`).

## Relying on a type hint to protect you

A hint does not make Python do anything; a value of the wrong type still gets
into the function and the error comes out inside it:

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

To catch this mistake before the program runs, run mypy on the code; a value
that comes from the user you still check yourself.

## Passing map a function that is already called

`map` is given the function itself; the parentheses call it right away, with
no argument:

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

The right way is `map(str.upper, words)`.

## Going through a generator twice

`map`, `filter` and generators hand out their values once; on the second pass
nothing is left, and there is no error either:

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

If you need the values more than once, put them in a list once with
`list(...)`, or call the generator again: `sum(evens(7))`.

## Getting the number of unpacked items wrong

`*` makes each item of the list an argument; if there are more or fewer items
than parameters, a `TypeError`:

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

A list of four items also gives `TypeError: total() takes 3 positional
arguments but 4 were given`. If a dictionary has a key the function does not
know: `TypeError: total() got an unexpected keyword argument 'pennies'`.

## A list as a default value

A default value is created **once, when the function is defined**. A mutable
value like a list is shared by every call:

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

Make the default `None` and build the list inside the function:

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
