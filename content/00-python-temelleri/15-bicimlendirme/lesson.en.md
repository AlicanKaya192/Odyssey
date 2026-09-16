# Formatting Text

Everything you print is text. Printing a number as it is usually is not
enough: money grows a third decimal, table columns drift, percentages are
worked out by hand.

The part written after the colon inside an f-string does this job. It is
called a **format specifier**.

## The problem first

```python
price = 12.5
total = 1234567.891
rate = 0.0725

print(f"Price: {price}")
print(f"Total: {total}")
print(f"Rate: {rate}")
```

```
Price: 12.5
Total: 1234567.891
Rate: 0.0725
```

The price is missing its cents, the total cannot be read, and the rate
does not say what percentage it is. One piece of syntax fixes all three.

## The colon

<figure class="fig anat">
  <div class="sig">f"{<u class="m1">total</u><u class="m2">:</u><u class="m3">,.2f</u>}"</div>
  <ul class="legend">
    <li class="m1"><b>The value</b> — what gets printed. A variable or an expression.</li>
    <li class="m2"><b>The colon</b> — everything after it is the format.</li>
    <li class="m3"><b>The specifier</b> — how it looks: separator, digits, type.</li>
  </ul>
</figure>

The specifier does **not** change the value, only how it appears. `total`
is still `1234567.891`.

## Decimal places: `.2f`

```python
price = 12.5
print(f"Price: {price:.2f}")
print(f"Pi: {3.14159:.3f}")
```

```
Price: 12.50
Pi: 3.142
```

The number after the dot says how many digits you want, and `f` says you
want a decimal number. Missing digits are filled with zeros, extra ones
are rounded.

## Thousands separator: `,`

```python
total = 1234567.891
print(f"Total: {total:,}")
print(f"Total: {total:,.2f}")
```

```
Total: 1,234,567.891
Total: 1,234,567.89
```

The comma puts a separator every three digits. The order matters:
**separator first, digits after** (`,.2f`).

## Percentage: `%`

```python
rate = 0.0725
print(f"Rate: {rate:.1%}")
```

```
Rate: 7.2%
```

`%` does two things at once: it multiplies by a hundred and adds the
sign. Writing `{rate * 100:.1f}%` gives the same result, but `%` is
shorter and you cannot forget the multiplication.

## Width and alignment

A number written before the type says **how many characters at least**
the value will take:

```python
print(f"[{42:6}]")
print(f"[{'ada':6}]")
```

```
[    42]
[ada   ]
```

Numbers go to the right, text to the left. You can choose yourself too:

<figure class="fig anat">
  <div class="anat-row"><span><code>:&lt;10</code></span><span>Align left, pad to ten characters</span></div>
  <div class="anat-row"><span><code>:&gt;10</code></span><span>Align right</span></div>
  <div class="anat-row"><span><code>:^10</code></span><span>Centre</span></div>
  <div class="anat-row"><span><code>:*^10</code></span><span>Centre, pad with stars instead of spaces</span></div>
</figure>

## Lining up a table

This is where alignment earns its keep:

```python
products = [("Pencil", 3, 12.5), ("Notebook", 12, 145.0), ("Eraser", 5, 7.25)]

for name, count, price in products:
    print(f"{name:<10}{count:>4}{price:>10.2f}")
```

```
Pencil       3     12.50
Notebook    12    145.00
Eraser       5      7.25
```

The name is left aligned in ten characters, the count right aligned in
four, the price right aligned in ten with two digits. The columns line up
because every field has a fixed width.

## Padding with zeros

```python
for day in [1, 9, 15]:
    print(f"2026-09-{day:02d}")
```

```
2026-09-01
2026-09-09
2026-09-15
```

`d` means whole number and `02` means "at least two characters, fill the
rest with zeros". Clocks, dates and order numbers need it often.

## Showing the plus sign

```python
change = 4.2
print(f"Change: {change:+.1f}")
print(f"Change: {-change:+.1f}")
```

```
Change: +4.2
Change: -4.2
```

A plus sign is not printed by default; `+` prints it as well. It helps
when rises and falls sit next to each other.

## While debugging: `=`

```python
count = 7
print(f"{count = }")
```

```
count = 7
```

It writes both the name and the value of the variable. Shorter than
`print("count:", count)` while you are looking into your code.

## Not the same as `round()`

```python
price = 12.5
rounded = round(price, 2)

print(rounded)
print(f"{price:.2f}")
```

```
12.5
12.50
```

`round()` changes the **number** and does not keep the trailing zero; a
format specifier changes the **appearance**. Use the specifier when you
print, and `round()` when the value goes on into another calculation.

## Summary

- The format is written after the colon: `f"{value:specifier}"`.
- `.2f` sets decimal places, `,` adds thousands separators, `%` makes a
  percentage.
- The order is `[fill][align][sign][width][,][.digits][type]`.
- `<` aligns left, `>` right, `^` centre; width lines up columns.
- `02d` pads with zeros, `+` shows the plus sign.
- A specifier never changes the number, only how it looks.
