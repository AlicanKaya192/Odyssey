# Comprehensions

Producing one list from another, building a dictionary from a list,
filtering a list — most of the code you write does these things. Python
has a one-line form for them: a **comprehension**.

You met the list form in the lists section: transforming and filtering.
Here we close four questions: how dictionaries and sets are produced, how
a filter differs from a conditional value, how nesting works, and how to
compute without filling memory.

## A reminder: list comprehension

```python
numbers = [1, 2, 3, 4, 5]

squares = []
for number in numbers:
    squares.append(number * number)
```

The same job in one line:

```python
squares = [number * number for number in numbers]
```

<figure class="fig anat">
  <div class="sig">[<u class="m1">number * number</u> <u class="m2">for number in numbers</u> <u class="m3">if number % 2 == 0</u>]</div>
  <ul class="legend">
    <li class="m1"><b>The value produced</b> — this is what goes into the list.</li>
    <li class="m2"><b>The source</b> — an ordinary <code>for</code> header.</li>
    <li class="m3"><b>The filter</b> — optional; an element that fails the condition is skipped.</li>
  </ul>
</figure>

Read it in this order: **the loop in the middle first, then the condition
on the right, then the expression on the left.** "For every number in
numbers, if it is even, take its square."

## Dictionary comprehension

Braces and the `key: value` form produce a dictionary:

```python
names = ["ada", "alan", "grace"]

lengths = {name: len(name) for name in names}
print(lengths)
```

```
{'ada': 3, 'alan': 4, 'grace': 5}
```

When you already have a dictionary, loop over it with `items()`:

```python
scores = {"ada": 90, "alan": 45, "grace": 72}

passed = {name: score for name, score in scores.items() if score >= 50}
print(passed)
```

```
{'ada': 90, 'grace': 72}
```

Swapping keys and values works the same way:

```python
flipped = {score: name for name, score in scores.items()}
```

## Set comprehension

Braces again but no `key: value` — the result is a set, so it holds **no
duplicates**:

```python
words = ["apple", "apricot", "elder", "avocado"]

initials = {word[0] for word in words}
print(initials)
```

```
{'a', 'e'}
```

Four words gave two letters; the set drops the repeats by itself.

## A conditional value: `if ... else`

This gets mixed up with the filter, but it is a different thing. A filter
**takes an element or leaves it out**; a conditional value **writes
something for every element**:

```python
scores = [90, 45, 72]

labels = ["passed" if score >= 50 else "failed" for score in scores]
print(labels)
```

```
['passed', 'failed', 'passed']
```

Their places differ too: the filter goes **at the end**, the conditional
value **at the front**.

<figure class="fig versus">
  <div class="ok">
    <h4>Filter (at the end)</h4>
    <p><code>[s for s in scores if s &gt;= 50]</code></p>
    <p>Two of the three elements remain. The length changes.</p>
  </div>
  <div class="dim">
    <h4>Conditional value (at the front)</h4>
    <p><code>["ok" if s &gt;= 50 else "no" for s in scores]</code></p>
    <p>Three elements stay three; their values change.</p>
  </div>
</figure>

## Nested comprehension

Flattening a list that is two levels deep:

```python
rows = [[1, 2], [3, 4], [5]]

flat = [value for row in rows for value in row]
print(flat)
```

```
[1, 2, 3, 4, 5]
```

The order is the same as nested `for` lines:

```python
flat = []
for row in rows:
    for value in row:
        flat.append(value)
```

Read left to right: the outer loop first, then the inner one. Beyond two
levels readability drops fast; write an ordinary loop there.

## Generator expression: parentheses instead of brackets

```python
numbers = [1, 2, 3, 4, 5]

total = sum(number * number for number in numbers)
any_big = any(number > 4 for number in numbers)
all_positive = all(number > 0 for number in numbers)

print(total, any_big, all_positive)
```

```
55 True True
```

This expression does **not** build a list; it produces the elements one
by one and hands them to `sum()`. On a file with a million rows that is
the difference between filling memory and not.

## When not to use one

<figure class="fig anat">
  <div class="anat-row"><span>When there is a side effect</span><span>Do not use a comprehension to write to a file or print; you build a list nobody uses.</span></div>
  <div class="anat-row"><span>When the line grows</span><span>A comprehension that does not fit on one line reads better as a loop.</span></div>
  <div class="anat-row"><span>Three levels deep</span><span>Two levels can be read; more than that calls for an ordinary loop.</span></div>
  <div class="anat-row"><span>A complex condition</span><span>When three conditions meet inside the <code>if</code>, a loop with <code>continue</code> is clearer.</span></div>
</figure>

This one is **not** used:

```python
[print(name) for name in names]
```

It prints, but it also builds a `[None, None, None]` list and throws it
away. An ordinary loop is the right tool.

## Summary

- `[expression for element in source if condition]` produces a list.
- `{key: value for ...}` gives a dictionary and `{value for ...}` a set.
- The filter goes last; a conditional value (`x if c else y`) goes first.
- `for` lines can be nested; more than two levels cannot be read.
- A generator expression in parentheses builds no list; with `sum`, `any`
  and `all` it works without filling memory.
- For side effects, long lines and complex conditions, write a loop.
