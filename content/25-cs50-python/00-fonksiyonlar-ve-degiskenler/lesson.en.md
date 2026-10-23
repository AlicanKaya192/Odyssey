# Functions, Variables

The first week of CS50 Python. You can watch the video in the **Video** tab;
this page is the written version of the lecture. Try the code in Odyssey's
exercise screen or on your own computer. By the end of the week you will have
programs that ask for your name, tidy up text, do arithmetic and use functions
you wrote yourself.

## Writing code with Python

A program is a list of instructions the computer carries out in order. A
Python program is a plain text file whose name ends in `.py`. In CS50 the
first file is called `hello.py`, and it contains a single line:

```python
print("hello, world")
```

To run the program you use the **terminal** (the command line), the window
where you give the computer commands by typing. The `$` means "you can type a
command"; you type `python hello.py` and press Enter:

```text
$ python hello.py
hello, world
```

Computers really only understand zeros and ones. The `python` command starts
an **interpreter**: it reads the text you wrote and turns it into steps the
computer can perform. This is the program nearly every programmer writes
first: printing `hello, world`. Congratulations, your first program is done.

## Functions

A **function** is something the computer, or the language, already knows how
to do; think of it as a verb. `print` is the verb "write to the screen". The
value you put in the parentheses is an **argument**: here the argument is the
text `"hello, world"`, and `print` writes it to the terminal.

## Bugs

Mistakes in code are called **bugs**, and they are a natural part of
programming; everyone makes them. Imagine you forgot the closing parenthesis:

```python
print("hello, world"
```

```text
$ python hello.py
  File "hello.py", line 1
    print("hello, world"
         ^
SyntaxError: '(' was never closed
```

Python reads the whole file before running it and stops when it finds an
unclosed parenthesis. The message tells you where (`line 1`) and why (`'('
was never closed`). Error messages often contain a clue; they are not always
this clear, but reading the last line first is a good habit.

## Personalising your first program

Let your program talk to the user. `input` is another function: it takes a
**prompt** as its argument, prints it and waits for the user to type
something and press Enter.

```python
input("What's your name? ")
print("hello, world")
```

```text
$ python hello.py
What's your name? David
hello, world
```

The question was asked and `David` was typed, but the program still said
`hello, world`: the name was not kept anywhere. To keep it we need a
variable.

### Variables

A **variable** is a container for a value inside your program; you give it a
name, like a label, and use the value through that name.

```python
name = input("What's your name? ")
print("hello, name")
```

The `=` in the middle is not the equals sign from mathematics; it is
**assignment**: the right side runs first (`input` asks the question and
**returns** what was typed), then that value is bound to the name `name` on
the left. But look at the output:

```text
$ python hello.py
What's your name? David
hello, name
```

Everything inside quotes is plain text; the word `name` there has nothing to
do with the variable. To use the variable, write it outside the quotes:

```python
name = input("What's your name? ")
print("hello,")
print(name)
```

```text
$ python hello.py
What's your name? David
hello,
David
```

The name comes through now, but on two separate lines. We will get to that
shortly.

### Comments

A **comment** is a line starting with `#` that Python never runs. You leave
notes for yourself and for others who read the code: what this does, and why.

```python
# Ask the user for their name
name = input("What's your name? ")
print("hello,")
print(name)
```

Comments can also serve as a to-do list.

### Pseudocode

**Pseudocode** means writing the steps as plain sentences in comments first,
when you do not yet know how to do the task. Then you write the code for each
step under its comment:

```python
# Ask the user for their name
name = input("What's your name? ")

# Print hello
print("hello,")

# Print the name inputted
print(name)
```

## Improving the program a little more

You can **concatenate** two strings with `+`. Note the space at the end of
`"hello, "`; without it the name would stick to the comma:

```python
name = input("What's your name? ")
print("hello, " + name)
```

Some functions take more than one argument. Give `print` two arguments
separated by a comma and it prints both **with a space between them**:

```python
name = input("What's your name? ")
print("hello,", name)
```

```text
$ python hello.py
What's your name? David
hello, David
```

## Strings and parameters

A **string**, `str` in Python, is a piece of text: letters, digits, spaces,
all together.

Functions have **parameters** that change how they behave. The documentation
of `print` shows two important ones:

- `end`: what goes at the end after printing. Its default is `"\n"`, a
  **newline**. That is why every `print` moves to a new line, and why two
  `print` calls split the greeting and the name onto two lines.
- `sep`: what goes between the arguments. Its default is a single space `" "`.

With `end=""` the newline is gone:

```python
name = input("What's your name? ")
print("hello,", end="")
print(name)
```

```text
$ python hello.py
What's your name? David
hello,David
```

Same line now, but `hello,` and `David` are stuck together: `end=""` removes
the newline and puts no space in its place. (CS50's notes say this prints
`hello, David`; when you run it, the two are joined.) Add the space yourself
and it is fixed:

```python
name = input("What's your name? ")
print("hello, ", end="")
print(name)
```

```text
$ python hello.py
What's your name? David
hello, David
```

With `sep` you choose what goes in between:

```python
print("hello", "world", sep=", ")
print("a", "b", "c", sep="-")
```

```text
$ python hello.py
hello, world
a-b-c
```

In short, a **parameter** is the name of an argument a function accepts
(`end`, `sep`); an **argument** is the value you pass when you call it (`""`,
`", "`).

### A small problem with quotation marks

If you want double quotes inside a string, Python gets confused about where
the string ends:

```python
print("hello,"friend"")
```

```text
$ python hello.py
  File "hello.py", line 1
    print("hello,"friend"")
                  ^^^^^^
SyntaxError: invalid syntax. Is this intended to be part of the string?
```

There are two fixes: open the string with **single quotes**, or put a
**backslash** (`\`) before the inner quote. The backslash means "the next
character is part of the string, not its end"; this is called **escaping**.

```python
print('hello, "friend"')
print("hello, \"friend\"")
```

```text
$ python hello.py
hello, "friend"
hello, "friend"
```

## Formatting strings

The most readable way to combine a string and a variable is a **formatted
string** (an f-string). You write `f` before the string, and the value of the
variable inside the braces `{}` is placed into the text:

```python
name = input("What's your name? ")
print(f"hello, {name}")
```

```text
$ python hello.py
What's your name? David
hello, David
```

You will use f-strings very often in this course.

## More on strings

**Never** assume the user will type exactly what you want. They may leave
spaces before and after their name, or type in lowercase. Strings come with
ready-made **methods**: functions you call by putting a dot after a string.
`strip` removes whitespace from the start and the end:

```python
name = input("What's your name? ")

# Remove whitespace from the str
name = name.strip()

print(f"hello, {name}")
```

```text
$ python hello.py
What's your name?     David   
hello, David
```

Note: `name.strip()` does not change `name`; it returns a **new**, cleaned
string. That is why we assign the result back to `name` (`name =
name.strip()`). `title` capitalises the first letter of every word:

```python
name = input("What's your name? ")
name = name.strip()

# Capitalize the first letter of each word
name = name.title()

print(f"hello, {name}")
```

```text
$ python hello.py
What's your name?    david malan  
hello, David Malan
```

Methods can be chained; each works on the string returned by the one before.
They can even be applied directly to the string `input` returns:

```python
name = input("What's your name? ").strip().title()
print(f"hello, {name}")
```

Which is better is debatable: one line is short but dense, separate lines are
longer but readable. In the terminal the up arrow brings back your last
command, so you do not have to retype `python hello.py` every time.

A few more methods that will help in the problem set:

```python
text = "Hello, World"
print(text.lower())
print(text.upper())
print(text.replace("World", "CS50"))
print("$50.00".removeprefix("$"))
print("15%".removesuffix("%"))
```

```text
$ python methods.py
hello, world
HELLO, WORLD
Hello, CS50
50.00
15
```

- `lower` / `upper`: make every letter lowercase / uppercase.
- `replace(old, new)`: replace every `old` with `new`.
- `removeprefix` / `removesuffix`: drop a given piece of text from the start /
  the end (and leave the string alone if it is not there).

## Integers (int)

In Python a whole number has the type `int` (integer). You know the usual
operators: `+`, `-`, `*`, `/`. Two more are new:

- `//` is **floor division**: it rounds the result down.
- `%` is **modulo**: it gives the remainder of a division (`7 = 2 × 3 + 1`,
  remainder 1).

```python
print(7 + 2)
print(7 - 2)
print(7 * 2)
print(7 / 2)
print(7 // 2)
print(7 % 2)
```

```text
$ python calculator.py
9
5
14
3.5
3
1
```

If you type just `python` in the terminal, the **interactive mode** opens with
a `>>>` prompt, and lines like `1 + 1` run immediately. This course will not
use it much, but it is handy for quick experiments.

Let us write a calculator, `calculator.py`:

```python
x = 1
y = 2

z = x + y

print(z)
```

```text
$ python calculator.py
3
```

Now from the user:

```python
x = input("What's x? ")
y = input("What's y? ")

z = x + y

print(z)
```

```text
$ python calculator.py
What's x? 1
What's y? 2
12
```

1 plus 2 came out as 12. Here is why: everything from the keyboard is
**text**. `input` always returns a `str`, and `+` puts two strings side by
side: `"1" + "2"` = `"12"`. The text has to be turned into a number; `int(x)`
does that. Changing a value from one type to another is called **casting**.

```python
x = input("What's x? ")
y = input("What's y? ")

z = int(x) + int(y)

print(z)
```

```text
$ python calculator.py
What's x? 1
What's y? 2
3
```

Shorter still: you can put functions inside functions.

```python
x = int(input("What's x? "))
y = int(input("What's y? "))

print(x + y)
```

<figure class="fig"><div class="flow"><span class="node">input("What's x? ")</span><span class="arrow">→</span><span class="node">"1"</span><span class="arrow">→</span><span class="node">int("1")</span><span class="arrow">→</span><span class="node ok">1</span></div><figcaption>In a nested call the <b>inner</b> one runs first: <code>input</code> returns the text, then <code>int</code> turns it into a number.</figcaption></figure>

## Readability wins

There are many reasonable ways to do the same thing; whichever you choose,
the code must be **readable**. Say what you do and why in comments, and do not
cram too much into one line. The person reading your code in six months is
most likely you.

## Float basics

A **floating point** value (a float) is a number with a decimal part, like
`0.52`. In Python the decimal separator is a dot (`.`):

```python
x = float(input("What's x? "))
y = float(input("What's y? "))

print(x + y)
```

```text
$ python calculator.py
What's x? 1.2
What's y? 3.4
4.6
```

To round the total to the nearest integer there is `round`. Its documentation
says `round(number[, ndigits])`; the square brackets mean "optional":

```python
x = float(input("What's x? "))
y = float(input("What's y? "))

# Create a rounded result
z = round(x + y)

print(z)
```

```text
$ python calculator.py
What's x? 1.2
What's y? 3.4
5
```

To write large numbers readably, the `:,` format inside an f-string puts a
comma as the thousands separator:

```python
x = float(input("What's x? "))
y = float(input("What's y? "))

z = round(x + y)

print(f"{z:,}")
```

```text
$ python calculator.py
What's x? 999
What's y? 1
1,000
```

## More on floats

A division can go on forever:

```python
x = float(input("What's x? "))
y = float(input("What's y? "))

z = x / y

print(z)
```

```text
$ python calculator.py
What's x? 2
What's y? 3
0.6666666666666666
```

There are two ways to round to two decimal places. A second argument to
`round`:

```python
x = float(input("What's x? "))
y = float(input("What's y? "))

z = round(x / y, 2)

print(z)
```

```text
$ python calculator.py
What's x? 2
What's y? 3
0.67
```

Or `:.2f` in an f-string ("a float with two digits after the point"):

```python
x = float(input("What's x? "))
y = float(input("What's y? "))

z = x / y

print(f"{z:.2f}")
```

```text
$ python calculator.py
What's x? 2
What's y? 3
0.67
```

The difference: `round` returns a **number**, `:.2f` produces **text**
(`round(2.5, 2)` gives `2.5`, while `f"{2.5:.2f}"` prints `2.50`).

## def: your own functions

Wouldn't it be nice to write our own functions? First let us call one that
does not exist:

```python
name = input("What's your name? ")
hello()
print(name)
```

```text
$ python hello.py
What's your name? David
Traceback (most recent call last):
  File "hello.py", line 2, in <module>
    hello()
    ^^^^^
NameError: name 'hello' is not defined. Did you mean: 'help'?
```

`NameError`: Python does not know a name `hello` (and suggests `help`, which
looks similar). To **define** a function you write `def`:

```python
def hello():
    print("hello")


name = input("What's your name? ")
hello()
print(name)
```

```text
$ python hello.py
What's your name? David
hello
David
```

Everything under `def hello():` is **indented**. Python uses indentation to
know which lines are the function's **body**; a line without indentation is
outside the function. The output is not what we want yet. Let us give the
function a **parameter** for whom to greet:

```python
# Create our own function
def hello(to):
    print("hello,", to)


# Output using our own function
name = input("What's your name? ")
hello(name)
```

```text
$ python hello.py
What's your name? David
hello, David
```

When `hello(name)` is called, the value of `name` goes into the function as
`to`. A parameter can also have a **default value**, used when no argument is
given:

```python
def hello(to="world"):
    print("hello,", to)


name = input("What's your name? ")
hello(name)

# Output without passing the expected arguments
hello()
```

```text
$ python hello.py
What's your name? David
hello, David
hello, world
```

Functions do not have to be at the top of the file. Programmers usually put
the main flow of the program in a function called `main` and write the other
functions below it:

```python
def main():
    name = input("What's your name? ")
    hello(name)


def hello(to="world"):
    print("hello,", to)
```

```text
$ python hello.py
```

Nothing happened. It is not an error: `def` only **defines**, it does not
run. Nobody called `main`, so the question was never even asked. One line at
the end of the file is enough:

```python
def main():
    name = input("What's your name? ")
    hello(name)
    hello()


def hello(to="world"):
    print("hello,", to)


main()
```

```text
$ python hello.py
What's your name? David
hello, David
hello, world
```

With this layout `hello` is already defined by the time `main` runs, so the
order of the functions in the file does not matter.

## Returning values

Sometimes you do not want a function to print something but to compute a
value and **hand it back**; that is a **return value**. `return` sends the
value back to wherever the function was called:

```python
def main():
    x = int(input("What's x? "))
    print("x squared is", square(x))


def square(n):
    return n * n


main()
```

```text
$ python calculator.py
What's x? 3
x squared is 9
```

The call `square(x)` takes `x` as `n` and returns `n * n`; `print` prints that
value. The difference between `print` and `return` matters: `print` writes to
the screen and the value is gone, `return` hands the value back so the program
can use it.

## Summing up

What you learned this week will come up again and again in every program you
write:

- Writing your first Python program and running it in the terminal
- Functions, arguments and parameters (`print`, `input`, `end`, `sep`)
- Bugs and reading an error message
- Variables and assignment (`=`)
- Comments and pseudocode
- Strings, f-strings and string methods (`strip`, `title`, `lower`, `replace`)
- Integers, floats and casting (`int`, `float`, `round`)
- Readability
- Your own functions (`def`, `main`) and return values (`return`)

## This week's problem set

This section has two kinds of exercises. The seven in the **Exercise** tab
practise this lecture's topics one by one. The five in the **Problem Set** tab
are CS50's assignment for the week (Problem Set 0); each uses a topic from the
lecture:

| Problem | What it asks | Topic in the lecture |
|---|---|---|
| Indoor Voice | print the input in lowercase | `lower` |
| Playback Speed | `...` in place of spaces | `replace` |
| Making Faces | text in place of `:)` and `:(`, `main` and `convert` | your own functions, `return` |
| Einstein | E = mc² | `int`, `**` |
| Tip Calculator | complete two missing functions | `removeprefix`, `float`, `return` |

How it differs from CS50:

- In CS50 each problem is written in its own file (`indoor.py`, `tip.py`...)
  and checked with `check50`. Here, when you press **Run**, Odyssey runs your
  program with the inputs from CS50's "How to Test" section one by one and
  compares your output.
- Your prompt (the text inside `input("...")`) can say anything you like; only
  what your program prints is checked.
- Making Faces uses `[happy]` / `[sad]` instead of emoji (so that everything
  you type is on the keyboard).

---

*This section is translated and adapted from week 0 of Harvard University's [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) (lecture notes and problem set); examples and exercises were changed, and the problem set is checked by Odyssey, not by CS50's check50. The original and this adaptation are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Harvard does not endorse this adaptation.*
