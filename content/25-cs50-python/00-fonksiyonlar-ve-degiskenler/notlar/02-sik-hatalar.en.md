The mistakes that come up most often in this week's programs, with their
messages (measured in Python 3.14). Read the **last line** of an error first:
the type and the reason are there.

## An unclosed parenthesis or quote

```python
print("hello, world"
```

```text
SyntaxError: '(' was never closed
```

Python reads the whole file before running it; with a syntax error, no line
runs at all. Count your parentheses and quotes in pairs.

## Quotes inside quotes

```python
print("hello,"friend"")
```

```text
SyntaxError: invalid syntax. Is this intended to be part of the string?
```

Use single quotes outside (`'hello, "friend"'`) or escape the inner quote
(`"hello, \"friend\""`).

## Adding text and a number

```python
x = input("What's x? ")
print(x + 1)
```

```text
TypeError: can only concatenate str (not "int") to str
```

`input` returns text. Convert it first if you want to do arithmetic:
`int(input(...))`. Its silent sibling gives no error but is wrong: adding two
strings (`"1" + "2"` → `"12"`).

## Typing a decimal where an integer is expected

```python
int("1.5")
```

```text
ValueError: invalid literal for int() with base 10: '1.5'
```

`int` only converts whole-number text; use `float` for decimals.

## An undefined name

```python
hello()
```

```text
NameError: name 'hello' is not defined. Did you mean: 'help'?
```

The function was never defined, its name is spelled differently (case
matters too), or it is called **before** its definition.

## A function body without indentation

```python
def f():
print(1)
```

```text
IndentationError: expected an indented block after function definition on line 1
```

The body after a `def` line is indented (usually 4 spaces).

## Mistakes without an error

These produce no message; the program runs but does not do what you want.

| What you wrote | What happens | Instead |
|---|---|---|
| `print("hello, name")` | the word `name` is printed | `print(f"hello, {name}")` |
| `name.strip()` (on its own) | `name` does not change | `name = name.strip()` |
| `print("hello,", end="")` + `print(name)` | `hello,David`, joined | `print("hello, ", end="")` |
| `def main(): ...` and no call | the program does nothing | `main()` at the end of the file |
| `print(n * n)` in a function | no value comes back (`None`) | `return n * n` |
