# Operators and Loops

In this section you will learn how to do arithmetic, compare values, and walk over the items of a list one by one. These are the basic tools you will use in every section that follows.

## Arithmetic operators

| Operator | What it does | Example | Result |
|---|---|---|---|
| `+` | addition | `7 + 3` | `10` |
| `-` | subtraction | `7 - 3` | `4` |
| `*` | multiplication | `7 * 3` | `21` |
| `/` | division | `7 / 3` | `2.333…` |
| `//` | floor division | `7 // 3` | `2` |
| `%` | remainder | `7 % 3` | `1` |
| `**` | power | `7 ** 3` | `343` |

`/` always returns a decimal number (`float`) — even `7 / 1` gives `7.0`. If you want a whole number, use `//`.

The `%` operator is especially handy for telling whether a number is even or odd: if `number % 2 == 0`, the number is even.

## Comparison operators

These return `True` or `False`:

```python
print(5 > 3)    # True
print(5 == 3)   # False
print(5 != 3)   # True
```

Careful: `=` assigns, `==` compares. Mixing these two up is one of the most common mistakes there is.

## The for loop

To visit the items of a list one at a time, use `for`:

```python
sayilar = [1, 2, 3, 4, 5]

for sayi in sayilar:
    print(sayi)
```

The body of the loop is written **indented**. In Python indentation takes the place of curly braces, so it is not optional.

## Adding things up with a loop

To sum the numbers in a list, first define an accumulator variable, then add to it inside the loop:

```python
sayilar = [1, 2, 3, 4, 5]
toplam = 0

for sayi in sayilar:
    toplam = toplam + sayi

print(toplam)   # 15
```

Instead of `toplam = toplam + sayi` you can write the shorter `toplam += sayi` — they mean the same thing.

Python also has a built-in `sum()` function that does this in one line. But using `sum()` before you understand how a loop works will make the later sections harder for you. That is why the exercise asks you not to use it.

---

## Summary

- `/` gives a decimal, `//` divides into whole numbers; `%` gives the remainder.
- `=` assigns, `==` compares.
- `for` walks over the items of a list, and its body is indented.
- To add things up, zero the accumulator first, then add to it inside the loop.
