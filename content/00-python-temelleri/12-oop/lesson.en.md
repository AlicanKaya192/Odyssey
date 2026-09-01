# Object-Oriented Programming

You want to hold a student's name, grade and city. With the tools you have
today you would do it like this:

```python
student = {"name": "Ada", "grade": 90, "city": "London"}


def is_passing(record):
    return record["grade"] >= 50


print(is_passing(student))
```

It works. But there are three problems:

- The `student` dictionary and the `is_passing` function are **not tied
  together.** Pass a different dictionary by accident and you get a
  `KeyError`.
- If you misspell a key (`"grades"`), the error only shows up at run time.
- Once there are a hundred students, there is no way to be sure they all carry
  the same keys.

A **class** solves all three at once: it gathers the data and the functions
that work on that data into a single place.

## Your first class

```python
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def is_passing(self):
        return self.grade >= 50


ada = Student("Ada", 90)

print(ada.name)
print(ada.is_passing())
```

```
Ada
True
```

<figure class="fig anat">
  <div class="sig">class <u class="m1">Student</u>:
    def <u class="m2">__init__</u>(<u class="m3">self</u>, name, grade):
        <u class="m4">self.name</u> = name</div>
  <ul class="legend">
    <li class="m1"><b>The class name</b> — starts with a capital letter. It is a template, not an object yet.</li>
    <li class="m2"><b>The constructor</b> — runs the moment you write <code>Student(...)</code>. Its name is fixed.</li>
    <li class="m3"><b>self</b> — the object being built. It is always the first parameter.</li>
    <li class="m4"><b>The object's attribute</b> — anything written with <code>self.</code> stays on the object.</li>
  </ul>
</figure>

## The difference between a class and an object

`Student` is a **template**. You can produce as many objects from it as you
like, and each carries its own data:

```python
ada = Student("Ada", 90)
brian = Student("Brian", 40)

print(ada.grade)
print(brian.grade)
```

```
90
40
```

<figure class="fig">
  <div class="flow">
    <span class="node acc"><b>Student</b><br>the template</span>
    <span class="arrow">→</span>
    <span class="node"><b>ada</b><br>name: Ada<br>grade: 90</span>
    <span class="node"><b>brian</b><br>name: Brian<br>grade: 40</span>
  </div>
  <figcaption>One template, two objects. Both carry the same methods but their data is separate; changing one does not affect the other.</figcaption>
</figure>

The template is called a **class**, and everything produced from it is an
**object**.

## What is `self`, really?

This is the part that confuses people most, but it is simple.

When you call a method, Python passes the object to it **as the first
argument**. So these two are the same thing:

```python
ada.is_passing()
Student.is_passing(ada)
```

`self` is the name that passed-in object goes by inside the method. That is
why:

- The first parameter of every method has to be `self`.
- You write `self.grade` to reach the object's data, not a bare `grade`.

Forgetting `self.` inside a method is the most common mistake:

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h5>WITHOUT self</h5>
<pre><code>def is_passing(self):
    return grade &gt;= 50</code></pre>
    </div>
    <div class="ok">
      <h5>WITH self</h5>
<pre><code>def is_passing(self):
    return self.grade &gt;= 50</code></pre>
    </div>
  </div>
  <figcaption>The left-hand one raises a <code>NameError</code>: there is no free variable called <code>grade</code>; that value lives on the object.</figcaption>
</figure>

## An object's state can change

Methods do not only calculate; they can change the object's data too:

```python
class Counter:
    def __init__(self):
        self.count = 0

    def increase(self):
        self.count = self.count + 1
        return self.count


clicks = Counter()
clicks.increase()
clicks.increase()

print(clicks.count)
```

```
2
```

This could have been done with a dictionary, but here is the difference: the
`Counter` object manages its own counter. There is no way to write the wrong
key from outside.

## Printing an object: `__str__`

If you try to print an object directly:

```python
ada = Student("Ada", 90)
print(ada)
```

```
<__main__.Student object at 0x000001F3A2B4C110>
```

Unreadable. The `__str__` method fixes that:

```python
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __str__(self):
        return self.name + ": " + str(self.grade)


print(Student("Ada", 90))
```

```
Ada: 90
```

`__str__` **returns** a string, it does not print. Writing `print` inside it
is a common mistake.

## Inheritance

When two classes have something in common, you can write the common part once
and hand it down:

```python
class Shape:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return self.name + " has area " + str(self.area())


class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("rectangle")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)
        self.name = "square"


print(Rectangle(3, 4).describe())
print(Square(5).describe())
```

```
rectangle has area 12
square has area 25
```

There are two pieces:

- `class Rectangle(Shape):` — this says "a Rectangle is a Shape". Every method
  of `Shape` exists on `Rectangle` too.
- `super().__init__(...)` — calls the parent class's constructor. Leave it out
  and `self.name` is never set up.

Note: the `Shape` class itself has no `area` method, yet `describe` calls it.
That is deliberate — every shape works out its area differently, and the
subclasses fill that in.

## When should you write a class?

A class is not the answer to every problem. Where it helps:

- **When data and behaviour belong together.** A student's grade and the
  question "did they pass" belong in the same place.
- **When many things will be produced from the same shape.** A hundred
  students, all from one template.
- **When an object has a state that changes over time.** A counter, a basket,
  a connection.

Where it is unnecessary:

- **When it carries a single value.** That is what a variable is for.
- **When it only calculates.** An operation with no state is a function, not a
  class. `def average(values):` does not belong inside a class.
- **When it only holds data with no behaviour.** A dictionary may be enough.

The test: **does the object have something it needs to remember?** If it does,
write a class; if not, a function.

## Summary

- A class is a template; everything produced from it is an object.
- `__init__` runs while the object is being built and puts the starting data
  in place.
- The first parameter of every method is `self`, the object itself.
- You reach the object's data with `self.name`; forgetting `self.` raises a
  `NameError`.
- Methods can read the object's data and **change** it.
- `__str__` decides how the object looks when printed; it returns a string
  rather than printing one.
- `class Child(Parent):` is inheritance; `super().__init__(...)` calls the
  parent's constructor.
- For an operation with no state, write a function rather than a class.
