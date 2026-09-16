A comprehension is not always better. One question is enough to decide:
**would somebody reading this line six months from now see what it does
at a glance?**

## Write a comprehension

When you are doing one of three things:

<figure class="fig anat">
  <div class="anat-row"><span>Transforming</span><span>Turning every element into another value: <code>[p * 2 for p in prices]</code></span></div>
  <div class="anat-row"><span>Filtering</span><span>Keeping some of the elements: <code>[p for p in prices if p &gt; 100]</code></span></div>
  <div class="anat-row"><span>Both at once</span><span><code>[p * 2 for p in prices if p &gt; 100]</code></span></div>
</figure>

## Write a loop

- When the line does not fit on one line.
- When there is a side effect: printing, writing to a file, updating
  something.
- When more than two `for` clauses are nested.
- When you fill more than one list in the same pass.
- When you need `break` or `continue` — a comprehension has neither.

That last point matters: a comprehension **looks at every element**. If
you want to stop as soon as you find what you are after, write a loop.

## The same job, two ways

```python
prices = [80, 120, 250, 95]

# Comprehension
expensive = [price for price in prices if price > 100]

# Loop
expensive = []
for price in prices:
    if price > 100:
        expensive.append(price)
```

Both give the same result. The comprehension turns three lines into one
and says "a new list is being built here" at the start of the line. With
the loop you have to read all three lines to see that.

## Speed

A comprehension is usually a little faster, because the `append` lookup
does not happen on every pass. The difference is small: milliseconds over
a hundred thousand elements. **Do not write a comprehension for speed**,
write it for readability.

## Three common mistakes

1. **Using one for a side effect.**

```python
[print(name) for name in names]
```

It prints, but it also produces a list nobody uses. Write a loop.

2. **Putting the filter at the front.**

```python
[score if score >= 50 for score in scores]
```

This is a `SyntaxError`. A filter goes at the end; what goes at the front
is a conditional value, completed with `if ... else`.

3. **Keeping a counter inside the comprehension.**

```python
total = 0
[total := total + p for p in prices]
```

It works but it does not read. For a sum there is `sum(prices)`.
