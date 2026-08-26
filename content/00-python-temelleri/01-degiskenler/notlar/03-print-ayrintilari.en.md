`print()` is the function you use from day one, but it has a few settings that make life easier once you know them.

## Separating with commas

With a comma, Python writes the values side by side and **adds a space itself**. Mixed types are not a problem:

```python
name = "Alican"
year = 2001
print(name, year)      # Alican 2001
```

This is both shorter and safer than joining with `+`. With `+` you would have to convert the number using `str()` first.

## Changing the separator: sep

If you do not want that space, change it with `sep`:

```python
print("2026", "08", "26", sep="-")    # 2026-08-26
print("a", "b", "c", sep="")          # abc
```

## Changing the line ending: end

By default `print()` adds a newline at the end. You can change that with `end`:

```python
print("loading", end="")
print("...")          # loading...
```

Useful when you want to keep writing on the same line.

## Formatting with f-strings

The cleanest way to place a variable inside text:

```python
name = "Alican"
age = 25
print(f"{name} is {age} years old.")
```

You can do calculations inside an f-string too:

```python
print(f"In 5 years they will be {age + 5}.")
```

To limit the number of decimal places, use a colon and a format code:

```python
pi = 3.14159265
print(f"Pi is about {pi:.2f}")     # Pi is about 3.14
```

That `.2f` notation will come in handy whenever you print tables or reports.
