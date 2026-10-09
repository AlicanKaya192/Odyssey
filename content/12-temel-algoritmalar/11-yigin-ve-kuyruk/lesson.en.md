# Stacks and Queues

In some algorithms the **order** in which data is processed is everything.
Two basic structures set that order:

- **Stack:** last in, first out (LIFO). A pile of plates: you take the one you
  put on last first.
- **Queue:** first in, first out (FIFO). A ticket queue: whoever comes first
  is served first.

Both do only **two operations** in constant time: add at one end, take from
one end. That restriction is not a weakness but a strength: the algorithm
never has to think about "who is next?".

## A stack in Python: a list

The **end** of the list is the top of the stack: put with `append`, take with
`pop`. Both `O(1)`. To look at the top element without taking it,
`stack[-1]`.

```python
history = []
history.append("type: hello")
history.append("type: world")
history.append("delete: world")
print(history.pop())       # the last action is undone
print(history[-1])         # the next one to undo
```

**Undo (Ctrl+Z)** in a text editor is exactly a stack: what you did last is
undone first. So is the **call stack** of earlier sections: the function
called last finishes first.

## Stack use 1: checking brackets

Do the brackets in an expression close properly? `(a[b]{c})` is right,
`(a[b)]` is wrong. Put every opening bracket on the stack; when you see a
closing bracket, check whether the **top** of the stack is its partner. Why
the top? Because the bracket opened last must close first: exactly LIFO.

```python
def is_balanced(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack           # False if something was opened and never closed

for t in ["(a[b]{c})", "(a[b)]", "((", ""]:
    print(repr(t), is_balanced(t))
```

```text
'(a[b]{c})' True
'(a[b)]' False
'((' False
'' True
```

Three traps, all three in the code: the stack may be **empty** when a closing
bracket arrives (`")("`); the top bracket may be of the **wrong kind**
(`(a[b)]`); and brackets may be **left open** on the stack at the end (`((`).

## Stack use 2: evaluating postfix

One way to tell a computer `(3 + 4) * 2` without brackets is **postfix**
(reverse Polish notation): operators come **after** the numbers: `3 4 + 2 *`.
One stack is enough to evaluate it: push a number; on an operator, take the
top two numbers, apply it, push the result back.

```python
def eval_postfix(tokens):
    stack = []
    for token in tokens:
        if token in "+-*/":
            right = stack.pop()        # order matters: the right one comes off first
            left = stack.pop()
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            elif token == "*":
                stack.append(left * right)
            else:
                stack.append(left / right)
        else:
            stack.append(float(token))
        print(token, stack)
    return stack.pop()

print(eval_postfix(["3", "4", "+", "2", "*"]))
```

```text
3 [3.0]
4 [3.0, 4.0]
+ [7.0]
2 [7.0, 2.0]
* [14.0]
14.0
```

Calculators and compilers evaluate expressions internally in a similar way.

## Stack use 3: the next greater element

In daily temperatures, the question for each day: "how warm is the **first
warmer day after** it?". Brute force looks ahead for every day: `O(n²)`. A
**monotonic stack** keeps the days that have not found their answer yet; the
values in the stack always stand in decreasing order. When a new day arrives,
it is the answer for all colder days on top of the stack:

```python
def next_greater(values):
    result = [-1] * len(values)
    stack = []                                # indices of days waiting for an answer
    for i, x in enumerate(values):
        while stack and values[stack[-1]] < x:
            result[stack.pop()] = x           # a waiting day found its answer
        stack.append(i)
    return result
```

We compared the two methods by counting steps, for `[2, 7, 3, 5, 4, 6, 8]` and
for 5000 decreasing temperatures:

```text
([7, 8, 5, 6, 6, 8, -1], 13)
True 12497500 5000
```

The first line is the result and the monotonic stack's steps. On the second
line (sorted decreasing, brute force's worst day) the results are the same,
but brute force took 12.5 million steps and the monotonic stack 5000. Despite
the inner `while` it is `O(n)`: every day enters the stack **once** and leaves
**at most once**.

## A queue in Python: deque

Taking from the front of a list with `pop(0)` shifts the whole list (`O(n)`);
we measured that two sections ago. For a queue, `collections.deque`: add at
the end with `append`, take from the front with `popleft`, both `O(1)`.

```python
from collections import deque

queue = deque()
queue.append("Ada")
queue.append("Bora")
queue.append("Cem")
print(queue.popleft())     # the first to arrive
print(list(queue))
```

<figure class="fig">
  <div class="versus">
    <div><h4>Stack (LIFO)</h4>
      <p>Add: <code>append</code> → at the end<br>Take: <code>pop()</code> ← from the end</p>
      <p>After adding 1, 2, 3 the taking order is: <b>3, 2, 1</b></p>
      <p>Undo, brackets, diving deep</p></div>
    <div class="ok"><h4>Queue (FIFO)</h4>
      <p>Add: <code>append</code> → at the end<br>Take: <code>popleft()</code> ← from the front</p>
      <p>After adding 1, 2, 3 the taking order is: <b>1, 2, 3</b></p>
      <p>Processing in order, level by level</p></div>
  </div>
  <figcaption>Both add at the end; the difference is which end they take from.</figcaption>
</figure>

## Where are queues used?

- **Work processed in order:** printer queues, request queues, message queues
  (the Kafka simulation in the Big Data path is a queue).
- **Breadth-first search (BFS):** walking a graph or tree level by level, from
  near to far. It will be done with this queue in the Trees section and the Algorithm Techniques module's
  graph sections.
- **The last `k` events:** `deque(maxlen=k)` (we saw it in the sliding window
  section).

## Summary

- Stack: LIFO; in Python a list (`append`, `pop`, `stack[-1]`), all `O(1)`.
- Queue: FIFO; in Python `collections.deque` (`append`, `popleft`), `O(1)`.
  `pop(0)` on a list is `O(n)`.
- Stack patterns: undo, bracket checking, postfix evaluation, the call stack,
  the monotonic stack (next greater/smaller element in `O(n)`).
- Queue patterns: processing in order, BFS, the last `k` events.
