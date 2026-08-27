`range()` is a function for generating numbers. It earns its keep when you have no list and simply want a certain number of repetitions.

## Three forms

```python
range(5)          # 0, 1, 2, 3, 4
range(2, 6)       # 2, 3, 4, 5
range(0, 10, 2)   # 0, 2, 4, 6, 8
```

| Written as | What it means |
|---|---|
| `range(stop)` | starts at 0, goes **up to** `stop` |
| `range(start, stop)` | from `start` up to `stop` |
| `range(start, stop, step)` | in the given steps |

## Why is the upper bound excluded?

`range(5)` produces five numbers but does not include 5. That feels wrong at first. The reason is that counting starts at zero in Python, so "five of them" means "0 through 4".

There is a practical benefit — it lines up directly with the length of a list:

```python
names = ["Ada", "Alan", "Grace"]

for i in range(len(names)):
    print(i, names[i])
```

`len(names)` gives three, and `range(3)` produces 0, 1, 2 — exactly the valid positions in the list.

## Counting backwards

A negative step counts down:

```python
for i in range(3, 0, -1):
    print(i)      # 3, 2, 1
```

## range is not a list

If you try to print a `range` you will not see a list:

```python
print(range(5))         # range(0, 5)
print(list(range(5)))   # [0, 1, 2, 3, 4]
```

`range` does not build the numbers up front and hold them in memory; it produces them as they are asked for. That is why even `range(1000000)` uses almost no memory. To turn it into a list you need `list()`.

## Walking with the position

If you want both the item and its position, `enumerate()` is cleaner than `range(len(...))`:

```python
names = ["Ada", "Alan", "Grace"]

for i, name in enumerate(names):
    print(i, name)
```

Both give the same result, but `enumerate` states the intent more clearly and leaves less room for mistakes.
