The most common mistakes when working with exceptions and their messages
(measured on Python 3.14). Read the **last line** of an error message first.

## An uncaught ValueError

```python
x = int(input("What's x? "))
print(f"x is {x}")
```

```text
$ python number.py
What's x? cat
Traceback (most recent call last):
  File "number.py", line 1, in <module>
    x = int(input("What's x? "))
ValueError: invalid literal for int() with base 10: 'cat'
```

Every `int(input(...))` from a user will one day raise a `ValueError`. Catch it
with `try` / `except ValueError`.

## A name left unassigned after try

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

If `except` ran, `x` was never assigned. Move the line using the value into
`else`, or ask in a loop until a good value arrives.

## An uncaught division by zero

```python
x = int(input("x: "))
print(10 / x)
```

```text
$ python divide.py
x: Traceback (most recent call last):
  File "divide.py", line 2, in <module>
    print(10 / x)
          ~~~^~~
ZeroDivisionError: division by zero
```

If the divisor comes from the user, write `except ZeroDivisionError:` too. The
division must be **inside** `try`.

## An unclosed quote

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

A syntax error appears before the program starts; `try` cannot catch it. Fix
the code.

## Mistakes without an error

These produce no message; the program runs but does not do what you want.

| What you wrote | What happens | Instead |
|---|---|---|
| the whole program in `try` | other errors are caught with the wrong message | only the risky line |
| a bare `except:` | even your typos are swallowed quietly | `except ValueError:` |
| `except ValueError: pass` without a loop | the program quietly ends on bad input | ask again with `while True` |
| no `break` in `else` | it keeps asking after good input | `else: break`, or `return` |
| `except ValueError:` but the error is a `ZeroDivisionError` | not caught, the program stops | name both types |
| an `input()` loop not expecting `EOFError` | the program stops with an error when input ends | `except EOFError: break` |
