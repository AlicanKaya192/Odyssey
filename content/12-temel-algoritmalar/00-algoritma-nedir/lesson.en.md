# What Is an Algorithm?

Think of a recipe: the ingredients are given, the steps come in order,
every step is clear ("boil the water", "add the pasta, wait 8 minutes")
and at the end there is a meal. An **algorithm** is exactly that: **ordered,
clear steps that finish** and solve a problem.

A computer cannot make up the recipe on its own; you give it the steps. In
this path we go one step beyond running code: we learn to **break a problem
into steps**, to make sure those steps are **correct**, and to say **which
of two solutions is better**.

## Input, steps, output

Every algorithm has three parts:

- **Input:** the data the algorithm works on. A list of numbers, say.
- **Steps:** the instructions that process the input.
- **Output:** the result. The largest number in the list, say.

<figure class="fig">
  <div class="flow">
    <span class="node">Input: [3, 8, 2, 9, 4]</span><span class="arrow">→</span>
    <span class="node">Steps</span><span class="arrow">→</span>
    <span class="node acc">Output: 9</span>
  </div>
  <figcaption>An algorithm is the sequence of steps that turns input into output. The same input must give the same output every time.</figcaption>
</figure>

## A first algorithm: finding the largest number

Imagine a stack of cards with a number on each. How do you find the
largest? Probably like this:

1. Look at the first card and keep its number in mind: "the largest so far".
2. Look at the next card. If it is bigger than the one in mind, replace it.
3. Repeat step 2 until no cards are left.
4. The number in mind is the largest.

Those four lines are an algorithm. It is not Python yet, but every step is
clear. Writing steps like this, **independent of any programming language**
and close to plain speech, is called **pseudocode**:

```text
largest ← first element of the list
for each number in the list:
    if number > largest:
        largest ← number
result: largest
```

`←` means "assign this to that". Pseudocode has loose rules; the point is to
make the idea clear before writing code. Turning it into Python is now
almost word for word:

```python
def find_largest(numbers):
    largest = numbers[0]
    for number in numbers:
        if number > largest:
            largest = number
    return largest

print(find_largest([3, 8, 2, 9, 4]))
```

```text
9
```

"Python already has `max()`", you may say, and you are right. But inside
`max()` exactly this loop is running. Someone who does not know what is
inside the ready-made function does not know what to do when a problem has
no ready-made function. In this path we deliberately set the built-ins
aside and write the algorithms ourselves; afterwards it becomes much clearer
which built-in tool helps when.

## What makes a good algorithm

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Input and output</span><span>What it works with and what it produces are clear.</span></div>
    <div class="anat-row"><span>Definiteness</span><span>Every step has one meaning; two people carry it out the same way.</span></div>
    <div class="anat-row"><span>Finiteness</span><span>It ends at some point on every input; it does not run forever.</span></div>
    <div class="anat-row"><span>Correctness</span><span>It gives the right result on every valid input, not just the example.</span></div>
    <div class="anat-row"><span>Efficiency</span><span>It takes no more steps than needed; it stays reasonable as the input grows.</span></div>
  </div>
  <figcaption>A recipe has these five properties too: ingredients, clear steps, a process that ends, the right dish and a reasonable time.</figcaption>
</figure>

The one most often skipped is **correctness**: an algorithm that gave the
right answer on an example does not necessarily work on every input.

## Edge cases: the real test of an algorithm

Picture someone solving the same problem slightly differently: "I will
start the largest at zero; every number is bigger than zero anyway".

```python
def find_largest_wrong(numbers):
    largest = 0
    for number in numbers:
        if number > largest:
            largest = number
    return largest

print(find_largest_wrong([3, 8, 2, 9, 4]))
print(find_largest_wrong([-5, -2, -9]))
```

```text
9
0
```

The first list is right, the second is **wrong**: it returned `0`, which is
not even in the list. The assumption "every number is bigger than zero"
broke on negative numbers. The version that starts from the first element
does not fall into this trap:

```python
print(find_largest([-5, -2, -9]))
```

```text
-2
```

An algorithm is most likely to break not on ordinary inputs but on the
ones **at the edges**. These are called **edge cases**. After writing an
algorithm, ask yourself:

- **Empty input:** what if the list is empty? (`find_largest([])` raises an
  error: there is no `numbers[0]`. Either we document that or we return a
  special value.)
- **One element:** is a one-number list right?
- **All equal:** `[7, 7, 7]`?
- **Negatives and zero:** the bug above showed up exactly here.
- **Position:** is the answer at the start, at the end, in the middle?

The checks in the exercises will try your code with exactly these inputs.

## Same problem, two algorithms

A problem often has more than one correct algorithm. Take the sum of the
numbers from 1 to `n`. The first idea is to add them one by one:

```python
def sum_loop(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total
```

Then there is the way Gauss reportedly found as a child: pair 1 with 100,
2 with 99, and every pair makes 101, with 50 pairs. In general
`n × (n + 1) / 2`:

```python
def sum_formula(n):
    return n * (n + 1) // 2

print(sum_loop(100), sum_formula(100))
print(sum_loop(1_000_000) == sum_formula(1_000_000))
```

```text
5050 5050
True
```

Both are correct. So which one is better?

<figure class="fig">
  <div class="versus">
    <div><h4>Adding in a loop</h4>
      <p>Adds the <code>n</code> numbers one by one.</p>
      <p><code>n = 100</code> → 100 additions<br><code>n = 1 000 000</code> → 1 000 000 additions</p>
      <p>The step count <b>grows with <code>n</code></b>.</p></div>
    <div class="ok"><h4>With the formula</h4>
      <p>One multiplication, one addition, one division.</p>
      <p><code>n = 100</code> → 3 operations<br><code>n = 1 000 000</code> → 3 operations</p>
      <p>The step count is <b>constant</b>.</p></div>
  </div>
  <figcaption>Both give the right result; the difference is how the work grows as the input grows.</figcaption>
</figure>

With `n` at 100 the difference does not matter. With `n` at a billion the
loop does a billion additions and the formula still a handful of
operations. **When comparing algorithms we look not at seconds but at how
the number of steps grows as the input grows.** That is exactly the topic
of the next section: complexity and Big O notation.

## Tracing an algorithm

The best way to understand an algorithm is to follow it step by step:
which line ran, how did the variables change? In the exercises of this
path, after writing your code press the **Step by step** button next to
**Run**; you will see line by line how `largest` changes through the loop.
When you are stuck, the same button lets you trace the sample solution.

## Summary

- An algorithm is ordered, clear steps that finish and turn input into
  output.
- Write the idea in **pseudocode** first, then turn it into Python.
- Correctness means working on **every input**, not on one example; always
  try the edge cases (empty, one element, negatives, all equal).
- A problem can have several algorithms; to compare them we look at how
  the **number of steps** grows as the input grows.
