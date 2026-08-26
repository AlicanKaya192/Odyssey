For characters that cannot be typed directly inside text, Python uses **escape characters**. They all start with a backslash.

## The most common ones

| Written as | What it does |
|---|---|
| `\n` | moves to a new line |
| `\t` | inserts a tab space |
| `\\` | writes a backslash itself |
| `\'` | writes a single quote |
| `\"` | writes a double quote |

## Why are they needed?

If you opened a string with a single quote, a single quote inside it ends the string early:

```python
wrong = 'Alican's car'
```

Python reads `'Alican'` as the string, cannot make sense of the rest, and raises a `SyntaxError`. There are two fixes:

```python
right1 = 'Alican\'s car'    # escape the quote
right2 = "Alican's car"     # use double quotes outside
```

The second is usually more readable. Reach for an escape character only when there is no better option.

## Line breaks

```python
print("First line\nSecond line")
```

Output:

```
First line
Second line
```

## Turning escaping off

Backslashes cause trouble in file paths because Python treats them as escape characters. Putting `r` in front of the string turns escaping off completely:

```python
path = r"C:\Users\new\documents"
```

Without the `r`, `\U`, `\n` and `\d` would be read as escape characters and the path would break. This is called a **raw string**, and it will serve you well in file paths and regular expressions.
