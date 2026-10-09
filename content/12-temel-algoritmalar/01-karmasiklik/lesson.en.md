# Complexity and Big O

In the previous section we saw two algorithms for the same problem: one did
`n` additions, the other always a handful of operations. Both were correct;
the difference was **how the work grows as the input grows**. In this
section we learn to measure that difference and to state it with a single
notation: **Big O**.

## Why not seconds?

We can measure how many seconds an algorithm takes, but that number says
little: the same code is quick on a fast computer and slow on an old one,
and it changes again if another program is running in the background.
Instead we count **how many steps** the algorithm takes. By a step we mean
roughly one simple operation: a comparison, an addition, an assignment.

The easiest way to count steps is to add a counter to the algorithm. For
**linear search**, which looks for a value from the start of the list to
the end:

```python
def linear_search(items, target):
    steps = 0
    for i in range(len(items)):
        steps += 1
        if items[i] == target:
            return i, steps
    return -1, steps

data = list(range(1, 1001))
print(linear_search(data, 1))
print(linear_search(data, 500))
print(linear_search(data, 1000))
print(linear_search(data, 5000))
```

```text
(0, 1)
(499, 500)
(999, 1000)
(-1, 1000)
```

Same function, same list: if the target is at the start, **1** step; if it
is at the end or missing, **1000** steps. Two important ideas follow.

## Best, average and worst case

- **Best case:** the target is the first element, 1 step.
- **Worst case:** the target is the last element or missing, `n` steps.
- **Average case:** somewhere at random, about `n / 2`.

When comparing algorithms we mostly look at the **worst case**: we want to
be able to say "whatever happens, it takes no longer than this". Relying on
the best case in an application means the system grinds to a halt on a bad
day.

## Growth: how does the step count rise with `n`?

We can write an algorithm's step count as an expression in the input size
`n`. Linear search takes `n` steps in the worst case. What about this
nested loop?

```python
def count_pairs(n):
    steps = 0
    for i in range(n):
        for j in range(i + 1, n):
            steps += 1
    return steps

for n in [10, 100, 1000, 2000]:
    print(n, count_pairs(n))
```

```text
10 45
100 4950
1000 499500
2000 1999000
```

This loop visits **every pair** once: `n × (n − 1) / 2` steps. When `n`
doubled from 1000 to 2000, the step count **quadrupled** (499 500 →
1 999 000). For linear search, twice the input meant twice the work; here
it is four times. That is what we call the "rate of growth".

Now a loop that halves the number every round:

```python
def halving_steps(n):
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps

for n in [10, 100, 1000, 1_000_000, 1_000_000_000]:
    print(n, halving_steps(n))
```

```text
10 3
100 6
1000 9
1000000 19
1000000000 29
```

Getting from a billion down to 1 takes only **29** halvings. When the input
grew a thousandfold, the step count rose by only about 10. The answer to
"how many times can I halve it?" is called the **logarithm**: `log₂ n`.
Binary search (in the coming sections) is so fast precisely because of
this.

## Big O notation

Writing the exact step count (`3n + 5`, `n²/2 − n/2`) gives needless detail.
Big O keeps only the **dominant term**, with two rules:

1. **Constant factors are dropped:** `3n` → `O(n)`, `n²/2` → `O(n²)`.
2. **Smaller terms are dropped:** `n² + n + 7` → `O(n²)`.

Why can we drop them? Because as `n` grows, the dominant term crushes
everything else. With `n` at a million, `n²` is a trillion while `n` is only
a million: a millionth of it. Constants also depend on things outside the
algorithm, like the speed of the computer; Big O deliberately ignores them.

The classes you will meet often, from fast to slow:

| Notation | Name | Example | Steps for n = 1 000 000 |
|---|---|---|---|
| `O(1)` | constant | `items[5]` on a list, the sum formula | 1 |
| `O(log n)` | logarithmic | binary search, halving | ~20 |
| `O(n)` | linear | linear search, finding the largest | 1 000 000 |
| `O(n log n)` | n log n | efficient sorts (merge sort) | ~20 000 000 |
| `O(n²)` | quadratic | visiting every pair | 1 000 000 000 000 |
| `O(2ⁿ)` | exponential | trying every subset | too many to compute |

Let us turn those numbers into real time. On this computer a simple Python
loop takes about **10 million** steps per second (measured). So
on an input of a million elements an `O(n)` algorithm takes a tenth of a
second, `O(n log n)` a few seconds, and `O(n²)` hours on end. That gap
cannot be closed by buying a computer; it is closed by changing the
algorithm.

## Reading Big O from the code

Most of the time you do not need a counter; you look at the code and
estimate with these rules:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>A single simple operation</span><span><code>O(1)</code>: an assignment, a comparison, <code>items[i]</code>.</span></div>
    <div class="anat-row"><span>One loop, constant body</span><span><code>O(n)</code>: the loop runs <code>n</code> times.</span></div>
    <div class="anat-row"><span>Nested loops</span><span><b>Multiply</b>: <code>n</code> × <code>n</code> = <code>O(n²)</code>.</span></div>
    <div class="anat-row"><span>Consecutive blocks</span><span><b>Add</b>, the largest remains: <code>O(n) + O(n²)</code> = <code>O(n²)</code>.</span></div>
    <div class="anat-row"><span>A loop that halves every round</span><span><code>O(log n)</code>.</span></div>
    <div class="anat-row"><span>A built-in call</span><span>Count the loop inside it: <code>max</code>, <code>sum</code>, <code>in</code> (on a list) are <code>O(n)</code>.</span></div>
  </div>
  <figcaption>Estimating Big O by reading the code. Built-ins are one line, but there may be a loop inside.</figcaption>
</figure>

Example: a function that first goes through the list once (`O(n)`) and then
looks at every pair (`O(n²)`) is `O(n + n²) = O(n²)` in total.

## Memory is a cost too

Big O is used not only for time but also for **extra memory**. The loop
that finds the largest number keeps a single variable: `O(1)` extra memory.
Code that writes the square of every element into a new list builds a new
list of `n` elements: `O(n)` extra memory. Sometimes we spend memory to gain
speed (like finding repeats with a set in later sections); that is a
deliberate trade.

## Summary

- Algorithms are compared not in seconds but by **how the step count grows
  as the input grows**.
- We usually look at the **worst case**.
- Big O keeps the dominant term; constants and smaller terms are dropped.
- Classes: `O(1)` < `O(log n)` < `O(n)` < `O(n log n)` < `O(n²)` < `O(2ⁿ)`.
- Nested loops multiply, consecutive blocks add (the largest remains), a
  loop that halves every round is `O(log n)`.
- Extra memory is stated in Big O as well.
