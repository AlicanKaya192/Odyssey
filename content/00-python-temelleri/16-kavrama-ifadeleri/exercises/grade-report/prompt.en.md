You will produce a class report: build it with comprehensions and print
it with format specifiers.

The data you have:

```python
scores = {"ada": 90, "alan": 45, "grace": 72, "gauss": 38}
```

**What to do:**

1. `passed` — the names that scored **50 or above** (a list, built with a
   comprehension).
2. `average` — the average of every score. Put a **generator expression**
   inside `sum()`.
3. `lines` — a list of lines like `"ada      90 ok"`: the name left
   aligned in **8**, the score right aligned in **3**, then a space and
   `"ok"` / `"no"`.
4. Print the lines with a loop, then the average with **one decimal
   place**, then the names that passed.

**Expected output:**

```
ada      90 ok
alan     45 no
grace    72 ok
gauss    38 no
Average: 61.2
Passed: ['ada', 'grace']
```

> A line holds both a conditional value and a format specifier; you can
> write it as `f"{name:<8}{score:>3} " + ("ok" if score >= 50 else "no")`.
