Most mistakes with classes come from the same few places. They are all here.

## 1. Forgetting `self.`

```python
class Student:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return "hello " + name
```

```
NameError: name 'name' is not defined
```

There is no free variable called `name`. That value lives on the object, and
you reach it with `self.name`.

Rule: **write `self.` every time you reach the object's data inside a
method.**

## 2. Forgetting `self.` inside `__init__`

This one is sneakier, because it **raises no error**:

```python
class Student:
    def __init__(self, name):
        name = name          # no self.
```

That line does nothing: it assigns the local parameter to itself, and it
disappears when the function ends. Then:

```python
ada = Student("Ada")
print(ada.name)
```

```
AttributeError: 'Student' object has no attribute 'name'
```

The error appears far away from `__init__`, not in it. You start looking in
the wrong place.

## 3. Leaving out the `self` parameter

```python
class Student:
    def greet():
        return "hello"


Student().greet()
```

```
TypeError: Student.greet() takes 0 positional arguments but 1 was given
```

The message is confusing: "takes 0 arguments but one was given." The argument
given is the object itself — Python passes it automatically.

The fix: `def greet(self):`

## 4. A shared class attribute

This trap deserves to be at the top of the list. It raises no error and is
very hard to find:

```python
class Basket:
    items = []                    # at class level

    def add(self, item):
        self.items.append(item)


first = Basket()
second = Basket()

first.add("apple")
print(second.items)
```

```
['apple']
```

You added nothing to the `second` basket, yet there is an apple in it. The
reason: `items` belongs to the class, not to the objects. **Every object
shares the same list.**

The right way is to build the list inside `__init__`:

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h5>SHARED — WRONG</h5>
<pre><code>class Basket:
    items = []</code></pre>
    </div>
    <div class="ok">
      <h5>PER OBJECT — RIGHT</h5>
<pre><code>class Basket:
    def __init__(self):
        self.items = []</code></pre>
    </div>
  </div>
  <figcaption>The left-hand list is created once, when the class is defined. The right-hand one is created afresh every time an object is built.</figcaption>
</figure>

A class attribute is not wrong in itself — but it is not used for something
**mutable** (a list, a dictionary). It suits constants:

```python
class Circle:
    PI = 3.14159        # the same for everyone, never changes
```

## 5. Printing inside `__str__`

```python
class Student:
    def __str__(self):
        print(self.name)      # wrong
```

```python
print(Student("Ada"))
```

```
Ada
None
```

Two lines of output: one from the `print` inside `__str__`, and one `None`
because `__str__` returned nothing.

`__str__` **returns** a string:

```python
    def __str__(self):
        return self.name
```

## 6. Comparing objects with `==`

```python
a = Student("Ada", 90)
b = Student("Ada", 90)

print(a == b)
```

```
False
```

They carry the same data, but by default Python asks "is this the same
object", not "are these the same values". They are two separate objects.

If you want comparison by value, you have to write `__eq__`:

```python
    def __eq__(self, other):
        return self.name == other.name and self.grade == other.grade
```

## 7. Not calling `super().__init__()`

```python
class Shape:
    def __init__(self, name):
        self.name = name


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius        # super was never called


print(Circle(5).name)
```

```
AttributeError: 'Circle' object has no attribute 'name'
```

When a subclass writes its own `__init__`, the parent's does **not run on its
own.** You have to call it:

```python
    def __init__(self, radius):
        super().__init__("circle")
        self.radius = radius
```

If the subclass writes no `__init__` at all, the parent's is used as it is and
there is no problem.

## 8. Putting a stateless function inside a class

```python
class MathHelper:
    def add(self, a, b):
        return a + b


MathHelper().add(2, 3)
```

This class remembers nothing. Every time you build an empty object and call
its single method. That is not a class, it is a function in fancy dress:

```python
def add(a, b):
    return a + b
```

The test: **if nothing is written with `self.`, it should not be a class.**

## Summary

| Trap | How it shows up |
|---|---|
| Forgetting `self.` in a method | `NameError` |
| Forgetting `self.` in `__init__` | An `AttributeError` much later |
| Leaving out the `self` parameter | "takes 0 positional arguments" |
| A list at class level | Objects share the data |
| `print` inside `__str__` | An extra `None` is printed |
| Comparing objects with `==` | `False` even for identical data |
| No `super().__init__()` | The parent's data is never set up |
| A stateless class | Needless complexity |
