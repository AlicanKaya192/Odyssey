# Loops

When you want to do the same thing to every item in a list, you use a loop. Without one you would write ten lines for a ten-item list, and a hundred for a hundred-item list. A loop removes that repetition.

## The for loop

To visit the items of a list one at a time, use `for`:

```python
numbers = [1, 2, 3, 4, 5]

for number in numbers:
    print(number)
```

Here `number` holds the next item of the list on every turn. You choose its name; you could just as well have written `for item in numbers`.

The body of the loop is written **indented**. In Python indentation takes the place of curly braces, so it is not optional — forget it and you get an `IndentationError`.

## Adding things up

Summing the numbers in a list is the most common use of a loop. First you define an **accumulator** variable, then you add to it inside the loop:

```python
numbers = [1, 2, 3, 4, 5]
total = 0

for number in numbers:
    total += number

print(total)   # 15
```

The order matters: `total = 0` must come **before** the loop. Put it inside and it resets on every turn, giving you the wrong answer.

> The `+=` you learned in the previous section is doing the work here. `total += number` and `total = total + number` are the same thing, but the short form states the intent more clearly.

## Generating numbers with range

When you have no list and simply want a certain number of repetitions, use `range()`:

```python
for i in range(5):
    print(i)
```

This prints `0, 1, 2, 3, 4` — **five numbers, starting from zero**. The upper bound is not included; that is a rule you meet everywhere in Python and it takes a while to get used to.

`range()` comes in three forms:

```python
range(5)         # 0, 1, 2, 3, 4
range(2, 6)      # 2, 3, 4, 5
range(0, 10, 2)  # 0, 2, 4, 6, 8   -> in steps of two
```

## The while loop

`for` is for a known number of repetitions; `while` repeats **as long as a condition holds**:

```python
count = 3

while count > 0:
    print(count)
    count -= 1

print("Done")
```

This prints `3, 2, 1, Done`.

There is only one thing to watch when writing a `while`: **the condition must eventually become false.** In the example above, forget the `count -= 1` line and `count` stays at 3 forever, so the loop never ends. That is called an infinite loop.

> If you write an infinite loop in this application, it stops your code after 10 seconds and tells you. The app itself does not freeze.

## Which one, when?

A simple rule: **if you know how many times you will repeat, use `for`; if you do not, use `while`.**

Walking over the items of a list has a known count — `for`. Asking a user until they give the right answer has no known count — `while`.

In practice `for` is used far more often.

---

## Summary

- `for item in mylist:` walks over the items of a list.
- The loop body is indented; indentation is not optional.
- When adding things up, the accumulator is zeroed **before** the loop.
- `range(5)` counts from zero to four — the upper bound is not included.
- `while` repeats as long as the condition holds; forget to change the condition and it repeats forever.
