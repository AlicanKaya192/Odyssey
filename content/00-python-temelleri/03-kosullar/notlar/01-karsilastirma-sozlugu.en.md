# Comparison Reference

A list of what you can put inside a condition. Look here when you get stuck.

## Comparison operators

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `==` | Is equal to | `5 == 5` | `True` |
| `!=` | Is not equal to | `5 != 3` | `True` |
| `>` | Is greater than | `5 > 3` | `True` |
| `<` | Is less than | `5 < 3` | `False` |
| `>=` | Is greater than or equal to | `5 >= 5` | `True` |
| `<=` | Is less than or equal to | `3 <= 5` | `True` |

All of them give back `True` or `False`. So when you write a comparison you
are really producing a value:

```python
result = 10 > 3
print(result)
```

```
True
```

## Chained comparison

Python has a short way of testing whether a value sits between two bounds:

```python
age = 25

if 18 <= age < 65:
    print("working age")
```

```
working age
```

This is the same as `age >= 18 and age < 65`, but easier to read. Most
languages do not have this form; Python does, and it is used.

## Logical operators

| Operator | True when |
|---|---|
| `and` | **Both** sides are true |
| `or` | **At least one** side is true |
| `not` | Flips the value |

```python
temperature = 30
raining = False

if temperature > 25 and not raining:
    print("go outside")
```

```
go outside
```

### Order of precedence

`not` first, then `and`, then `or`. So these two are the same thing:

```python
a or b and c
a or (b and c)
```

If you are unsure, add brackets. Brackets make life easier for whoever reads
the code; they do not slow anything down.

## `in` — is it inside?

It asks whether something is inside a container:

```python
name = "Ada"
team = ["Ada", "Alan", "Grace"]

if name in team:
    print("found")
```

It works on strings too, where it means "does this substring appear":

```python
if "@" in email:
    print("looks like an address")
```

The opposite is `not in`:

```python
if name not in team:
    print("missing")
```

## The difference between `==` and `is`

Both ask "are these the same", but they ask different questions:

- `==` → are the **values** the same?
- `is` → is it the **same object**?

```python
a = [1, 2]
b = [1, 2]

print(a == b)
print(a is b)
```

```
True
False
```

The two lists hold the same values, but they are two separate lists in
memory. That is why `==` is true and `is` is false.

**Rule:** use `==` when comparing values. `is` is only used with `None`,
`True` and `False`:

```python
if value is None:
    print("no value")
```

## Short-circuiting

`and` and `or` do not do unnecessary work. If the left-hand side already
settles the answer, the right-hand side is never evaluated:

```python
# the second condition never runs, because the first is already False
if False and expensive_check():
    ...
```

This has a practical use — check for safety first, then use the value:

```python
if len(values) > 0 and values[0] == "start":
    print("ok")
```

If the list were empty, `values[0]` would raise an error. But since the
left-hand condition is `False`, the right-hand side is never reached.

## Using a comparison without `if`

Because a condition is a value, you can assign it directly:

```python
is_adult = age >= 18
print(is_adult)
```

That is shorter and more readable than writing:

```python
if age >= 18:
    is_adult = True
else:
    is_adult = False
```

Both do the same job. The first one is preferred.
