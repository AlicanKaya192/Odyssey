# Variables and Data Types

When we want to store a value in Python, we use a **variable**. You can think of a variable as a labelled box that you put something into.

## Assigning a value

We use the `=` symbol to assign a value:

```python
name = "Alican"
print(name)
```

Text (string) values are wrapped in quotes. The quotes can be double `" "` or single `' '` — both do the same job:

```python
name = "Alican"
name = 'Alican'
```

The `print()` function writes the value inside the variable to the screen.

## A common mistake

If you use single quotes and the text itself contains a single quote, Python cannot tell where the string ends:

```python
wrong = 'Alican's car'   # SyntaxError
```

Python reads `'Alican'` as the string and then cannot make sense of `s car`.

> **The fix:** escape the quote with a backslash: `'Alican\'s car'`. This is called an **escape character** in Python. Alternatively, use double quotes on the outside: `"Alican's car"` — usually the more readable option.

## Working with text

To join two strings together, use `+`:

```python
team = "Galatasaray"
team2 = "Trabzonspor"
print(team + team2)      # GalatasarayTrabzonspor
```

Careful: everything you join with `+` must **be a string**. If you want a space in between, you have to add it yourself:

```python
print(team + " " + team2)   # Galatasaray Trabzonspor
```

To repeat a string, use `*`:

```python
print(team * 2)    # GalatasarayGalatasaray
```

You cannot multiply two strings by each other — that raises an error.

## Checking the data type

Use `type()` to find out the type of a variable:

```python
team = "Galatasaray"
year = 1903

print(type(team))   # <class 'str'>
print(type(year))   # <class 'int'>
```

The basic types you will use most often:

| Type | Holds | Example |
|---|---|---|
| `str` | text | `"Galatasaray"` |
| `int` | whole number | `1903` |
| `float` | decimal number | `3.14` |
| `bool` | true/false | `True`, `False` |

## Printing different types together

If you use commas inside `print()`, Python places the values side by side and adds a space between them itself. Mixed types are not a problem:

```python
name = "Alican"
birth_year = 2001

print(name, "was born in:", birth_year)
# Alican was born in: 2001
```

But if you want to use `+`, you must convert the number to a string first:

```python
print(str(birth_year) + " " + name)   # 2001 Alican
```

The rule here is: **commas accept mixed types, plus does not.**

## Type conversion

To convert one type into another, use the type's name as a function:

```python
age = "25"            # this is text
age_number = int(age) # now it is a whole number

print(age_number + 5) # 30
```

`int()`, `str()`, `float()` and `bool()` are the converters you will use most. Trying to convert something that cannot be converted raises an error — for example `int("hello")` will not work.

## Formatting with f-strings

The most comfortable way to place a variable inside text is the f-string. Put an `f` before the quote and write the variable inside curly braces:

```python
name = "Alican"
age = 25

print(f"{name} is {age} years old.")
# Alican is 25 years old.
```

You can also do calculations inside an f-string:

```python
print(f"In 5 years they will be {age + 5}.")
# In 5 years they will be 30.
```

This approach is more readable than joining with `+`, and it saves you from worrying about type conversion.

---

## Summary

- Use `=` to assign a value.
- Strings go in quotes; an inner quote is escaped with `\'`.
- `+` only joins values of the same type, `,` accepts mixed types.
- `type()` tells you the type; `int()` / `str()` / `float()` convert between types.
- The cleanest way to put a variable inside text is an f-string.
