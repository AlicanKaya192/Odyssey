# Exceptions

The fourth week of CS50 Python. You can watch the video in the **Video** tab;
this page is the written version of the lecture. **Exceptions** are problems
that arise while your program is running: things that go wrong within your
code.

## Syntax errors

Let us open a file called `hello.py` and make a mistake on purpose, leaving out
one of the quotes:

```python
print("hello, world)
```

```text
$ python hello.py
  File "hello.py", line 1
    print("hello, world)
          ^
SyntaxError: unterminated string literal (detected at line 1)
```

Python reports a **syntax error**. Python reads the whole file before running
it; if there is a syntax error, not a single line runs. The cure for these
errors is to double-check your code and fix it; the tools we see this week do
not help with them.

## Runtime errors

**Runtime errors** happen when the code meets something unexpected. For
example, you expect a number from the user and they type a letter instead.
`number.py`:

```python
x = int(input("What's x? "))
print(f"x is {x}")
```

```text
$ python number.py
What's x? 50
x is 50
```

The `f` at the start says that what is inside the curly braces (the value of
`x`) goes into the text. You can imagine a user easily typing a word instead
of a number, or even hitting Enter without typing anything. Typing `cat`:

```text
$ python number.py
What's x? cat
Traceback (most recent call last):
  File "number.py", line 1, in <module>
    x = int(input("What's x? "))
ValueError: invalid literal for int() with base 10: 'cat'
```

The `int` function cannot convert the text `cat` into a number and raises a
`ValueError`. As programmers we should be **defensive**: make sure our users
type what we expected. The way to do that is **error handling**.

## try

In Python, `try` and `except` are the way to test the user's input before
something goes wrong:

```python
try:
    x = int(input("What's x? "))
    print(f"x is {x}")
except ValueError:
    print("x is not an integer")
```

```text
$ python number.py
What's x? cat
x is not an integer
```

Typing `50` is accepted; typing `cat` shows the user a message explaining why
their input was not accepted. The error still happens, but instead of crashing
the program Python jumps to the `except` block.

Still, this is not the best way to write it: there are two lines inside `try`.
Good practice is to put in `try` only **the fewest lines you are worried could
fail**. Let us do that:

```python
try:
    x = int(input("What's x? "))
except ValueError:
    print("x is not an integer")

print(f"x is {x}")
```

```text
$ python number.py
What's x? cat
x is not an integer
Traceback (most recent call last):
  File "number.py", line 6, in <module>
    print(f"x is {x}")
                  ^
NameError: name 'x' is not defined
```

We reached our goal, but a new error appeared: a `NameError`, `x` is not
defined. Why? Assignment works **right to left**: first `int(input(...))` is
computed, then the result is assigned to `x`. When `int` fails, the assignment
never happens; there is no `x` to print on the last line.

## else

There is another way to handle such a case with `try`: `else`. If no error
occurs in the `try` block, the `else` block runs.

```python
try:
    x = int(input("What's x? "))
except ValueError:
    print("x is not an integer")
else:
    print(f"x is {x}")
```

```text
$ python number.py
What's x? 50
x is 50
```

```text
$ python number.py
What's x? cat
x is not an integer
```

<figure class="fig"><div class="flow"><span class="node">try: attempt</span><span class="arrow">→</span><span class="node no">an error?</span><span class="arrow">→</span><span class="node">if yes, except</span><span class="arrow">→</span><span class="node ok">if not, else</span></div><figcaption>The lines in the <code>try</code> block are attempted. If a <code>ValueError</code> occurs, Python leaves the rest of the block and jumps to <code>except</code>; if no error occurs, <code>except</code> is skipped and <code>else</code> runs.</figcaption></figure>

Notice too that we are being a bit rude to our user. If they do not type a
number, the program simply ends. Let us use a loop to ask again until a number
arrives:

```python
while True:
    try:
        x = int(input("What's x? "))
    except ValueError:
        print("x is not an integer")
    else:
        break

print(f"x is {x}")
```

```text
$ python number.py
What's x? cat
x is not an integer
What's x? dog
x is not an integer
What's x? 50
x is 50
```

`while True` loops forever; once the user gives the right input, the `break`
in `else` leaves the loop and the result is printed. A user who types something
wrong is asked again.

## Creating a function to get an integer

There will be many places where we want an integer from the user. Let us hand
the job to a function:

```python
def main():
    x = get_int()
    print(f"x is {x}")


def get_int():
    while True:
        try:
            x = int(input("What's x? "))
        except ValueError:
            print("x is not an integer")
        else:
            break
    return x


main()
```

```text
$ python number.py
What's x? cat
x is not an integer
What's x? 7
x is 7
```

We abstracted away getting an integer; the program itself is now just its first
three lines. It gets better still: `return` does not only return a value from a
function, it also leaves the loop inside it. No need for `break` plus a separate
`return`:

```python
def main():
    x = get_int()
    print(f"x is {x}")


def get_int():
    while True:
        try:
            x = int(input("What's x? "))
        except ValueError:
            print("x is not an integer")
        else:
            return x


main()
```

Some people also argue for returning the value straight from inside `try` when
the conversion works. It does the same thing with fewer lines:

```python
def main():
    x = get_int()
    print(f"x is {x}")


def get_int():
    while True:
        try:
            return int(input("What's x? "))
        except ValueError:
            print("x is not an integer")


main()
```

```text
$ python number.py
What's x? cat
x is not an integer
What's x? 7
x is 7
```

## pass

If, instead of warning the user every time, we want to quietly ask the
question again, we use `pass`. `pass` means "do nothing"; Python does not accept
an empty block, so it stands in for one:

```python
def main():
    x = get_int()
    print(f"x is {x}")


def get_int():
    while True:
        try:
            return int(input("What's x? "))
        except ValueError:
            pass


main()
```

```text
$ python number.py
What's x? cat
What's x? 7
x is 7
```

Sometimes you want to tell the user clearly what went wrong, sometimes just
asking again is enough. One final refinement: the prompt is currently
hard-coded inside `get_int`. Let us pass the prompt to the function as an
argument, so each call can ask a different question:

```python
def main():
    x = get_int("What's x? ")
    print(f"x is {x}")


def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            pass


main()
```

```text
$ python number.py
What's x? cat
What's x? 7
x is 7
```

## Two extras for the problem set

This week's problem set needs two more things that the lecture only touches on.

**Several exceptions.** A `try` can have several `except` blocks; Python runs
the first one matching the error. Dividing by zero raises a
`ZeroDivisionError`:

```python
try:
    x = int(input("x: "))
    y = int(input("y: "))
    print(x / y)
except ValueError:
    print("not an integer")
except ZeroDivisionError:
    print("cannot divide by zero")
```

```text
$ python divide.py
x: 1
y: 0
cannot divide by zero
```

If you do the same thing for both, you can catch the two types on one line:
`except (ValueError, ZeroDivisionError):`.

**The end of the input.** When the user presses `Ctrl+D` (on Windows `Ctrl+Z`
then Enter) to end the input, `input()` raises an `EOFError` (EOF stands for
*end of file*). In programs where you do not know how many lines will come,
the loop ends with it:

```python
total = 0
while True:
    try:
        n = int(input("Number: "))
    except EOFError:
        print()
        break
    total += n

print("Total:", total)
```

```text
$ python total.py
Number: 3
Number: 4
Number: 
Total: 7
```

In Odyssey you do not type the input yourself when an exercise is checked: the
check feeds each case's lines and then ends the input.

## Summing up

Errors are inevitable, but with what you learned today you can head them off:

- Exceptions, syntax and runtime errors
- `ValueError`, `NameError`, `ZeroDivisionError`, `EOFError`
- `try`, `except`, and keeping the fewest lines in `try`
- `else`, and asking again with `while True`
- Leaving a loop with `return`, carrying on quietly with `pass`

## This week's problem set

The seven exercises in the **Exercise** tab practise this lecture's topics one
by one. The four in the **Problem Set** tab are CS50's assignment for the week
(Problem Set 3):

| Problem | What it asks | Topic in the lecture |
|---|---|---|
| Fuel Gauge | `3/4` → `75%`, ask again if invalid | two exceptions, `round` |
| Felipe's Taqueria | keep the total of an order | `EOFError`, a dict |
| Grocery List | count and sort the items | `EOFError`, counting with a dict |
| Outdated | `9/8/1636` → `1636-09-08` | asking again on `ValueError` |

Grocery List uses `sorted` and Outdated uses `index`, which the lecture did not
show; they are written in the prompts as hints.

---

*This section is translated and adapted from week 3 of Harvard University's [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) (lecture notes and problem set); examples and exercises were changed, and the problem set is checked by Odyssey, not by CS50's check50. The original and this adaptation are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Harvard does not endorse this adaptation.*
