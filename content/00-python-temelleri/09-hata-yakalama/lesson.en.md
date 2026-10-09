# Handling Errors

Up to now, when an error appeared the program stopped. Some red text, a few
lines with file names, then silence.

Sometimes that is the right behaviour. Not always though: a program closing
down entirely because the user typed a letter instead of a number is not
good. It should have said "please enter a number" and asked again.

This section teaches that difference: which errors you catch and carry on
from, and which ones you leave where they are.

## Two kinds of error

A **syntax error** appears before the code even runs. Python sees something
it does not understand while reading the file:

```python
if score > 70
    print("passed")
```

```
SyntaxError: expected ':'
```

You cannot catch this because the program never starts. You have to fix it.

A **runtime error** appears while the code is running. There is nothing wrong
with the way it is written, but the operation cannot be done with the value
in hand at that moment:

```python
number = int("abc")
```

```
ValueError: invalid literal for int() with base 10: 'abc'
```

This section is about the second kind. Errors like these are called
**exceptions**.

## Reading a traceback

When an error appears Python prints a report. It looks long but it is easy to
read:

```
Traceback (most recent call last):
  File "main.py", line 7, in <module>
    result = divide(10, 0)
  File "main.py", line 3, in divide
    return a / b
ZeroDivisionError: division by zero
```

**Read it from the bottom up.** The last line says what happened:
`ZeroDivisionError: division by zero`. The lines above it show how you got
there — line 7 called `divide`, and the division happened on line 3.

The commonest beginner mistake is to look at the top line. The information
you want is **at the bottom**.

## `try` / `except`

The shape is this: you put the risky code in a `try` block, and if an error
appears the `except` block runs.

```python
try:
    number = int("abc")
    print(number)
except ValueError:
    print("that was not a number")
```

```
that was not a number
```

The moment an error appears, the rest of the `try` block is **skipped**. In
the example above `print(number)` never runs.

If no error appears the `except` block never runs:

```python
try:
    number = int("42")
    print(number)
except ValueError:
    print("that was not a number")
```

```
42
```

## Which error are you catching?

When you write `except` you say which error you expect. The ones you will
meet most:

| Error | When it appears |
|---|---|
| `ValueError` | Right type, impossible value: `int("abc")` |
| `TypeError` | Wrong type: `"5" + 3` |
| `ZeroDivisionError` | Dividing by zero |
| `KeyError` | A key that is not in the dictionary |
| `IndexError` | An index that is not in the list |
| `FileNotFoundError` | The file is not there |
| `NameError` | An undefined variable |

You can catch several at once:

```python
try:
    value = data[key]
except (KeyError, IndexError):
    value = None
```

Or treat each one differently:

```python
try:
    number = int(text)
    result = 100 / number
except ValueError:
    print("not a number")
except ZeroDivisionError:
    print("cannot divide by zero")
```

## Don't: a bare `except`

There is a form that catches **everything**:

```python
try:
    do_something()
except:            # don't do this
    pass
```

The problem is that you do not know what you caught. If there is a typo in
your code (a `NameError`) it lands in this block too and you never hear about
it. The program looks like it is working while giving a wrong answer.

Name the error you expect. An error you did not expect ought to appear — so
that you notice it.

## Getting hold of the error

When you want the error itself you use `as`:

```python
try:
    number = int("abc")
except ValueError as error:
    print("problem:", error)
```

```
problem: invalid literal for int() with base 10: 'abc'
```

`error` holds the explanation Python wrote. It is usually too technical to
show a user, but it is useful for a log.

## `else` and `finally`

Two more blocks can be added to a `try`:

```python
try:
    number = int(text)
except ValueError:
    print("not a number")
else:
    print("worked:", number)
finally:
    print("done")
```

- **`else`**: runs when **no** error appeared.
- **`finally`**: runs **always**, error or not.

`finally` is mostly used for tidying up: closing a file you opened, letting
go of a connection. That work has to happen even when something failed.

## `raise` — raising an error yourself

There is something as important as catching: sometimes **you** should raise
the error. Until now the errors you saw were raised by Python (like
`int("abc")`). `raise` lets you do the same in your own code.

```python
def set_age(age):
    if age < 0:
        raise ValueError(f"age cannot be negative: {age}")
    print("age saved")
    return age


print(set_age(30))
try:
    set_age(-5)
except ValueError as error:
    print("caught:", error)
```

```text
age saved
30
caught: age cannot be negative: -5
```

What happened, step by step:

- `raise ValueError("...")` builds an error and **throws** it. The text in
  the brackets is the error's explanation; caught with `as error`, `print`
  writes it.
- The moment `raise` runs, the function **stops there**: for `-5`, "age
  saved" was not printed and `return` never ran. Like `return`, it leaves the
  function; the difference is that it carries an error, not a value.
- The error goes to **the place that called** the function. If there is a
  `try` there, it is caught; if not, it goes to the caller above, finally
  reaching the program itself, and the program stops. Had only
  `set_age(-5)` been written below the `print(set_age(30))` line, without a
  `try`, the explanation you wrote would appear on the last line of the
  traceback (the file path is shortened):

```text
Traceback (most recent call last):
  File "main.py", line 9, in <module>
    set_age(-5)
    ~~~~~~~^^^^
  File "main.py", line 3, in set_age
    raise ValueError(f"age cannot be negative: {age}")
ValueError: age cannot be negative: -5
```

Why raise an error yourself? Because the value the function was handed is
meaningless and there is no sense in carrying on. Saying "this value will not
do" rather than quietly returning zero shows the caller where the problem
came from. A negative age that stops where it came in is far easier to find
than one that is saved and gives a strange result three functions later.

**Which error to raise?** Pick the one of Python's ready error types that
describes the situation:

| Situation | Error |
|---|---|
| The type is right but the value will not do (a negative age, an empty name) | `ValueError` |
| The type is wrong (text came where a number was expected) | `TypeError` |
| The requested key is missing | `KeyError` |

Do not raise a plain `Exception`: to catch it, the caller has to write
`except Exception` and so catches every other error too. Let the explanation
say what is wrong and what value came in: `age cannot be negative: -5` is far
more useful than `invalid input`.

## Catch, do something, raise again

Sometimes you want to catch an error and make a note of it but leave the
fixing to the caller. A **bare `raise`** inside an `except` block sends the
caught error up as it is:

```python
def read_age(text):
    try:
        return int(text)
    except ValueError:
        print("could not read:", text)
        raise


try:
    read_age("abc")
except ValueError as error:
    print("caller:", error)
```

```text
could not read: abc
caller: invalid literal for int() with base 10: 'abc'
```

`read_age` saw the error and wrote it down, but did not swallow it: the
caller got the same error with the same explanation. That is the difference
from catching the error and carrying on as if nothing happened (`pass`).

Writing your own error type (like `InsufficientFunds`) needs classes; that
comes in the Object-Oriented Programming section.

## When to catch and when to leave it

A simple test: **when you catch this error, do you have something sensible to
do about it?**

If you do, catch it — ask the user again, fall back to a default, show a
message. If you do not, leave it: an error you can see is better than a
program that quietly does the wrong thing.

```python
# Good: there is something to do
try:
    count = int(text)
except ValueError:
    count = 0

# Bad: the error was swallowed and nobody knows
try:
    save_to_database(record)
except:
    pass
```

In the second example the data was not saved and nobody was told.

## Summary

- A syntax error appears before the code runs and cannot be caught; a runtime
  error can be.
- Read a traceback **from the bottom up**; what happened is on the last line.
- `try` / `except` protects risky code; when an error appears the rest of the
  `try` is skipped.
- Name the error you expect; a bare `except` swallows everything.
- `as error` gets you the explanation.
- `else` runs when nothing failed, `finally` runs either way.
- `raise ValueError("explanation")` raises an error yourself and stops the
  function there; `ValueError` for a wrong value, `TypeError` for a wrong
  type.
- A bare `raise` inside `except` passes the same error up.
- If you cannot do anything about it, do not catch it.
