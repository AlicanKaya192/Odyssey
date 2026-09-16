A format specifier rounds, but rounding on a computer is not as simple as
it looks. Three different things get mixed up.

## 1. Decimal numbers are not stored exactly

```python
print(0.1 + 0.2)
print(f"{0.1 + 0.2:.2f}")
```

```
0.30000000000000004
0.30
```

The computer stores decimals in binary and `0.1` does not fit exactly.
The arithmetic is right, the display is surprising. This is why a format
specifier is used **every time** something is printed.

Comparisons hold the same trap:

```python
print(0.1 + 0.2 == 0.3)
print(round(0.1 + 0.2, 2) == 0.3)
```

```
False
True
```

## 2. round() does not round the way you expect

```python
print(round(2.5))
print(round(3.5))
```

```
2
4
```

Python rounds a half to the nearest **even** number. If you want every
half to go up you have to write that yourself; in accounting the
difference matters.

## 3. round() and a format specifier do different jobs

<figure class="fig versus">
  <div class="ok">
    <h4>Format specifier</h4>
    <p>Changes only the appearance. The number stays as it is and the
    trailing zero is printed: <code>12.50</code>.</p>
    <p>Used when printing, when producing a report.</p>
  </div>
  <div class="dim">
    <h4>round()</h4>
    <p>Changes the number itself and does not keep the trailing zero:
    <code>12.5</code>.</p>
    <p>Used when the calculation continues or the result is stored.</p>
  </div>
</figure>

## When you work with money

If the cents matter, there are two ways:

1. **Keep the cents as a whole number.** Work with `1250` (cents) and
   divide by a hundred when you print. Banking software does this.
2. **Use the `decimal` module.** It keeps decimals exact:

```python
from decimal import Decimal

print(Decimal("0.1") + Decimal("0.2"))
```

```
0.3
```

In this section `float` is enough; but if you write something real that
handles money, pick one of the two ways above.
