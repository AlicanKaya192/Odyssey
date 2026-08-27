Operators are the symbols that do something to values. The ones you will use most are arithmetic.

## The table

| Operator | What it does | Example | Result |
|---|---|---|---|
| `+` | addition | `7 + 3` | `10` |
| `-` | subtraction | `7 - 3` | `4` |
| `*` | multiplication | `7 * 3` | `21` |
| `/` | division | `7 / 3` | `2.333…` |
| `//` | floor division | `7 // 3` | `2` |
| `%` | remainder (modulo) | `7 % 3` | `1` |
| `**` | power | `7 ** 3` | `343` |

## The difference between the two divisions

Mixing these two up is a common mistake:

```python
print(7 / 3)    # 2.3333333333333335  -> float
print(7 // 3)   # 2                   -> int
```

`/` **always** returns a decimal number, even when the division comes out even:

```python
print(6 / 2)    # 3.0  (not 3!)
print(6 // 2)   # 3
```

Use `//` when you want the whole part of a division. For example, finding how many full minutes there are in 100 seconds:

```python
seconds = 100
minutes = seconds // 60
print(minutes)   # 1
```

## What is the remainder operator for?

`%` gives you what is left over after a division. It looks useless at first, but it earns its place in three situations.

**Odd or even?** If the remainder of dividing by 2 is 0, the number is even:

```python
number = 14
print(number % 2)    # 0  -> even
```

**Finding the leftover part:** 100 seconds is 1 minute and 40 seconds:

```python
seconds = 100
print(seconds // 60)   # 1  -> minutes
print(seconds % 60)    # 40 -> leftover seconds
```

**Doing something at regular intervals:** if you want a counter to act every 5 steps, `counter % 5 == 0` is the check you need.

## Powers

`**` raises a number to a power:

```python
print(2 ** 10)    # 1024
print(9 ** 0.5)   # 3.0  -> square root
```

A fractional power gives you a root. `9 ** 0.5` produces the same result as `math.sqrt(9)`; the second one needs a module to be imported first.

## Order of operations

Python follows the order you learned in maths: `**` first, then `*` `/` `//` `%`, and `+` `-` last.

```python
print(2 + 3 * 4)      # 14   (multiplication first)
print((2 + 3) * 4)    # 20   (brackets come first)
```

When you are not sure, use brackets. Even when they are unnecessary, the person reading your code can see what you meant — that is not something worth economising on.
