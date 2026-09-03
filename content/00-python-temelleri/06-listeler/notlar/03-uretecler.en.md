Producing one list from another is one of the things you do most often. So
far you have done it with a loop:

```python
numbers = [1, 2, 3, 4]
doubled = []

for number in numbers:
    doubled.append(number * 2)

print(doubled)
```

```
[2, 4, 6, 8]
```

Python has a one-line form for this, and it is **very common in real code** —
you need to be able to read it.

## Your first comprehension

```python
doubled = [number * 2 for number in numbers]
```

The same result, one line instead of four.

<figure class="fig anat">
  <div class="sig">[<u class="m1">number * 2</u> <u class="m2">for number in numbers</u>]</div>
  <ul class="legend">
    <li class="m1"><b>What is produced</b> — the value worked out for each element. This is what goes into the list.</li>
    <li class="m2"><b>Where it comes from</b> — the header of an ordinary <code>for</code> loop, written the same way.</li>
  </ul>
</figure>

Read it backwards: **the loop on the right first, then the expression on the
left.** "For every number in numbers, number times two."

The square brackets say the result is a **list**.

## Filtering: adding `if`

You can put a condition on the end:

```python
scores = [90, 40, 75, 30, 65]
passed = [score for score in scores if score >= 50]

print(passed)
```

```
[90, 75, 65]
```

The loop equivalent:

```python
passed = []
for score in scores:
    if score >= 50:
        passed.append(score)
```

The trailing `if` is a **filter**: an element that fails the condition never
enters the list.

You can use both together:

```python
names = ["ada", "alan", "grace"]
short = [name.upper() for name in names if len(name) < 5]

print(short)
```

```
['ADA', 'ALAN']
```

## Dictionary and set comprehensions

The same form with curly brackets produces a dictionary:

```python
names = ["Ada", "Alan"]
lengths = {name: len(name) for name in names}

print(lengths)
```

```
{'Ada': 3, 'Alan': 4}
```

Without the colon it produces a set:

```python
unique = {len(name) for name in names}
```

You can loop over a dictionary too:

```python
scores = {"Ada": 90, "Alan": 40}
passed = {name: value for name, value in scores.items() if value >= 50}

print(passed)
```

```
{'Ada': 90}
```

## When to use one, and when not to

A comprehension does not replace every loop. The test: **use one when you are
producing a single list.**

<figure class="fig">
  <div class="versus">
    <div class="ok">
      <h5>APPROPRIATE</h5>
<pre><code>squares = [n * n for n in numbers]</code></pre>
    </div>
    <div class="no">
      <h5>NOT APPROPRIATE</h5>
<pre><code>[print(n) for n in numbers]</code></pre>
    </div>
  </div>
  <figcaption>The one on the right produces no list; it prints — and leaves behind a useless list of <code>None</code>. Loops that do work are written as ordinary <code>for</code> loops.</figcaption>
</figure>

**Do not use one:**

- When more than one job happens inside. A comprehension holds one
  expression.
- When there are two nested loops and a condition. It stops being readable;
  an ordinary loop is clearer.
- For side effects (`print`, writing to a file, appending to a list). A
  comprehension's job is producing values.

The length rule is simple: **if it does not fit on one line, write a loop.**

## A comparison table

| Loop | Comprehension |
|---|---|
| `result = []`<br>`for x in items:`<br>`    result.append(x * 2)` | `result = [x * 2 for x in items]` |
| `for x in items:`<br>`    if x > 0:`<br>`        result.append(x)` | `result = [x for x in items if x > 0]` |
| `for k, v in d.items():`<br>`    out[k] = v * 2` | `out = {k: v * 2 for k, v in d.items()}` |

## Where will you meet them?

Everywhere. When you look at a library's documentation, at an example, at an
answer on Stack Overflow. They are common in data science too:

```python
columns = [name.strip().lower() for name in header]
```

That line cleans up a CSV header. What you are learning is exactly how to read
that line.
