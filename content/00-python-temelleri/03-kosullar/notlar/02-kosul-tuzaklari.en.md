# Condition Traps

The places beginners most often go wrong with conditions. All of them come
from real mistakes; most of them **raise no error** and simply behave
incorrectly — which is what makes them dangerous.

## 1. `=` instead of `==`

```python
if age = 18:
    print("adult")
```

```
SyntaxError: invalid syntax
```

`=` assigns, `==` compares. This is a good trap because it raises an error —
there is no way to miss it.

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h5>ASSIGNMENT</h5>
<pre><code>age = 18</code></pre>
    </div>
    <div class="ok">
      <h5>COMPARISON</h5>
<pre><code>age == 18</code></pre>
    </div>
  </div>
  <figcaption>A single equals sign puts a value in; a double equals sign asks a question.</figcaption>
</figure>

## 2. `if x == 1 or 2`

This line raises no error, but it is **always true**:

```python
number = 7

if number == 1 or 2:
    print("matched")
```

```
matched
```

Python reads it as `(number == 1) or (2)`. `2` is a non-zero number, so its
truth value is `True`. The result: the condition always holds.

The correct way is to write out each possibility:

```python
if number == 1 or number == 2:
    print("matched")
```

Or, more concisely:

```python
if number in (1, 2):
    print("matched")
```

## 3. Writing `== True`

```python
if is_ready == True:
    print("go")
```

It works, but it is redundant. `is_ready` is already `True` or `False`;
comparing it to `True` again asks "is true true?".

```python
if is_ready:
    print("go")
```

And for the opposite, `not`:

```python
if not is_ready:
    print("wait")
```

## 4. Comparing decimal numbers with `==`

```python
print(0.1 + 0.2 == 0.3)
```

```
False
```

This is not a bug. Because computers store decimal numbers in binary,
`0.1 + 0.2` comes out as exactly `0.30000000000000004`.

With decimals you ask about **closeness** rather than equality:

```python
total = 0.1 + 0.2

if abs(total - 0.3) < 0.0001:
    print("close enough")
```

Whole numbers have no such problem; `==` is safe there.

## 5. Consecutive `if` instead of `elif`

These two are not the same thing:

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h5>CONSECUTIVE if</h5>
<pre><code>if score &gt;= 90:
    grade = "A"
if score &gt;= 80:
    grade = "B"</code></pre>
    </div>
    <div class="ok">
      <h5>elif</h5>
<pre><code>if score &gt;= 90:
    grade = "A"
elif score &gt;= 80:
    grade = "B"</code></pre>
    </div>
  </div>
  <figcaption>For a score of 95 the left-hand version writes "A" and then overwrites it with "B". The right-hand one stops at the first condition that holds.</figcaption>
</figure>

When `score = 95`, the left-hand code puts `"A"` into `grade` and then
`"B"` — because 95 is greater than both bounds and the two `if` statements
run independently. The result is `"B"`, which is wrong.

`elif` means "if the previous one did not hold, look at this". The chain
closes at the first condition that holds.

## 6. Writing the order backwards

```python
if score >= 50:
    grade = "pass"
elif score >= 90:
    grade = "excellent"
```

For `score = 95` the result is `"pass"`. 95 hits the `>= 50` condition first,
the chain ends there, and the `elif` line is never reached.

**Rule:** in an `elif` chain, conditions go from **narrowest to widest**. The
most selective one goes at the top.

```python
if score >= 90:
    grade = "excellent"
elif score >= 50:
    grade = "pass"
```

## 7. Indentation

In Python indentation is not decoration; it is the code itself:

```python
if logged_in:
    print("welcome")
print("goodbye")
```

`print("goodbye")` is not indented, so it is **outside** the `if`. It runs
even when the condition does not hold. If you want it inside, you have to
indent it.

There is also the mixed-indentation problem: if you use spaces on some lines
and tabs on others, Python raises a `TabError`. Set your editor to convert
tabs to spaces and use four spaces.

## 8. Asking about an empty container with `len`

This works, but it is long:

```python
if len(items) > 0:
    print("has items")
```

In Python an empty list, an empty string and an empty dictionary already
count as `False`:

```python
if items:
    print("has items")
```

Same thing, shorter. This is the preferred way of checking for emptiness.

## Summary

- `=` assigns, `==` compares.
- `x == 1 or 2` is always true; write out each possibility.
- `== True` is redundant; write the condition directly.
- With decimals, ask about closeness rather than equality.
- Consecutive `if` and `elif` behave differently.
- In an `elif` chain, the most selective condition goes at the top.
- Indentation changes what the code means.
- `if items:` is enough to check for emptiness.
