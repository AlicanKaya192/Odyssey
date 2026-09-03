This note is a glossary. When you see an error on screen you can look up its
name here and find out what it is trying to say.

## `SyntaxError`

Appears before the code runs. Python cannot parse what you wrote.

```python
if score > 70
    print("passed")
```

```
SyntaxError: expected ':'
```

The commonest causes: a missing colon, an unclosed bracket, writing `=`
instead of `==` in a condition.

**A trap:** Python sometimes points at the **next** line. With an unclosed
bracket the problem is not on the line it reports but on the line where
Python gave up. If you cannot find anything wrong on the reported line, look
at the one above.

## `IndentationError`

The indentation does not line up. Because indentation is the syntax in
Python, this gets an error of its own.

```python
def greet():
print("hello")
```

```
IndentationError: expected an indented block
```

Mixing tabs and spaces causes the same error — they look identical on screen
but are different to Python.

## `NameError`

You reached for a name that was never defined.

```python
print(totl)
```

```
NameError: name 'totl' is not defined
```

Usually a typo. Forgetting the quotes around a string does it too:
`print(Hello)`.

## `TypeError`

The operation cannot be done with the types you gave it.

```python
print("5" + 3)
```

```
TypeError: can only concatenate str (not "int") to str
```

Other common forms: passing too few or too many arguments to a function,
calling something that is not a function.

## `ValueError`

The type is right but the value is not suitable for the operation.

```python
int("abc")
```

```
ValueError: invalid literal for int() with base 10: 'abc'
```

The difference from `TypeError` matters: `int([1, 2])` is a `TypeError` (a
list cannot be turned into a number), while `int("abc")` is a `ValueError`
(text is a convertible type but this text cannot be converted).

## `ZeroDivisionError`

```python
100 / 0
```

```
ZeroDivisionError: division by zero
```

It applies to `%` and `//` as well. When the divisor is a variable you either
check it first or catch the error.

## `IndexError`

An index that is not in the list.

```python
items = [1, 2, 3]
print(items[3])
```

```
IndexError: list index out of range
```

In a three-element list the indexes are 0, 1, 2. There is no `items[3]`.
Reaching the last element with `items[-1]` avoids this error entirely.

## `KeyError`

A key that is not in the dictionary.

```python
prices = {"apple": 12}
print(prices["melon"])
```

```
KeyError: 'melon'
```

Two ways out: ask with `in` first, or use `prices.get("melon", 0)`.

## `AttributeError`

The object has no such attribute or method.

```python
text = "hello"
text.push("x")
```

```
AttributeError: 'str' object has no attribute 'push'
```

This error usually tells you that what you are holding is not the type you
thought. If a function returned `None` and you call a method on it you see
`'NoneType' object has no attribute ...` — that is the form you meet most.

## `FileNotFoundError`

```python
open("data.csv")
```

```
FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'
```

The file is missing or in another folder. Paths are resolved relative to the
folder the program is running in.

## `ModuleNotFoundError`

```python
import pandas
```

```
ModuleNotFoundError: No module named 'pandas'
```

The module is not installed, or you misspelled the name. If it is one of your
own files, it is not in the same folder as the file you are running.

## `RecursionError`

A function that calls itself never stopped.

```
RecursionError: maximum recursion depth exceeded
```

Python gives up past a certain depth. It means the stopping condition is
missing or never holds.

## Their common ancestor

All of these come from a shared type called `Exception`. That is why
`except Exception:` catches almost all of them.

Almost — `KeyboardInterrupt` (Ctrl+C) and `SystemExit` stay outside it. Just
as well: a program with `except Exception:` can still be stopped with Ctrl+C.

Even so, think twice before writing `except Exception:`. Naming the error you
expect is always better.
