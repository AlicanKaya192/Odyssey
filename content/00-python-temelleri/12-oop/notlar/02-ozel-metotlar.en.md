# Special Methods

Methods whose names start and end with two underscores are called **special
methods**: `__init__`, `__str__`, `__len__`. You do not call them directly;
Python calls them for you in particular situations.

In conversation people say "dunder" — short for *double underscore*.

## How do they work?

What you write is on the left; what Python calls is on the right:

| What you write | What Python calls |
|---|---|
| `Student("Ada")` | `__init__` |
| `print(ada)` | `__str__` |
| `len(basket)` | `__len__` |
| `a == b` | `__eq__` |
| `a < b` | `__lt__` |
| `item in basket` | `__contains__` |
| `basket[0]` | `__getitem__` |
| `for x in basket` | `__iter__` |

In other words, you are **teaching** Python's built-in operations about your
own class.

## `__init__` — the constructor

You already know this one. It runs while the object is being built and puts
the starting data in place.

```python
class Basket:
    def __init__(self):
        self.items = []
```

It returns nothing. Writing `return` raises an error.

## `__str__` — how it looks to a person

```python
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __str__(self):
        return self.name + " (" + str(self.grade) + ")"


print(Student("Ada", 90))
```

```
Ada (90)
```

It **returns** a string. Writing `print` inside it is a common mistake.

### The difference from `__repr__`

`__str__` is for people, `__repr__` is for developers:

```python
class Student:
    def __str__(self):
        return self.name

    def __repr__(self):
        return "Student(" + repr(self.name) + ")"


ada = Student("Ada")

print(ada)
print([ada])
```

```
Ada
[Student('Ada')]
```

Note: when an object is **inside a list**, `__repr__` is used rather than
`__str__`. That is why, if you wrote only `__str__`, lists still show
`<__main__.Student object at ...>`.

If you are only going to write one, write `__repr__` — when `__str__` is not
defined, Python uses `__repr__` in its place. The reverse is not true.

## `__len__` — length

```python
class Basket:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def __len__(self):
        return len(self.items)


basket = Basket()
basket.add("apple")
basket.add("bread")

print(len(basket))
```

```
2
```

`__len__` must return a **whole number**. Returning a string or a decimal
raises a `TypeError`.

It has a side effect: once `__len__` is defined, the object gains a truth
value too. When the length is zero the object counts as `False`:

```python
if basket:
    print("not empty")
```

## `__eq__` — equality

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


print(Point(1, 2) == Point(1, 2))
```

```
True
```

Without it the answer would be `False` — by default Python asks "is this the
same object".

**Watch out:** the moment you write `__eq__`, your object can no longer be a
dictionary key or a set element. If you want it to be, you have to write
`__hash__` as well:

```python
    def __hash__(self):
        return hash((self.x, self.y))
```

## `__contains__` — the `in` operator

```python
class Basket:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def __contains__(self, item):
        return item in self.items


basket = Basket()
basket.add("apple")

print("apple" in basket)
print("bread" in basket)
```

```
True
False
```

## How many should you write?

Not all of them. In practice the order is:

- **`__init__`** — in almost every class.
- **`__repr__`** — very useful while debugging, worth writing.
- **`__str__`** — when the object will be shown to a user.
- **`__eq__`** — when you will compare objects by value.
- **`__len__`, `__contains__`, `__getitem__`** — when your object is going to
  behave like a **container**.

The rest are advanced and rarely needed.

## Where will you meet them?

They are everywhere in Python. `len("abc")` works because the `str` class has
a `__len__`. `[1, 2] + [3]` works because the `list` class has an `__add__`.

When you move on to data science you will see pandas write `table["score"]` —
that is `__getitem__`. So what you are learning here is how libraries
themselves are written.
