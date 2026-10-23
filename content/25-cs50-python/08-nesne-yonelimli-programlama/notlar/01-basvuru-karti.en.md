Everything from Week 8 on one page.

## Tuples, lists, dictionaries

| Syntax | What it does |
|---|---|
| `return name, house` | returns a tuple (the comma builds the tuple) |
| `name, house = get_student()` | unpacks the tuple into two variables |
| `(a, b)` / `[a, b]` | tuple (immutable) / list (mutable) |
| `t[0] = x` | a `TypeError` with a tuple |
| `{"name": n, "house": h}` | dictionary: every value has a name |

## Classes and objects

| Syntax | What it does |
|---|---|
| `class Student:` | a new type (class); the name starts with a capital |
| `student = Student("Harry", "Gryffindor")` | creates an object (instance); a constructor call |
| `def __init__(self, name, house):` | initializes the object; Python calls it automatically |
| `self.name = name` | an instance variable (attribute) |
| `student.name` | reads the attribute |
| `raise ValueError("Invalid house")` | raises an error for an invalid value |
| `def __str__(self): return ...` | `print(student)` and `str(student)` use it |
| `def charm(self): ...` | a method of your own; the first parameter is `self` |

## Properties

```python
@property
def house(self):          # getter: student.house
    return self._house

@house.setter
def house(self, house):   # setter: student.house = ...
    if house not in HOUSES:
        raise ValueError("Invalid house")
    self._house = house
```

- The value is in `self._house`; it cannot have the same name as the
  property.
- In `__init__`, `self.house = house` (no underscore): the assignment goes
  through the setter.
- The underscore is a convention, not a lock: `student._house = ...` is not
  stopped.

## Class level

| Syntax | What it does |
|---|---|
| `houses = [...]` (in the class body) | a class variable: all objects share it |
| `@classmethod` + `def sort(cls, name):` | a class method; `Hat.sort("Harry")` |
| `return cls(name, house)` | creates an object from inside a class method |
| `@staticmethod` | a method that takes neither the object nor the class |

## Inheritance

| Syntax | What it does |
|---|---|
| `class Student(Wizard):` | `Student` is a subclass of `Wizard` |
| `super().__init__(name)` | calls the superclass's `__init__` |
| `isinstance(student, Wizard)` | is the object of this class (or a subclass) |
| `class HouseError(ValueError): ...` | an exception of your own, derived from an existing one |

## Operator overloading

| Method | Operator |
|---|---|
| `__add__(self, other)` | `a + b` |
| `__sub__(self, other)` | `a - b` |
| `__eq__(self, other)` | `a == b` |
| `__lt__(self, other)` | `a < b` |
| `__str__(self)` | `str(a)`, `print(a)` |

## Built-in types

`int`, `str`, `list` and `dict` are classes too: `type(50)` →
`<class 'int'>`. `"hi".lower()` is a method of a `str` object.
