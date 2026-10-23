The most common mistakes in programs with conditionals and their messages
(measured on Python 3.14). Read the **last line** of an error message first.

## A single `=` in a comparison

```python
x = int(input("What's x? "))
if x = 1:
    print("one")
```

```text
$ python compare.py
  File "compare.py", line 2
    if x = 1:
       ^^^^^
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```

A single `=` assigns, comparison is `==`. Python guesses what you meant and
says so.

## No `:` after the condition

```python
x = int(input("What's x? "))
if x == 1
    print("one")
```

```text
$ python compare.py
  File "compare.py", line 2
    if x == 1
             ^
SyntaxError: expected ':'
```

Lines starting with `if`, `elif`, `else`, `match` and `case` all end with `:`.

## Writing `else if`

```python
x = int(input("What's x? "))
if x == 1:
    print("one")
else if x == 2:
    print("two")
```

```text
$ python compare.py
  File "compare.py", line 4
    else if x == 2:
         ^^
SyntaxError: expected ':'
```

The `else if` of other languages is `elif` in Python. Python expects a `:`
right after `else`, which is why the message talks about a missing colon.

## Comparing a string with a number

```python
x = input("What's x? ")
if x > 3:
    print("big")
```

```text
$ python compare.py
What's x? 5
Traceback (most recent call last):
  File "compare.py", line 2, in <module>
    if x > 3:
       ^^^^^
TypeError: '>' not supported between instances of 'str' and 'int'
```

`input` returns a string; `>` and `<` cannot compare a string with a number.
Convert first: `x = int(input(...))`. Note that `==` raises no error, it is
just always `False` (`"5" == 5` → `False`).

## Mistakes without an error

These produce no message; the program runs but does not do what you want.

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

| What you wrote | What happens | Instead |
|---|---|---|
| `name == "Harry" or "Ron"` | every name counts as true | `name == "Harry" or name == "Ron"` |
| three separate `if`s | if the conditions overlap, several blocks run | `if` / `elif` / `else` |
| `if score >= 80` first, `elif score >= 90` after | a 95 gets a `B` | order from largest to smallest |
| `case _:` at the top | the cases below are never reached | put `case _:` last |
| `"7:30" < "10:00"` | strings are compared letter by letter: `False` | convert to numbers first |
