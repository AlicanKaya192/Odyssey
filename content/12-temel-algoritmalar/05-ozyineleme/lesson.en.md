# Recursion

Some problems are made of smaller copies of themselves. The size of a folder
is the sum of the files in it and **the sizes of its subfolders**; a
subfolder's size is found the same way. `5!` (5 factorial) is `5 × 4!`; and
`4!` is `4 × 3!`. The natural way to solve such problems is for a function
to **call itself**. This is called **recursion**.

## Two parts: the base case and the recursive step

Every recursive function must have two parts:

- **Base case:** the smallest problem whose answer is known directly. Here
  the function does **not** call itself. `1! = 1`.
- **Recursive case:** reduce the problem to a **smaller** copy and call
  itself with it. `n! = n × (n−1)!`.

```python
def factorial(n):
    if n <= 1:                     # base case
        return 1
    return n * factorial(n - 1)    # recursive step: n gets smaller
```

Every call decreases `n` by one and it eventually reaches the base case. If
these two conditions (there is a base case and every step gets closer to it)
do not hold, the function never finishes.

## The call stack

When a function calls another, Python puts the unfinished work aside (which
line it stopped at, what its variables are) and runs the called one. This
place for putting work aside is called the **call stack**: like a stack of
plates, the last one put on is taken first. In recursion many copies of the
same function sit on top of each other in the stack. To see it, let us print
every call with indentation:

```python
def factorial(n, depth=0):
    print("  " * depth + f"factorial({n}) cagrildi")
    if n <= 1:
        result = 1
    else:
        result = n * factorial(n - 1, depth + 1)
    print("  " * depth + f"factorial({n}) = {result}")
    return result

factorial(4)
```

```text
factorial(4) cagrildi
  factorial(3) cagrildi
    factorial(2) cagrildi
      factorial(1) cagrildi
      factorial(1) = 1
    factorial(2) = 2
  factorial(3) = 6
factorial(4) = 24
```

(`cagrildi` means "called".) First four calls piled up (each waiting for the
previous one's answer). `factorial(1)` was the base case and returned at once;
then the stack unwound in reverse: 1, 2, 6, 24. Seeing this two-way movement
(calls waiting on the way down, results combining on the way up) is the key
to understanding recursion. In the exercises the **Step by step** button
shows the stack layer by layer in the variables section.

## If you forget the base case

A function without a base case tries to call itself forever. To protect the
stack, Python sets a limit:

```python
import sys
print(sys.getrecursionlimit())

def countdown(n):
    return countdown(n - 1)       # no base case

try:
    countdown(5)
except RecursionError as error:
    print(type(error).__name__, "-", error)
```

```text
1000
RecursionError - maximum recursion depth exceeded
```

The limit is about **1000** levels of calls. That is why in Python
work whose depth can reach tens of thousands (walking a long list element by
element with recursion, say) is written as a loop. This is not a bug but a
choice of Python: unlike some languages, Python does not speed up recursive
calls by turning them into loops.

## Thinking recursively

To solve a problem with recursion, ask yourself three questions:

1. **What is its smallest form, and what is the answer?** (An empty list →
   total 0.)
2. **If I make it one step smaller, what is left?** (The first element and
   the rest of the list.)
3. **If I knew the answer for the smaller one, how would I build the bigger
   one's?** (The first element + the total of the rest.)

```python
def total(items):
    if not items:                        # 1. an empty list
        return 0
    return items[0] + total(items[1:])   # 2-3. first + the total of the rest
```

The third question requires **trusting that the smaller answer comes back
right**; instead of trying to trace every level in your head, think "the
function works on the smaller input; I am only building the last step". This
is sometimes called the **recursive leap of faith**.

Note: `items[1:]` builds a copy of the list on every call; this example is to
show the idea. On a long list, moving by index (`total(items, i + 1)`) is
cheaper.

## Where recursion shines

For work that can also be written as a loop, recursion is often
unnecessary. But in **nested structures** recursion is the most natural way,
because the structure itself is recursive:

```python
def deep_sum(items):
    result = 0
    for item in items:
        if isinstance(item, list):
            result += deep_sum(item)      # a sublist: the same problem, smaller
        else:
            result += item
    return result

print(deep_sum([1, [2, 3], [4, [5, [6]]]]))
```

```text
21
```

We do not know in advance how deeply the list is nested; to write it with a
loop we would have to keep our own stack. Folder trees, JSON documents,
decision trees and the **trees** of the coming sections are all like this.

The same idea appears in algorithms: **merge sort** in the next section
splits the list in two and sorts each half with itself. Binary search can be
written recursively too: "look at the middle, then do the same on a half".

## Watch out: doing the same work again and again

The definition of the Fibonacci numbers is recursive:
`fib(n) = fib(n−1) + fib(n−2)`, `fib(0) = 0`, `fib(1) = 1`. Let us turn the
definition directly into code and count **how many times it is called**:

```python
calls = 0

def fib(n):
    global calls
    calls += 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

for n in [10, 20, 25, 30]:
    calls = 0
    print(n, fib(n), calls)
```

```text
10 55 177
20 6765 21891
25 75025 242785
30 832040 2692537
```

**Millions** of calls for `fib(30)`. The reason: `fib(30)` calls `fib(29)` and
`fib(28)`; `fib(29)` calls `fib(28)` again; the same values are computed from
scratch over and over. The call count grows about 1.6 times every time `n`
goes up by 1: exponential growth. The fix (computing each result once and
keeping it) comes in ALG 2's **Dynamic Programming** section.

## Summary

- A recursive function calls itself with a **smaller** input.
- There must always be a **base case**, and every step must get closer to
  it.
- Calls pile up on the **call stack**; Python's depth limit is about
  1000, and exceeding it raises `RecursionError`.
- Thinking recursively: the smallest form, one step smaller, building the
  bigger answer from the smaller one.
- In nested structures (trees, nested lists, folders) recursion is the most
  natural way; if a plain loop can do it, the loop is often better.
- Recursion that solves the same subproblem again and again can grow
  exponentially.
