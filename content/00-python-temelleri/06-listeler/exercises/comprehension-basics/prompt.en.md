You will use the one-line form for producing one list from another. It is
very common in real code and you need to be able to read it.

The data you have:

```python
scores = [90, 40, 75, 30, 65]
names = ["ada", "alan", "grace"]
```

**What you need to do — write all of them as comprehensions, no loops:**

1. `doubled` — each score doubled.
2. `passed` — only the scores of **50 and above**.
3. `upper_names` — all the names in upper case.
4. `short_names` — only the names **shorter than five letters**, in upper
   case.

Then print all four in order.

**Expected output:**

```
[180, 80, 150, 60, 130]
[90, 75, 65]
['ADA', 'ALAN', 'GRACE']
['ADA', 'ALAN']
```

> The form is `[expression for element in list]`. To filter, add
> `if condition` at the end. For upper case, `name.upper()`.
