Pseudocode has no single standard; books and interviews write it
differently. The notation used in this path and its Python equivalents:

| Pseudocode | Python |
|---|---|
| `x ← 5` | `x = 5` |
| `for each a in list:` | `for a in items:` |
| `for i from 0 to n-1:` | `for i in range(n):` |
| `if a > b: … else: …` | `if a > b: … else: …` |
| `while condition holds:` | `while condition:` |
| `result: x` | `return x` |
| `list[i]` | `items[i]` (the first element is `0`) |
| `length(list)` | `len(items)` |
| `empty list` | `[]` |

## An example: the first repeated letter

Problem: find the **first letter that repeats** in a word; `None` if there
is none.

By hand: "banana" → b (first time), a (first time), n (first time), a (**seen
it!**) → answer `a`.

Pseudocode:

```text
seen ← empty set
for each letter in the word:
    if letter is in seen:
        result: letter
    add letter to seen
result: none
```

Python:

```python
def first_repeated(word):
    seen = set()
    for letter in word:
        if letter in seen:
            return letter
        seen.add(letter)
    return None
```

Note that the two `result:` lines of the pseudocode became two separate
`return`s in Python. The first is **inside** the loop and leaves as soon as
the answer is found; the second runs when the loop ends without finding
one.

## When can you skip the pseudocode?

For a small problem, writing Python directly is fine. Write pseudocode
first when:

- there are several nested loops or conditions,
- in an interview you are expected to explain your idea before coding,
- you will have to explain the algorithm to someone else (or to yourself in
  three months).
