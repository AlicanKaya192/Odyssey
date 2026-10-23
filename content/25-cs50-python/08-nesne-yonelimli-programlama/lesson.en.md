# Object-Oriented Programming

Week 8 of CS50 Python. You can watch the lecture in the **Video** tab; this
page is its written form. Programming has different **paradigms**
(approaches) to solving problems. So far we have mostly written
**procedural** code: functions, step by step from top to bottom. When we
passed functions to other functions with `lambda`, we touched on
**functional** programming too. This week, a third one: **object-oriented
programming** (OOP). It is a pretty compelling solution to problems you run
into as programs get longer, larger and more complicated.

## Returning more than one value: tuples

A program that gets the name and house of a student from the world of Harry
Potter, `student.py`. We want to get a student with a single function; but
we have two values. In Python you can return both with a comma, and unpack
them into two variables with a comma on the way back:

```python
def main():
    name, house = get_student()
    print(f"{name} from {house}")


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return name, house


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Harry from Gryffindor
```

What comes back is actually **one** value: a **tuple**. A tuple is a
collection of values similar to a list; a comma on its own builds a tuple,
and you can write it explicitly with parentheses: `(name, house)`. You can
keep the tuple in one variable without unpacking it, and look inside it by
position as with a list:

```python
def main():
    student = get_student()
    print(f"{student[0]} from {student[1]}")


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return (name, house)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Harry from Gryffindor
```

## Tuples are immutable

In the films Padma is in Gryffindor, in the books in Ravenclaw. If the user
types Padma, let's fix her house:

```python
def main():
    student = get_student()
    if student[0] == "Padma":
        student[1] = "Ravenclaw"
    print(f"{student[0]} from {student[1]}")


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return (name, house)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Padma
House: Gryffindor
Traceback (most recent call last):
  File "student.py", line 15, in <module>
    main()
    ~~~~^^
  File "student.py", line 4, in main
    student[1] = "Ravenclaw"
    ~~~~~~~^^^
TypeError: 'tuple' object does not support item assignment
```

A tuple is **immutable**: once created, no position in it can be assigned a
new value. That is not a bug; it is how tuples are designed. If a value
should not change, not keeping it in a type that can change prevents
mistakes you or a colleague might make later.

If you do want to change it, use a list: with just `return [name, house]` in
`get_student`, the code works.

```text
$ python student.py
Name: Padma
House: Gryffindor
Padma from Ravenclaw
```

When **creating** a value, square brackets mean a list and parentheses a
tuple; but when **looking inside**, both use square brackets: `student[0]`.

## Dictionaries

You have to remember that `student[0]` is the name and `student[1]` the
house; with more fields this gets confusing. A dictionary gives each value a
name:

```python
def main():
    student = get_student()
    if student["name"] == "Padma":
        student["house"] = "Ravenclaw"
    print(f"{student['name']} from {student['house']}")


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return {"name": name, "house": house}


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Padma
House: Gryffindor
Padma from Ravenclaw
```

Inside the f-string we wrote the keys in single quotes, with double quotes
outside. In the Python of the lecture, using double quotes inside as well
was a syntax error; **since Python 3.12** an f-string may use the same quotes
inside (measured in 3.14 on this computer):

```python
student = {"name": "Harry", "house": "Gryffindor"}
print(f"{student["name"]} from {student["house"]}")
```

```text
$ python student.py
Harry from Gryffindor
```

Even so, keeping the two kinds of quotes apart makes it easier to read.

## Classes

Tuples, lists and dictionaries are general-purpose types. If Python had a
`Student` type, we would not need this discussion. Instead, Python gives us
a way to create our own type: a **class**. A class is a **blueprint**, a
**mold**: every value you create with that mold has the same structure.

```python
class Student:
    ...


def main():
    student = get_student()
    print(f"{student.name} from {student.house}")


def get_student():
    student = Student()
    student.name = input("Name: ")
    student.house = input("House: ")
    return student


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Harry from Gryffindor
```

- `class Student:` defines a new type. By convention, class names start with
  a capital letter. `...` is a valid placeholder that says "I'll write the
  body later".
- `Student()` creates an **object** of this class. An object is also called
  an **instance** of the class: if the class is the blueprint of a house, the
  object is one particular house built from it.
- `student.name = ...` adds an **attribute** to the object. The dot means
  "this thing inside that thing", as with modules.

## __init__ and self

Adding attributes one by one from outside is messy. Let's give the values
all at once when the object is created: `Student(name, house)`. For that, a
special method is written in the class. A **method** is a function inside a
class.

```python
class Student:
    def __init__(self, name, house):
        self.name = name
        self.house = house


def main():
    student = get_student()
    print(f"{student.name} from {student.house}")


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return Student(name, house)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Harry from Gryffindor
```

- `Student(name, house)` is a **constructor call**. Python first creates an
  empty object in memory, then automatically calls `__init__` to initialize
  it. The double underscores at the start and end are called **dunder**
  (double underscore).
- The first parameter of `__init__` is `self`: the object that was just
  created. You do not pass it when calling; Python does. `Student("Harry",
  "Gryffindor")` is called with two arguments, `__init__` takes three
  parameters.
- `self.name = name` stores the value inside that object. These variables
  inside an object are called **instance variables**.

This is where a class starts to differ from a dictionary: you can control
what goes in.

## Raising errors: raise

If the name is empty, or the house is not one of the four Hogwarts houses,
the student should not be created at all. Warning with `print` is not enough
(the program carries on), and `sys.exit` closes the whole program. Besides,
when `__init__` runs, the object already exists; it is too late to return
`None`. The right way is to **raise** an exception: so far we caught the
`ValueError`s Python raised; now we raise them ourselves.

```python
class Student:
    def __init__(self, name, house):
        if not name:
            raise ValueError("Missing name")
        if house not in ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            raise ValueError("Invalid house")
        self.name = name
        self.house = house


def main():
    student = get_student()
    print(f"{student.name} from {student.house}")


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return Student(name, house)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Harry from Gryffindor
```

If Harry types the address of the house he grew up in:

```text
$ python student.py
Name: Harry
House: Number Four, Privet Drive
Traceback (most recent call last):
  File "student.py", line 23, in <module>
    main()
    ~~~~^^
  File "student.py", line 12, in main
    student = get_student()
  File "student.py", line 19, in get_student
    return Student(name, house)
  File "student.py", line 6, in __init__
    raise ValueError("Invalid house")
ValueError: Invalid house
```

With `raise ValueError("Invalid house")` we give the message too. The code
that creates the student can catch it, if it wants, with the usual
`try` / `except ValueError`.

## __str__

If we print the student directly:

```python
class Student:
    def __init__(self, name, house):
        if not name:
            raise ValueError("Missing name")
        if house not in ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            raise ValueError("Invalid house")
        self.name = name
        self.house = house


def main():
    student = get_student()
    print(student)


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return Student(name, house)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
<__main__.Student object at 0x...>
```

The default string representation tells the object's type and its place in
memory (`0x...`, different on every run). If you define the special method
**`__str__`**, Python calls it automatically whenever a function (like
`print`) wants to see your object as a string:

```python
class Student:
    def __init__(self, name, house):
        if not name:
            raise ValueError("Missing name")
        if house not in ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            raise ValueError("Invalid house")
        self.name = name
        self.house = house

    def __str__(self):
        return f"{self.name} from {self.house}"


def main():
    student = get_student()
    print(student)


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return Student(name, house)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Draco
House: Slytherin
Draco from Slytherin
```

(There is also `__repr__`: a representation for developers, usually more
detailed.)

## Methods of our own

Besides special methods, we can write our own. Students have a
**patronus**; let a `charm` method return an emoji to match it. The first
parameter of your own method is `self` too:

```python
class Student:
    def __init__(self, name, house, patronus):
        if not name:
            raise ValueError("Missing name")
        if house not in ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            raise ValueError("Invalid house")
        self.name = name
        self.house = house
        self.patronus = patronus

    def __str__(self):
        return f"{self.name} from {self.house}"

    def charm(self):
        match self.patronus:
            case "Stag":
                return "🐴"
            case "Otter":
                return "🦦"
            case "Jack Russell terrier":
                return "🐶"
            case _:
                return "🪄"


def main():
    student = get_student()
    print("Expecto Patronum!")
    print(student.charm())


def get_student():
    name = input("Name: ")
    house = input("House: ")
    patronus = input("Patronus: ")
    return Student(name, house, patronus)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Patronus: Stag
Expecto Patronum!
🐴
```

Draco, who has no patronus:

```text
$ python student.py
Name: Draco
House: Slytherin
Patronus: 
Expecto Patronum!
🪄
```

A class keeps not only the data (attributes) together but also the work done
with that data (methods).

## Properties

The checks in `__init__` only run when the object is **created**. Nothing
stops anyone from changing the attribute afterwards:

```python
class Student:
    def __init__(self, name, house):
        if not name:
            raise ValueError("Missing name")
        if house not in ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            raise ValueError("Invalid house")
        self.name = name
        self.house = house

    def __str__(self):
        return f"{self.name} from {self.house}"


def main():
    student = get_student()
    student.house = "Number Four, Privet Drive"
    print(student)


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return Student(name, house)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Harry from Number Four, Privet Drive
```

A **property** moves the checks into assignment too. Reading the attribute
goes through a **getter** method, assigning it through a **setter**:

```python
class Student:
    def __init__(self, name, house):
        self.name = name
        self.house = house

    def __str__(self):
        return f"{self.name} from {self.house}"

    # Getter
    @property
    def name(self):
        return self._name

    # Setter
    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Missing name")
        self._name = name

    @property
    def house(self):
        return self._house

    @house.setter
    def house(self, house):
        if house not in ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            raise ValueError("Invalid house")
        self._house = house


def main():
    student = get_student()
    student.house = "Number Four, Privet Drive"
    print(student)


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return Student(name, house)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Traceback (most recent call last):
  File "student.py", line 45, in <module>
    main()
    ~~~~^^
  File "student.py", line 34, in main
    student.house = "Number Four, Privet Drive"
    ^^^^^^^^^^^^^
  File "student.py", line 28, in house
    raise ValueError("Invalid house")
ValueError: Invalid house
```

- `@property` is a **decorator**: a function that changes the behavior of
  the function below it. Here it turns the `house` method into a getter;
  `student.house` now calls this method.
- `@house.setter` turns the second method of the same name into a setter;
  `student.house = ...` now calls it, and an invalid value raises a
  `ValueError`.
- The value itself is in `self._house`. If the instance variable were also
  named `house`, it would collide with the property; the convention is an
  underscore in front.
- In `__init__` we wrote `self.house = house`, without the underscore: that
  assignment goes through the setter too, so the check is in one place.

If the name is left empty, the check is again in a setter, but this time
while `__init__` runs:

```text
$ python student.py
Name: 
House: Gryffindor
Traceback (most recent call last):
  File "student.py", line 44, in <module>
    main()
    ~~~~^^
  File "student.py", line 33, in main
    student = get_student()
  File "student.py", line 40, in get_student
    return Student(name, house)
  File "student.py", line 3, in __init__
    self.name = name
    ^^^^^^^^^
  File "student.py", line 18, in name
    raise ValueError("Missing name")
ValueError: Missing name
```

Python has no **private** variables like languages such as Java. If someone
writes to the underscored variable directly, nothing stops them:

```python
class Student:
    def __init__(self, name, house):
        self.name = name
        self.house = house

    def __str__(self):
        return f"{self.name} from {self.house}"

    # Getter
    @property
    def name(self):
        return self._name

    # Setter
    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Missing name")
        self._name = name

    @property
    def house(self):
        return self._house

    @house.setter
    def house(self, house):
        if house not in ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            raise ValueError("Invalid house")
        self._house = house


def main():
    student = get_student()
    student._house = "Number Four, Privet Drive"
    print(student)


def get_student():
    name = input("Name: ")
    house = input("House: ")
    return Student(name, house)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Harry from Number Four, Privet Drive
```

The underscore is a **convention**: it means "don't touch this". If you
break things, that is on you.

## The types we know are classes too

`int`, `str`, `list` and `dict` were classes all along. `"hello".lower()`
calls a method of a `str` object, `list.append` a method of a `list` object.
`type` tells you the class of a value, `type.py`:

```python
print(type(50))
print(type("hello, world"))
print(type([]))
print(type({}))
```

```text
$ python type.py
<class 'int'>
<class 'str'>
<class 'list'>
<class 'dict'>
```

Python's built-in types start with a lowercase letter; for your own classes
the convention is a capital letter.

## Class methods and class variables

Let the sorting hat take a student's name and place them in a house,
`hat.py`. First the way we have done so far: create a `Hat` object and call
its method (`random.choice` picks a random house):

```python
import random


class Hat:
    def __init__(self):
        self.houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

    def sort(self, name):
        print(name, "is in", random.choice(self.houses))


hat = Hat()
hat.sort("Harry")
```

```text
$ python hat.py
Harry is in Hufflepuff
```

But there is only one sorting hat at Hogwarts; creating several hat objects
makes no sense. And the list of houses belongs not to a particular hat but
to the class itself:

```python
import random


class Hat:
    houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

    @classmethod
    def sort(cls, name):
        print(name, "is in", random.choice(cls.houses))


Hat.sort("Harry")
```

```text
$ python hat.py
Harry is in Ravenclaw
```

- `houses` is now a **class variable**: defined inside the class, without
  `self`; all objects share the same single copy.
- `@classmethod` makes a **class method**: it is called as `Hat.sort(...)`
  without creating an object. Its first parameter is not an object but the
  class itself; by convention `cls` (`class` is a keyword, so it cannot be
  used).
- The methods so far are **instance methods**: every method without a
  decorator is one.

The same idea tidies up the student program. `get_student` was about
students but lived outside the class; let everything about students live in
the class:

```python
class Student:
    def __init__(self, name, house):
        self.name = name
        self.house = house

    def __str__(self):
        return f"{self.name} from {self.house}"

    @classmethod
    def get(cls):
        name = input("Name: ")
        house = input("House: ")
        return cls(name, house)


def main():
    student = Student.get()
    print(student)


if __name__ == "__main__":
    main()
```

```text
$ python student.py
Name: Harry
House: Gryffindor
Harry from Gryffindor
```

`cls(name, house)` means "create an object of this class". `Student.get()`
can be called without creating an object; otherwise you would need a
student in order to get a student.

There is a third kind as well: a **static method**, with `@staticmethod`; it
takes neither the object nor the class. We don't use it in this course.

## Inheritance

Both students and professors have names, and in both the name must not be
empty. Instead of copying the same check into two classes, let's move the
common part into a superclass: both are wizards. `wizard.py`:

```python
class Wizard:
    def __init__(self, name):
        if not name:
            raise ValueError("Missing name")
        self.name = name


class Student(Wizard):
    def __init__(self, name, house):
        super().__init__(name)
        self.house = house


class Professor(Wizard):
    def __init__(self, name, subject):
        super().__init__(name)
        self.subject = subject


wizard = Wizard("Albus")
student = Student("Harry", "Gryffindor")
professor = Professor("Severus", "Defense Against the Dark Arts")

print(wizard.name)
print(student.name, student.house)
print(professor.name, professor.subject)
print(isinstance(student, Wizard), isinstance(student, Professor))
```

```text
$ python wizard.py
Albus
Harry Gryffindor
Severus Defense Against the Dark Arts
True False
```

- `class Student(Wizard):` says that `Student` **inherits** from `Wizard`.
  `Student` is a **subclass**, `Wizard` its **superclass**.
- `super().__init__(name)` calls the superclass's `__init__`: assigning and
  checking the name happens in `Wizard`, in one place. The subclass only adds
  what is its own (`house`, `subject`).
- `isinstance(student, Wizard)` is true: every student is a wizard.

Exceptions form a hierarchy too; let's print the superclasses of
`ValueError` in order, `exceptions.py`:

```python
for cls in ValueError.__mro__:
    print(cls.__name__)
```

```text
$ python exceptions.py
ValueError
Exception
BaseException
object
```

That is why `except Exception:` catches a `ValueError` as well. If you write
an exception of your own, you derive it from an existing one instead of
starting from scratch: `class HouseError(ValueError): ...`.

## Operator overloading

`+` does not always mean addition: it joins strings and lists. The type
itself decides that meaning, and for your own class you can decide it too:
**operator overloading**. Vaults at the Gringotts bank, `vault.py`; first we
add two vaults by hand:

```python
class Vault:
    def __init__(self, galleons=0, sickles=0, knuts=0):
        self.galleons = galleons
        self.sickles = sickles
        self.knuts = knuts

    def __str__(self):
        return f"{self.galleons} Galleons, {self.sickles} Sickles, {self.knuts} Knuts"


potter = Vault(100, 50, 25)
print(potter)

weasley = Vault(25, 50, 100)
print(weasley)

galleons = potter.galleons + weasley.galleons
sickles = potter.sickles + weasley.sickles
knuts = potter.knuts + weasley.knuts

total = Vault(galleons, sickles, knuts)
print(total)
```

```text
$ python vault.py
100 Galleons, 50 Sickles, 25 Knuts
25 Galleons, 50 Sickles, 100 Knuts
125 Galleons, 100 Sickles, 125 Knuts
```

If we write `potter + weasley` directly, Python does not know how to add two
vaults:

```python
class Vault:
    def __init__(self, galleons=0, sickles=0, knuts=0):
        self.galleons = galleons
        self.sickles = sickles
        self.knuts = knuts

    def __str__(self):
        return f"{self.galleons} Galleons, {self.sickles} Sickles, {self.knuts} Knuts"


potter = Vault(100, 50, 25)
weasley = Vault(25, 50, 100)
total = potter + weasley
```

```text
$ python vault.py
Traceback (most recent call last):
  File "vault.py", line 13, in <module>
    total = potter + weasley
            ~~~~~~~^~~~~~~~~
TypeError: unsupported operand type(s) for +: 'Vault' and 'Vault'
```

The special method `__add__` teaches it. When `a + b` is written, Python
calls `a.__add__(b)`: `self` is the operand on the left and, by convention,
`other` the one on the right.

```python
class Vault:
    def __init__(self, galleons=0, sickles=0, knuts=0):
        self.galleons = galleons
        self.sickles = sickles
        self.knuts = knuts

    def __str__(self):
        return f"{self.galleons} Galleons, {self.sickles} Sickles, {self.knuts} Knuts"

    def __add__(self, other):
        galleons = self.galleons + other.galleons
        sickles = self.sickles + other.sickles
        knuts = self.knuts + other.knuts
        return Vault(galleons, sickles, knuts)


potter = Vault(100, 50, 25)
weasley = Vault(25, 50, 100)

total = potter + weasley
print(total)
```

```text
$ python vault.py
125 Galleons, 100 Sickles, 125 Knuts
```

Many operators have special methods, like `__sub__` (`-`), `__eq__` (`==`)
and `__lt__` (`<`). New operators (new symbols) cannot be defined; you only
give meaning to the existing ones.

## Summary

- A tuple `(a, b)` is immutable, a list `[a, b]` mutable; a dictionary gives
  each value a name.
- `class`, object, instance, attribute; `__init__` and `self`
- `raise ValueError("...")`
- `__str__`, methods of your own
- `@property`, `@x.setter`, the underscore convention
- Class variables, `@classmethod` and `cls`
- Inheritance: `class Student(Wizard):`, `super().__init__(...)`
- Operator overloading: `__add__`

A class is not always necessary; in a short program a few functions do the
job. But gathering related data and functionality in a place that has a name
is one way to keep things organized as code grows.

---

*This section is translated and adapted from week 8 of Harvard University's [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) (lecture notes and problem set); examples and exercises were changed, and the problem set is checked by Odyssey, not by CS50's check50. The original and this adaptation are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Harvard does not endorse this adaptation.*
