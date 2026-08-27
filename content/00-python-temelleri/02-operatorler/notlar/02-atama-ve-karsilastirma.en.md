This note covers two groups of operators: the ones that update a variable, and the ones that compare two values.

## Shorthand assignment

The long way to add something to a variable is this:

```python
total = 0
total = total + 5
```

The short way:

```python
total = 0
total += 5
```

Both do the same thing. `+=` means "add, then store the result back".

Every arithmetic operator has a shorthand form:

| Short | Long form |
|---|---|
| `x += 3` | `x = x + 3` |
| `x -= 3` | `x = x - 3` |
| `x *= 3` | `x = x * 3` |
| `x /= 3` | `x = x / 3` |
| `x //= 3` | `x = x // 3` |
| `x %= 3` | `x = x % 3` |
| `x **= 3` | `x = x ** 3` |

These shorthands earn their keep in loops — in the next section you will write `total += number` while adding up the numbers in a list.

## Comparison operators

These ask a question and answer it with `True` or `False`:

| Operator | Its question | Example | Result |
|---|---|---|---|
| `==` | are they equal? | `5 == 5` | `True` |
| `!=` | are they different? | `5 != 3` | `True` |
| `>` | is it greater? | `5 > 3` | `True` |
| `<` | is it smaller? | `5 < 3` | `False` |
| `>=` | greater or equal? | `5 >= 5` | `True` |
| `<=` | smaller or equal? | `5 <= 3` | `False` |

## The most common mistake

`=` and `==` are different things:

```python
age = 18      # ASSIGNMENT: put 18 into the variable age
age == 18     # COMPARISON: is age equal to 18? (produces True/False)
```

If you accidentally write `=` inside a condition, Python gives you a `SyntaxError`. That is actually good news — the mistake does not slip through quietly.

## Logical operators

To combine more than one condition, use `and`, `or` and `not`:

```python
age = 25
has_ticket = True

print(age >= 18 and has_ticket)   # True  -> both must be true
print(age >= 65 or has_ticket)    # True  -> one is enough
print(not has_ticket)             # False -> flips it
```

They read almost like English, which is the point: `and` needs both, `or` needs either, `not` reverses.

In the next section you will use these together with `if` — that is where they really start to matter.
