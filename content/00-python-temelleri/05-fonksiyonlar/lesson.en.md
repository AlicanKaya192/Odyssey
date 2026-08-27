# Functions

Everything you have written so far ran once, top to bottom. When you needed the
same work done a second time, your only option was to copy the code. Functions
solve exactly that: you describe a job **once**, then call it as many times as
you like.

## Why do we need them?

Say you want to add two numbers:

```python
a = 5
b = 3
print(a + b)
```

Now you need to add two other numbers. You write the same lines again. Then once
more. That is three copies already — and if the way you add ever changes, you
have three places to fix.

A function removes that repetition. It also brings two more things: it gives the
code a **name** (`calculate_total` tells you what it does, three lines of code do
not) and it splits the program into **pieces**.

## Defining with def

```python
def add(a, b):
    return a + b
```

Line by line:

- `def` — "I am defining a new function".
- `add` — the function's name. This is what you call.
- `(a, b)` — the **parameters**. The values the function takes from outside.
- `:` — a colon after the header, just like in conditions and loops.
- The indented lines — the **body**. Only this part belongs to the function.

Defining does **not** run the function. It only says "such a thing exists". Run
the code above and nothing appears on screen.

## Calling

To run a function, write its name and open brackets:

```python
def add(a, b):
    return a + b

result = add(5, 3)
print(result)     # 8
```

The moment you write `add(5, 3)`, 5 goes into `a`, 3 goes into `b` and the body
runs. The values you put in the brackets are called **arguments**.

Define once, call as often as you want:

```python
print(add(5, 3))      # 8
print(add(10, 20))    # 30
print(add(-4, 4))     # 0
```

## return — handing the value back

`return` is what sends the result out of the function:

```python
def double(number):
    return number * 2

x = double(21)
print(x)     # 42
```

The moment `return` runs, the function **ends**. Lines below it never run:

```python
def test():
    return "first"
    return "second"     # never reached

print(test())     # first
```

If you write no `return`, the function returns `None`. That is not an error, it
is Python's way of saying "there is nothing to hand back":

```python
def greet(name):
    print("Hello,", name)

x = greet("Ada")
print(x)     # None
```

## return and print are not the same

This is where beginners get stuck most often. The two do completely different
jobs:

- **`print`** writes text **to the screen.** It gives nothing back to the program.
- **`return`** hands a value **back to the code.** Nothing appears on screen.

```python
def add_print(a, b):
    print(a + b)

def add_return(a, b):
    return a + b

x = add_print(2, 3)      # writes 5 on screen
print(x)                 # None  <- there is nothing inside x

y = add_return(2, 3)     # writes nothing on screen
print(y)                 # 5     <- but y holds the result
```

The test is simple: if you are going to **use the result in another calculation**,
you need `return`. You cannot write `add_print(2, 3) * 10`, because what you have
is `None`.

## Default values

You can give a parameter a value up front. That parameter then becomes optional:

```python
def greet(name, greeting="Hello"):
    return greeting + ", " + name

print(greet("Ada"))            # Hello, Ada
print(greet("Ada", "Hi"))      # Hi, Ada
```

Parameters with a default must be written **after** the ones without.
`def greet(greeting="Hello", name)` is an error — Python cannot work out which
value goes where.

## Naming

A function **does something**, so its name usually starts with a verb:
`calculate_total`, `send_email`, `get_user`. Words are separated by underscores.

Pick the name well and you will know what a function does without looking inside
it. Not `calc`, but `calculate_average`; and never `f1`.

---

## Summary

- A function lets you describe a job once and call it many times.
- It is defined with `def name(parameters):` and its body is indented.
- Defining is not running; it runs when you write `name(...)`.
- `return` hands the result back to the code and ends the function.
- With no `return`, a function returns `None`.
- `print` writes to the screen, `return` gives back a value — they differ.
- Parameters with defaults go last and become optional.
