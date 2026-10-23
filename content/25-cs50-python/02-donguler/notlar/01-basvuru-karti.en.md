Everything from week 2 on one page.

## while

```python
i = 0
while i < 3:
    print("meow")
    i += 1
```

- The block runs again as long as the condition is true.
- Do not forget the line that will one day make the condition false
  (`i += 1`); otherwise you get an infinite loop.
- To stop an infinite loop: `Ctrl+C` in the terminal.

## for and range

| Code | Values |
|---|---|
| `range(3)` | `0, 1, 2` |
| `range(1, 4)` | `1, 2, 3` |
| `range(0, 10, 3)` | `0, 3, 6, 9` (in steps of three) |
| `range(5, 0, -1)` | `5, 4, 3, 2, 1` (backwards) |
| `for _ in range(3):` | `_` when the value is not used |
| `for c in "cat":` | goes over a string letter by letter |

## Loop control

| Keyword | What it does |
|---|---|
| `break` | leaves the loop right away |
| `continue` | skips the rest of the iteration and goes to the next |
| `return` (in a function) | leaves the function, and so the loop too |

The input validation pattern:

```python
while True:
    n = int(input("What's n? "))
    if n > 0:
        break
```

## List

| Code | Result (`s = ["Hermione", "Harry", "Ron"]`) |
|---|---|
| `s[0]` | `"Hermione"` (positions start at 0) |
| `s[2]` | `"Ron"` |
| `s[3]` | `IndexError` |
| `len(s)` | `3` |
| `for x in s:` | goes over the items in order |
| `for i in range(len(s)):` | goes over the positions (`0, 1, 2`) |

## Dictionary

| Code | Result |
|---|---|
| `d = {"Harry": "Gryffindor"}` | key `"Harry"`, value `"Gryffindor"` |
| `d["Harry"]` | `"Gryffindor"` |
| `d["Luna"]` | `KeyError` (no such key) |
| `for k in d:` | goes over the **keys**; the value is `d[k]` |
| `None` | "no value" |

## Repeating with strings

| Code | Result |
|---|---|
| `"-" * 5` | `"-----"` |
| `print("meow\n" * 3, end="")` | three lines of `meow`, no blank line at the end |
| `print("#", end="")` | prints without a line break |
| `print()` | just a line break |
