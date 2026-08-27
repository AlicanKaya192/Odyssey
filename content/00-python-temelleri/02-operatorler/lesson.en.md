# Operators

In this section you will learn how to do arithmetic and how to compare values. These are the basic tools you will use in every section that follows.

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

`/` always returns a decimal number (`float`) — even `6 / 2` gives `3.0`, not `3`. Use `//` when you want a whole number.

## The remainder operator

`%` gives you what is left over after a division, and it is far more useful than it looks.

```python
number = 14
print(number % 2)    # 0  -> the number is even
```

This is the standard way to tell whether a number is even: if `number % 2 == 0`, it is.

It comes up in time calculations too:

```python
seconds = 100
print(seconds // 60)   # 1  -> whole minutes
print(seconds % 60)    # 40 -> leftover seconds
```

## Shorthand assignment

There is a short way to add something to a variable:

```python
total = 0
total = total + 5    # the long form
total += 5           # the short form, same thing
```

Every arithmetic operator has a shorthand: `-=`, `*=`, `/=`, `//=`, `%=`, `**=`.

> This shorthand will earn its keep in loops. When adding up the numbers in a list, `total += number` is both shorter than `total = total + number` and clearer about what you meant.

## Comparison operators

These ask a question and return `True` or `False`:

```python
print(5 > 3)     # True
print(5 == 3)    # False
print(5 != 3)    # True
```

| Operator | Its question |
|---|---|
| `==` | are they equal? |
| `!=` | are they different? |
| `>` `<` | greater, smaller? |
| `>=` `<=` | greater/smaller or equal? |

## The most common mistake

`=` and `==` are different things, and mixing them up is where beginners get stuck most often:

```python
age = 18      # ASSIGNMENT: put 18 into the variable age
age == 18     # COMPARISON: is age equal to 18?
```

One places a value; the other asks a question.

## Logical operators

To combine more than one condition, use `and`, `or` and `not`:

```python
age = 25
has_ticket = True

print(age >= 18 and has_ticket)   # True  -> both must be true
print(age >= 65 or has_ticket)    # True  -> one is enough
print(not has_ticket)             # False -> flips it
```

You will really put these to work in the next section, together with `if`.

## Order of operations

Python follows the order you learned in maths: `**` first, then `*` `/` `//` `%`, and `+` `-` last.

```python
print(2 + 3 * 4)      # 14   (multiplication first)
print((2 + 3) * 4)    # 20   (brackets come first)
```

When you are not sure, use brackets. Extra brackets tell whoever reads your code what you meant.

---

## Summary

- `/` gives a decimal, `//` divides into whole numbers; `%` gives the remainder.
- `%` is how you check for even numbers: `number % 2 == 0`.
- `total += 5` means `total = total + 5`.
- `=` assigns, `==` compares — do not mix them up.
- `and` wants both, `or` wants either, `not` reverses.
