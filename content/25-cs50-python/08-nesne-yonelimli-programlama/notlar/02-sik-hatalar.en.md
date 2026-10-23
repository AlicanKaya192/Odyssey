The most common mistakes when working with classes, and their messages
(measured in Python 3.14 on this computer). Read the **last line** of an
error message first.

## Forgetting self

A method's first parameter is always the object itself. If it is forgotten,
Python puts the object into `name` and the number of arguments does not
match:

```python
class Student:
    def __init__(name, house):
        self.name = name
        self.house = house


student = Student("Harry", "Gryffindor")
```

```text
$ python student.py
Traceback (most recent call last):
  File "student.py", line 7, in <module>
    student = Student("Harry", "Gryffindor")
TypeError: Student.__init__() takes 2 positional arguments but 3 were given
```

"takes 2 but 3 were given": your two arguments plus the object Python passes
automatically. The fix is `def __init__(self, name, house):`.

## Assigning without self.

`name = name` only assigns to the local variable inside the function;
nothing is written to the object:

```python
class Student:
    def __init__(self, name, house):
        name = name
        house = house


student = Student("Harry", "Gryffindor")
print(student.name)
```

```text
$ python student.py
Traceback (most recent call last):
  File "student.py", line 8, in <module>
    print(student.name)
          ^^^^^^^^^^^^
AttributeError: 'Student' object has no attribute 'name'
```

Every value to keep in the object is written as `self.name = name`.

## A variable with the property's name

The getter returns `self.house`; but `self.house` is the getter itself. The
setter calls itself with `self.house = ...` too, and this goes on forever:

```python
class Student:
    def __init__(self, house):
        self.house = house

    @property
    def house(self):
        return self.house

    @house.setter
    def house(self, house):
        self.house = house


student = Student("Gryffindor")
```

```text
$ python student.py
Traceback (most recent call last):
  File "student.py", line 14, in <module>
    student = Student("Gryffindor")
  File "student.py", line 3, in __init__
    self.house = house
    ^^^^^^^^^^
  File "student.py", line 11, in house
    self.house = house
    ^^^^^^^^^^
  File "student.py", line 11, in house
    self.house = house
    ^^^^^^^^^^
  File "student.py", line 11, in house
    self.house = house
    ^^^^^^^^^^
  [Previous line repeated 995 more times]
RecursionError: maximum recursion depth exceeded
```

Keep the value in an instance variable with a different name: `self._house`.

## print in __str__

`__str__` must **return** a string. If it prints and returns nothing, it
returns `None`:

```python
class Student:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        print(f"Student {self.name}")


student = Student("Harry")
print(student)
```

```text
$ python student.py
Student Harry
Traceback (most recent call last):
  File "student.py", line 10, in <module>
    print(student)
    ~~~~~^^^^^^^^^
TypeError: __str__ returned non-string (type NoneType)
```

## A class method without its decorator

Without `@classmethod`, `sort` is an ordinary method and `Hat.sort("Harry")`
puts `"Harry"` into `cls`; `name` is missing:

```python
class Hat:
    houses = ["Gryffindor", "Slytherin"]

    def sort(cls, name):
        print(name, "is in", cls.houses[0])


Hat.sort("Harry")
```

```text
$ python hat.py
Traceback (most recent call last):
  File "hat.py", line 8, in <module>
    Hat.sort("Harry")
    ~~~~~~~~^^^^^^^^^
TypeError: Hat.sort() missing 1 required positional argument: 'name'
```

## Forgetting super().__init__

If the subclass has its own `__init__`, the superclass's is not called
automatically; the code that assigns the name never runs:

```python
class Wizard:
    def __init__(self, name):
        self.name = name


class Student(Wizard):
    def __init__(self, name, house):
        self.house = house


student = Student("Harry", "Gryffindor")
print(student.name)
```

```text
$ python wizard.py
Traceback (most recent call last):
  File "wizard.py", line 12, in <module>
    print(student.name)
          ^^^^^^^^^^^^
AttributeError: 'Student' object has no attribute 'name'
```

At the start of the subclass's `__init__`, `super().__init__(name)`.

## A shared class list

A variable in the class body is a variable **shared by all objects**. If it
is a mutable value like a list, adding to it through one object adds it for
everyone:

```python
class Student:
    courses = []

    def __init__(self, name):
        self.name = name


harry = Student("Harry")
hermione = Student("Hermione")
harry.courses.append("Potions")
print(hermione.courses)
```

```text
$ python student.py
['Potions']
```

If every object should have its own list, the list is created in
`__init__`:

```python
class Student:
    def __init__(self, name):
        self.name = name
        self.courses = []


harry = Student("Harry")
hermione = Student("Hermione")
harry.courses.append("Potions")
print(hermione.courses)
```

```text
$ python student.py
[]
```

## Trying to change a tuple

`return name, house` returns a tuple; `student[1] = ...` gives `TypeError:
'tuple' object does not support item assignment`. If it will change, a list,
a dictionary or a class.
