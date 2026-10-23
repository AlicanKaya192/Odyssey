# Conditionals

The second week of CS50 Python. You can watch the video in the **Video** tab;
this page is the written version of the lecture. Until now every line of your
programs ran in order. This week we learn to let a program **make decisions**:
choosing one path or another depending on a condition, like taking the left
or the right road at a fork.

## Comparison operators

Python comes with **operators** that compare two values. Each one asks a
question, and the answer is `True` or `False`:

| Operator | Meaning |
|---|---|
| `>` / `<` | greater than / less than |
| `>=` / `<=` | greater than or equal / less than or equal |
| `==` | equal |
| `!=` | not equal |

Mind the double equals sign in `==`: a single `=` **assigns** (binds the
value on the right to the name on the left), the double `==` **compares**.
Mixing them up is this week's most common mistake.

## if

Let us open a file called `compare.py`:

```python
x = int(input("What's x? "))
y = int(input("What's y? "))

if x < y:
    print("x is less than y")
```

```text
$ python compare.py
What's x? 1
What's y? 2
x is less than y
```

The program gets two numbers and converts them to integers, then on the `if`
line it asks `x < y`. If the answer is `True`, the **indented** line below it
runs; if `False`, it is skipped. The colon (`:`) at the end of the `if` line
means "a block starts here"; the lines of the block are indented.

`True` and `False` have the type `bool` (Boolean, named after the logician
George Boole). `if` always decides by looking at a `bool`.

## Control flow, elif and else

Let us handle all three cases:

```python
x = int(input("What's x? "))
y = int(input("What's y? "))

if x < y:
    print("x is less than y")
if x > y:
    print("x is greater than y")
if x == y:
    print("x is equal to y")
```

```text
$ python compare.py
What's x? 2
What's y? 1
x is greater than y
```

The output is right, but the program asks **all three questions** every time.
They cannot all be true: if `x < y` is true, there is no point asking the
others. The order in which code runs is called **control flow**, and here the
flow is longer than it needs to be. `elif` ("else if") is asked only when the
condition before it was false:

```python
x = int(input("What's x? "))
y = int(input("What's y? "))

if x < y:
    print("x is less than y")
elif x > y:
    print("x is greater than y")
elif x == y:
    print("x is equal to y")
```

<figure class="fig"><div class="flow"><span class="node">x &lt; y ?</span><span class="arrow">→</span><span class="node">if not, x &gt; y ?</span><span class="arrow">→</span><span class="node">if not, else</span></div><figcaption>In an <code>if</code> / <code>elif</code> / <code>else</code> chain the questions are asked in order and the block of <b>the first true one</b> runs; the rest are never asked.</figcaption></figure>

One more step: if `x` is neither less nor greater, it must be equal. There is
no need to ask the last question; `else` means "every other case" and has no
condition:

```python
x = int(input("What's x? "))
y = int(input("What's y? "))

if x < y:
    print("x is less than y")
elif x > y:
    print("x is greater than y")
else:
    print("x is equal to y")
```

```text
$ python compare.py
What's x? 2
What's y? 2
x is equal to y
```

Your computer will not notice a few extra questions, but on a server running
them billions of times a day every unnecessary question costs time. Code that
asks fewer questions is both faster and easier to read.

## or

`or` is true when **either** condition is true:

```python
x = int(input("What's x? "))
y = int(input("What's y? "))

if x < y or x > y:
    print("x is not equal to y")
else:
    print("x is equal to y")
```

```text
$ python compare.py
What's x? 1
What's y? 2
x is not equal to y
```

Better still: "less or greater" means "not equal". One question is enough:

```python
x = int(input("What's x? "))
y = int(input("What's y? "))

if x != y:
    print("x is not equal to y")
else:
    print("x is equal to y")
```

```text
$ python compare.py
What's x? 3
What's y? 3
x is equal to y
```

## and

`and` is true when both conditions are true. A grade program, `grade.py`:

```python
score = int(input("Score: "))

if score >= 90 and score <= 100:
    print("Grade: A")
elif score >= 80 and score < 90:
    print("Grade: B")
elif score >= 70 and score < 80:
    print("Grade: C")
elif score >= 60 and score < 70:
    print("Grade: D")
else:
    print("Grade: F")
```

```text
$ python grade.py
Score: 95
Grade: A
```

Python lets you **chain** comparisons; instead of `score >= 90 and score <=
100` you can write it as in mathematics (something few other languages allow):

```python
score = int(input("Score: "))

if 90 <= score <= 100:
    print("Grade: A")
elif 80 <= score < 90:
    print("Grade: B")
elif 70 <= score < 80:
    print("Grade: C")
elif 60 <= score < 70:
    print("Grade: D")
else:
    print("Grade: F")
```

```text
$ python grade.py
Score: 85
Grade: B
```

It gets simpler still. If we reach an `elif`, we know the condition above was
false: anyone reaching `score >= 80` is already below 90. No need to write the
upper limits:

```python
score = int(input("Score: "))

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
elif score >= 60:
    print("Grade: D")
else:
    print("Grade: F")
```

```text
$ python grade.py
Score: 72
Grade: C
```

Fewer questions, and a program that is easier to read and easier to change
later. (In CS50's notes the lines of these two examples are indented one level
too far; written that way Python raises an `IndentationError`. Here they are
the versions verified by running them.)

All three logical operators together, including `not`:

```python
print(True and False)
print(True or False)
print(not True)
print(1 < 2 < 3)
print(3 > 2 > 2)
```

```text
$ python logic.py
False
True
False
True
False
```

The last line means `3 > 2 and 2 > 2`; the second part is false, so it is
`False`.

## Modulo

In mathematics, **parity** is whether a number is even or odd. The modulo
operator `%` gives the remainder of a division: if a number divides evenly by
2, the remainder is 0.

```python
print(4 % 2)
print(3 % 2)
print(10 % 3)
```

```text
$ python parity.py
0
1
1
```

`parity.py`:

```python
x = int(input("What's x? "))

if x % 2 == 0:
    print("Even")
else:
    print("Odd")
```

```text
$ python parity.py
What's x? 7
Odd
```

## Creating our own parity function

As we saw last week, handing the job to a function keeps code tidy. Let
`is_even` **return** `True` or `False`:

```python
def main():
    x = int(input("What's x? "))
    if is_even(x):
        print("Even")
    else:
        print("Odd")


def is_even(n):
    if n % 2 == 0:
        return True
    else:
        return False


main()
```

```text
$ python parity.py
What's x? 4
Even
```

The line `if is_even(x):` has no comparison operator, yet it works: the
function returns a `bool` and `if` looks at it directly.

## Pythonic

Writing something in a short, readable way that is natural to Python is
called **Pythonic**. The four-line `if` / `else` can become a one-line
**conditional expression**: `A if condition else B` (A when the condition is
true, otherwise B):

```python
def is_even(n):
    return True if n % 2 == 0 else False


print(is_even(4), is_even(7))
```

```text
$ python parity.py
True False
```

It reads almost like an English sentence. But there is one more step:
`n % 2 == 0` is already `True` or `False`. Returning it directly is enough:

```python
def is_even(n):
    return n % 2 == 0


print(is_even(4), is_even(7))
print(4 % 2 == 0)
```

```text
$ python parity.py
True False
True
```

## match

When a long `if` / `elif` chain compares one value with several possibilities
in turn, `match` can be more readable. First with `if`, the houses of *Harry
Potter*:

```python
name = input("What's your name? ")

if name == "Harry":
    print("Gryffindor")
elif name == "Hermione":
    print("Gryffindor")
elif name == "Ron":
    print("Gryffindor")
elif name == "Draco":
    print("Slytherin")
else:
    print("Who?")
```

```text
$ python house.py
What's your name? Hermione
Gryffindor
```

The first three conditions print the same thing; `or` combines them:

```python
name = input("What's your name? ")

if name == "Harry" or name == "Hermione" or name == "Ron":
    print("Gryffindor")
elif name == "Draco":
    print("Slytherin")
else:
    print("Who?")
```

```text
$ python house.py
What's your name? Draco
Slytherin
```

Watch out for a common mistake here: both sides of `or` must be full
conditions. If you write `name == "Harry" or "Hermione"`, the right side is not
`name == "Hermione"` but just `"Hermione"`, and every non-empty string counts
as true. Result: everyone ends up in Gryffindor.

```python
name = input("What's your name? ")

# Wrong: "Hermione" on its own always counts as true
if name == "Harry" or "Hermione":
    print("Gryffindor")
else:
    print("Who?")
```

```text
$ python house.py
What's your name? Draco
Gryffindor
```

Let us write the same program with `match`. `match` compares the value with
each `case` in turn; the block of the first matching case runs and matching
stops. `case _:` matches anything, so it does the job of `else`:

```python
name = input("What's your name? ")

match name:
    case "Harry":
        print("Gryffindor")
    case "Hermione":
        print("Gryffindor")
    case "Ron":
        print("Gryffindor")
    case "Draco":
        print("Slytherin")
    case _:
        print("Who?")
```

```text
$ python house.py
What's your name? Padma
Who?
```

Several values can share one `case`, joined with `|` (or):

```python
name = input("What's your name? ")

match name:
    case "Harry" | "Hermione" | "Ron":
        print("Gryffindor")
    case "Draco":
        print("Slytherin")
    case _:
        print("Who?")
```

```text
$ python house.py
What's your name? Ron
Gryffindor
```

## Summing up

Your programs can now ask questions and act on the answers:

- Comparison operators (`<`, `>`, `<=`, `>=`, `==`, `!=`) and `bool`
- `if`, `elif`, `else` and control flow
- `or`, `and`, `not` and chained comparisons
- Odd and even with modulo (`%`)
- Your own functions returning a `bool`
- Pythonic code and the conditional expression
- `match`, `case`, `|` and `case _`

## This week's problem set

The seven exercises in the **Exercise** tab practise this lecture's topics one
by one. The five in the **Problem Set** tab are CS50's assignment for the week
(Problem Set 1):

| Problem | What it asks | Topic in the lecture |
|---|---|---|
| Deep Thought | `Yes` for `42` or `forty-two` | `or`, `lower`, `strip` |
| Home Federal Savings Bank | `$0`, `$20` or `$100` by greeting | `if` / `elif`, `startswith` |
| File Extensions | the media type by extension | a long `elif` chain, `endswith` |
| Math Interpreter | compute an expression like `1 + 1` | `split`, `if` / `elif` |
| Meal Time | the meal for a time | `convert`, chained comparisons |

Some problems use a small method the lecture did not show (`startswith`,
`endswith`, `split`); CS50 sends students to the documentation too. They are
written in the prompts as hints.

---

*This section is translated and adapted from week 1 of Harvard University's [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) (lecture notes and problem set); examples and exercises were changed, and the problem set is checked by Odyssey, not by CS50's check50. The original and this adaptation are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Harvard does not endorse this adaptation.*
