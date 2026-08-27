There are a few ways to pass values into a function. They all work with the same
function; the difference is how you write the call.

## Positional arguments

The most common form. Values are filled **in order**:

```python
def describe(name, age):
    return name + " is " + str(age)

print(describe("Ada", 36))     # Ada is 36
```

Order matters. Write `describe(36, "Ada")` and Python will not object, but the
result is nonsense — in this example you would even get a `TypeError`, because
you are trying to join a number to text.

## Keyword arguments

Write the parameter name and the order stops mattering:

```python
print(describe(age=36, name="Ada"))     # Ada is 36
```

This makes reading much easier as the number of parameters grows. Compare these
two:

```python
create_user("Ada", "Lovelace", True, False, 30)
create_user(name="Ada", surname="Lovelace", active=True, admin=False, age=30)
```

In the second one you know what `True` and `False` mean without opening the
function.

You can mix the two, but the **positional ones must come first**:

```python
describe("Ada", age=36)      # works
describe(name="Ada", 36)     # SyntaxError
```

## Default values

```python
def power(base, exponent=2):
    return base ** exponent

print(power(5))        # 25   -> exponent is taken as 2
print(power(5, 3))     # 125
```

Parameters with defaults sit at the **end** of the list. The reason is simple:
Python fills positional values from the front, so there cannot be a gap in the
middle.

```python
def wrong(a=1, b):     # SyntaxError
    return a + b
```

## Watch how many arguments you pass

If you pass too few:

```python
def add(a, b):
    return a + b

add(5)
# TypeError: add() missing 1 required positional argument: 'b'
```

If you pass too many:

```python
add(1, 2, 3)
# TypeError: add() takes 2 positional arguments but 3 were given
```

Both messages speak plainly: they tell you how many were expected and how many
arrived. Reading the error text is faster than guessing.

## A small trap

Do not use a **list** as a default value:

```python
def add_item(item, basket=[]):     # do not do this
    basket.append(item)
    return basket
```

The default value is created once, when the function is defined, and **the same
list** is reused on every call. So on the second call the old item is still
there. The correct way:

```python
def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket
```

Keep it somewhere in the back of your mind; plenty of people fall into this once
they start working with lists.
