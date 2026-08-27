Sometimes you need to interfere with the flow of a loop: stop once you have found what you were looking for, or skip certain items. There are two keywords for that.

## break — ends the loop

Once you have found what you wanted, there is no point looking at the rest:

```python
numbers = [4, 8, 15, 16, 23, 42]

for number in numbers:
    if number > 10:
        print("First large number:", number)
        break
```

Output: `First large number: 15`. The loop stops when it finds 15; it never looks at 16, 23 or 42.

Without `break` the loop would run to the end and print four lines.

## continue — skips this turn

When you do not want to process certain items, `continue` cuts that turn short and moves to the next one:

```python
numbers = [1, 2, 3, 4, 5, 6]

for number in numbers:
    if number % 2 != 0:
        continue
    print(number)
```

Output: `2, 4, 6`. On odd numbers `continue` runs and the `print` line is never reached.

You could do the same with `if number % 2 == 0: print(number)`. `continue` mainly helps readability when there are several cases to skip and the body is long.

## The difference between them

| | What it does |
|---|---|
| `break` | Leaves the loop entirely |
| `continue` | Skips only this turn; the loop carries on |

## The loop's else

Python has a little-known structure: a loop can have an `else`.

```python
numbers = [4, 8, 15]

for number in numbers:
    if number > 100:
        print("Large number found")
        break
else:
    print("No large numbers at all")
```

This `else` runs when the loop finishes **without being cut short by `break`**. In the example there is no number above 100, so `break` never runs and `else` takes over.

It lets you handle the "I did not find it" case without keeping a separate flag variable. It is rarely used, but worth recognising when you meet it.

## Escaping an infinite loop

`break` is often paired with `while True`:

```python
count = 0

while True:
    count += 1
    if count >= 3:
        break

print(count)   # 3
```

Since the condition of `while True` is always true, `break` is the only way out. When you write this shape, do not forget the `break` line — without it the program loops forever.
